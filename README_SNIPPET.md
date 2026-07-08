# DragonStats Profile Analytics Snippet

DragonStats is a lightweight FastAPI-powered GitHub profile analytics generator that creates dynamic SVG cards, badges, and contribution snake assets for GitHub profiles.

Copy and paste the sections below into your GitHub profile README (typically in your `DragonB0i/DragonB0i` repository).

---

## 1. Analytics Cards Snippet

Copy this section to display your dynamic analytics cards. 

> [!NOTE]
> Replace `API_URL` with your actual deployed backend URL (e.g. `https://my-github-analytics.vercel.app` or `https://my-github-analytics.onrender.com`).
> If you wish to query stats for a specific user, you can append `?username=DragonB0i` to the URLs (e.g., `API_URL/badge/profile?username=DragonB0i`).

```markdown
# GitHub Analytics

<div align="center">

<img height="180" src="API_URL/badge/profile"/>

<img height="180" src="API_URL/badge/activity"/>

</div>

<div align="center">

<img height="180" src="API_URL/badge/languages"/>

</div>
```

---

## 2. Contribution Snake Snippet

Copy this section to display your animated contribution snake.

> [!NOTE]
> If your snake workflow commits the SVG to the `output` branch (recommended), replace `snake.svg` with:
> `https://raw.githubusercontent.com/DragonB0i/DragonB0i/output/snake.svg`

```markdown
## Contribution Snake

<div align="center">

<img src="snake.svg"/>

</div>
```

---

## 3. Setup and Deployment Guide

### A. Deploying the Backend API

#### Option 1: Deploying to Vercel (Recommended)
This repository includes a `vercel.json` config ready for deployment.
1. Sign in to [Vercel](https://vercel.com).
2. Click **Add New** > **Project** and import this repository.
3. In the **Environment Variables** section, add:
   - `GITHUB_USERNAME`: Your GitHub username (e.g. `DragonB0i`) to serve as the default profile.
   - `GITHUB_TOKEN`: A GitHub Personal Access Token (PAT) with `read:user` and `repo` scopes. (Highly recommended to avoid hitting GitHub API rate limits!).
4. Click **Deploy**. Vercel will build and launch your FastAPI backend serverless functions.

#### Option 2: Deploying to Render
1. Sign in to [Render](https://render.com).
2. Click **New** > **Web Service** and connect this repository.
3. Configure the following:
   - **Language**: `Python`
   - **Build Command**: `pip install -r backend/requirements.txt`
   - **Start Command**: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
4. In the **Environment Variables** settings, add:
   - `GITHUB_USERNAME`: Your GitHub username.
   - `GITHUB_TOKEN`: Your GitHub Personal Access Token (PAT).
5. Click **Create Web Service**.

---

### B. Setting Up the GitHub Action for Snake Generation

For the GitHub Action to commit the generated contribution snake to the `output` branch, you must give it write permissions:

1. Go to your repository on GitHub.
2. Click **Settings** > **Actions** > **General**.
3. Scroll down to **Workflow permissions**.
4. Select **Read and write permissions**.
5. Click **Save**.
6. Trigger the workflow manually by going to the **Actions** tab, selecting **Generate Contribution Snake**, clicking **Run workflow**, and choosing the `main` branch.
7. Once completed, a new branch named `output` will be created automatically containing `snake.svg`.
