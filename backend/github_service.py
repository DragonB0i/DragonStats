import os
import time
import base64
import httpx
from typing import Dict, Any, List, Optional
from dotenv import load_dotenv

load_dotenv()

class GitHubService:
    def __init__(self):
        self.github_token = os.getenv("GITHUB_TOKEN")
        self.cache: Dict[str, tuple[float, Any]] = {}
        self.cache_ttl = 600  # 10 minutes cache TTL
        
        # Build headers
        headers = {
            "Accept": "application/vnd.github+json",
            "User-Agent": "github-profile-analytics-api",
            "X-GitHub-Api-Version": "2022-11-28",
        }
        if self.github_token:
            headers["Authorization"] = f"Bearer {self.github_token}"
            
        self.client = httpx.AsyncClient(headers=headers, timeout=10.0)

    async def close(self):
        await self.client.aclose()

    def get_cache(self, key: str) -> Optional[Any]:
        if key in self.cache:
            expiry, data = self.cache[key]
            if time.time() < expiry:
                return data
            else:
                del self.cache[key]
        return None

    def set_cache(self, key: str, data: Any):
        self.cache[key] = (time.time() + self.cache_ttl, data)

    async def get_profile(self, username: str) -> Dict[str, Any]:
        cache_key = f"profile_{username}"
        cached = self.get_cache(cache_key)
        if cached:
            return cached

        url = f"https://api.github.com/users/{username}"
        try:
            response = await self.client.get(url)
            if response.status_code == 404:
                raise httpx.HTTPStatusError("User not found", request=response.request, response=response)
            response.raise_for_status()
            
            data = response.json()
            profile_data = {
                "username": data.get("login"),
                "name": data.get("name") or data.get("login"),
                "avatar": data.get("avatar_url"),
                "followers": data.get("followers", 0),
                "following": data.get("following", 0),
                "public_repos": data.get("public_repos", 0),
                "created_at": data.get("created_at")[:10] if data.get("created_at") else "N/A",
            }
            self.set_cache(cache_key, profile_data)
            return profile_data
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                raise ValueError(f"GitHub user '{username}' not found.")
            raise Exception(f"GitHub API Error: {e.response.text}")
        except Exception as e:
            raise Exception(f"Failed to fetch profile: {str(e)}")

    async def get_repos_raw(self, username: str) -> List[Dict[str, Any]]:
        cache_key = f"repos_raw_{username}"
        cached = self.get_cache(cache_key)
        if cached:
            return cached

        repos = []
        page = 1
        # Fetch up to 3 pages (300 repositories) to balance detail and performance
        max_pages = 3
        
        try:
            while page <= max_pages:
                url = f"https://api.github.com/users/{username}/repos?per_page=100&page={page}"
                response = await self.client.get(url)
                if response.status_code != 200:
                    break
                page_repos = response.json()
                if not page_repos:
                    break
                repos.extend(page_repos)
                if len(page_repos) < 100:
                    break
                page += 1
                
            self.set_cache(cache_key, repos)
            return repos
        except Exception as e:
            print(f"Error fetching repos: {e}")
            return []

    async def get_repos(self, username: str) -> Dict[str, Any]:
        repos_data = await self.get_repos_raw(username)
        
        stars_received = sum(repo.get("stargazers_count", 0) for repo in repos_data)
        forks = sum(repo.get("forks_count", 0) for repo in repos_data)
        
        # Aggregate languages
        lang_counts = {}
        for repo in repos_data:
            lang = repo.get("language")
            if lang:
                lang_counts[lang] = lang_counts.get(lang, 0) + 1
                
        sorted_langs = sorted(lang_counts.items(), key=lambda x: x[1], reverse=True)
        most_used_languages = [lang for lang, _ in sorted_langs[:5]]
        
        return {
            "repository_count": len(repos_data),
            "stars_received": stars_received,
            "forks": forks,
            "most_used_languages": most_used_languages,
        }

    async def get_languages(self, username: str) -> Dict[str, float]:
        repos_data = await self.get_repos_raw(username)
        
        lang_counts = {}
        total_repos_with_lang = 0
        
        for repo in repos_data:
            lang = repo.get("language")
            if lang:
                lang_counts[lang] = lang_counts.get(lang, 0) + 1
                total_repos_with_lang += 1
                
        languages_percentage = {}
        if total_repos_with_lang > 0:
            for lang, count in lang_counts.items():
                languages_percentage[lang] = round((count / total_repos_with_lang) * 100, 1)
                
        # Sort by percentage descending
        sorted_percentages = dict(sorted(languages_percentage.items(), key=lambda x: x[1], reverse=True))
        return sorted_percentages

    async def get_total_contributions(self, username: str) -> int:
        cache_key = f"contributions_{username}"
        cached = self.get_cache(cache_key)
        if cached is not None:
            return cached

        commits_count = 0
        issues_count = 0

        # Fetch commits count
        try:
            commit_url = f"https://api.github.com/search/commits?q=author:{username}"
            commit_response = await self.client.get(commit_url)
            if commit_response.status_code == 200:
                commits_count = commit_response.json().get("total_count", 0)
            elif commit_response.status_code in [403, 429]:
                print(f"Commit Search API rate limited for {username}. Using fallback metrics.")
                # Fallback estimate based on repo count and stars
                profile = await self.get_profile(username)
                repos = await self.get_repos(username)
                commits_count = (profile.get("public_repos", 0) * 15) + (repos.get("stars_received", 0) * 5)
        except Exception as e:
            print(f"Error fetching commits count: {e}")

        # Fetch issues/PRs count
        try:
            issues_url = f"https://api.github.com/search/issues?q=author:{username}"
            issues_response = await self.client.get(issues_url)
            if issues_response.status_code == 200:
                issues_count = issues_response.json().get("total_count", 0)
        except Exception as e:
            print(f"Error fetching issues count: {e}")

        total_contributions = commits_count + issues_count
        self.set_cache(cache_key, total_contributions)
        return total_contributions

    async def get_avatar_base64(self, avatar_url: str) -> str:
        cache_key = f"avatar_b64_{avatar_url}"
        cached = self.get_cache(cache_key)
        if cached:
            return cached

        try:
            response = await self.client.get(avatar_url)
            if response.status_code == 200:
                content_type = response.headers.get("Content-Type", "image/jpeg")
                # Ensure content_type is indeed an image type
                if not content_type.startswith("image/"):
                    content_type = "image/jpeg"
                encoded = base64.b64encode(response.content).decode("utf-8")
                base64_str = f"data:{content_type};base64,{encoded}"
                self.set_cache(cache_key, base64_str)
                return base64_str
        except Exception as e:
            print(f"Error downloading/encoding avatar: {e}")

        # Cyber neon style SVG placeholder avatar if download fails
        default_avatar = (
            "data:image/svg+xml;utf8,"
            "<svg xmlns='http://www.w3.org/2000/svg' width='100' height='100' viewBox='0 0 100 100'>"
            "<defs>"
            "<linearGradient id='avatarGrad' x1='0%' y1='0%' x2='100%' y2='100%'>"
            "<stop offset='0%' stop-color='%233c0d68' />"
            "<stop offset='100%' stop-color='%23601c9a' />"
            "</linearGradient>"
            "</defs>"
            "<circle cx='50' cy='50' r='48' fill='url(%23avatarGrad)' stroke='%2339ff14' stroke-width='2'/>"
            "<text x='50' y='58' font-family='Courier New, monospace' font-weight='bold' font-size='26' fill='%2339ff14' text-anchor='middle'>&gt;_</text>"
            "</svg>"
        )
        return default_avatar
