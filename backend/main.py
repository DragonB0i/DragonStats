import os
from typing import Optional
from fastapi import FastAPI, Response, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from backend.github_service import GitHubService
from backend.badge_generator import (
    generate_profile_card,
    generate_activity_card,
    generate_languages_card,
    generate_capsule_badge,
)

app = FastAPI(
    title="DragonStats",
    description="DragonStats is a lightweight FastAPI-powered GitHub profile analytics generator that creates dynamic SVG cards, badges, and contribution snake assets for GitHub profiles.",
    version="1.0.0",
)

# Enable CORS for cross-origin analytics requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

github_service = GitHubService()

# Retrieve default username from environment, fallback to a popular demo account if not set
DEFAULT_USERNAME = os.getenv("GITHUB_USERNAME", "DragonB0i")

@app.on_event("startup")
async def startup_event():
    # Service is initialized on import, but this event hook is kept for lifecycle completeness
    pass

@app.on_event("shutdown")
async def shutdown_event():
    await github_service.close()

def resolve_username(username: Optional[str]) -> str:
    """Helper to resolve the username from query parameter or environment variable."""
    resolved = username or DEFAULT_USERNAME
    if not resolved:
        raise HTTPException(
            status_code=400,
            detail="Username not specified. Provide the 'username' query parameter or configure GITHUB_USERNAME environment variable.",
        )
    return resolved.strip()

def create_svg_response(svg_content: str) -> Response:
    """Helper to create a response with correct SVG headers to prevent aggressive caching by GitHub Camo."""
    return Response(
        content=svg_content,
        media_type="image/svg+xml",
        headers={
            "Cache-Control": "public, max-age=600",  # Cache for 10 minutes in browsers/GitHub Camo
            "Pragma": "no-cache",
            "Expires": "600",
        },
    )

# --- JSON API Endpoints (FEATURE 2) ---

@app.get("/")
async def root():
    return {
        "status": "online",
        "message": "DragonStats API is active. Access badges at /badge/* and JSON API at /api/*",
        "default_username": DEFAULT_USERNAME,
        "docs_url": "/docs"
    }

@app.get("/api/profile")
async def get_profile(username: Optional[str] = Query(None, description="GitHub username (defaults to GITHUB_USERNAME env var)")):
    user = resolve_username(username)
    try:
        profile_data = await github_service.get_profile(user)
        return profile_data
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/repos")
async def get_repos(username: Optional[str] = Query(None, description="GitHub username")):
    user = resolve_username(username)
    try:
        # Check if profile exists first to trigger 404 if invalid user
        await github_service.get_profile(user)
        repos_data = await github_service.get_repos(user)
        return repos_data
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/languages")
async def get_languages(username: Optional[str] = Query(None, description="GitHub username")):
    user = resolve_username(username)
    try:
        # Check if profile exists first to trigger 404
        await github_service.get_profile(user)
        languages_data = await github_service.get_languages(user)
        return languages_data
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- SVG Badge Endpoints (FEATURE 3) ---

@app.get("/badge/profile")
async def badge_profile(username: Optional[str] = Query(None, description="GitHub username")):
    user = resolve_username(username)
    try:
        profile = await github_service.get_profile(user)
        avatar_b64 = await github_service.get_avatar_base64(profile["avatar"])
        
        svg = generate_profile_card(
            username=profile["username"],
            name=profile["name"],
            avatar_base64=avatar_b64,
            followers=profile["followers"],
            following=profile["following"],
            public_repos=profile["public_repos"],
            created_at=profile["created_at"],
        )
        return create_svg_response(svg)
    except Exception as e:
        # Generate an error SVG badge
        error_svg = generate_capsule_badge("Profile Error", "User Not Found", 100, 110)
        return create_svg_response(error_svg)

@app.get("/badge/activity")
async def badge_activity(username: Optional[str] = Query(None, description="GitHub username")):
    user = resolve_username(username)
    try:
        profile = await github_service.get_profile(user)
        repos = await github_service.get_repos(user)
        total_contributions = await github_service.get_total_contributions(user)
        
        svg = generate_activity_card(
            username=profile["username"],
            total_contributions=total_contributions,
            stars_received=repos["stars_received"],
            forks=repos["forks"],
            public_repos=repos["repository_count"],
        )
        return create_svg_response(svg)
    except Exception as e:
        error_svg = generate_capsule_badge("Activity Error", "Unavailable", 110, 90)
        return create_svg_response(error_svg)

@app.get("/badge/languages")
async def badge_languages(
    username: Optional[str] = Query(None, description="GitHub username"),
    style: str = Query("card", description="Style of the badge: 'card' (180px) or 'badge' (capsule)")
):
    user = resolve_username(username)
    try:
        languages = await github_service.get_languages(user)
        
        if style == "badge":
            top_lang = next(iter(languages.keys())) if languages else "N/A"
            svg = generate_capsule_badge("Top Language", top_lang, 110, 80)
        else:
            svg = generate_languages_card(user, languages)
            
        return create_svg_response(svg)
    except Exception as e:
        error_svg = generate_capsule_badge("Languages Error", "Unavailable", 120, 90)
        return create_svg_response(error_svg)

@app.get("/badge/repos")
async def badge_repos(username: Optional[str] = Query(None, description="GitHub username")):
    user = resolve_username(username)
    try:
        repos = await github_service.get_repos(user)
        svg = generate_capsule_badge("Repositories", str(repos["repository_count"]), 110, 60)
        return create_svg_response(svg)
    except Exception as e:
        error_svg = generate_capsule_badge("Repos", "Error", 60, 50)
        return create_svg_response(error_svg)

@app.get("/badge/stars")
async def badge_stars(username: Optional[str] = Query(None, description="GitHub username")):
    user = resolve_username(username)
    try:
        repos = await github_service.get_repos(user)
        svg = generate_capsule_badge("Stars", str(repos["stars_received"]), 70, 60)
        return create_svg_response(svg)
    except Exception as e:
        error_svg = generate_capsule_badge("Stars", "Error", 60, 50)
        return create_svg_response(error_svg)

@app.get("/badge/commits")
async def badge_commits(username: Optional[str] = Query(None, description="GitHub username")):
    user = resolve_username(username)
    try:
        total_contributions = await github_service.get_total_contributions(user)
        svg = generate_capsule_badge("Contributions", str(total_contributions), 110, 80)
        return create_svg_response(svg)
    except Exception as e:
        error_svg = generate_capsule_badge("Contributions", "Error", 110, 60)
        return create_svg_response(error_svg)
