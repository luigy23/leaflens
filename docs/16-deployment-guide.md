# 16. Deployment Guide

End-to-end instructions to publish LeafLens to public URLs that any laptop
or phone can reach.

Target platforms:
- **Backend + database** → Render (free tier, Docker-based)
- **Frontend** → Vercel (hobby tier, static)

Total cost: $0. Total time once your accounts are set up: ~30 minutes.

---

## 0. Prerequisites

You need a free account on each of:
- GitHub (probably already have one)
- Render — sign up with GitHub at https://render.com
- Vercel — sign up with GitHub at https://vercel.com

You also need the LeafLens repo pushed to GitHub. If you haven't done that:

```bash
cd ~/Documents/GitHub/leaflens
gh repo create leaflens --public --source=. --remote=origin --push
```

(Requires the `gh` CLI; install with `brew install gh` and `gh auth login` once.)

---

## 1. Backend — Render

The repository already contains `render.yaml` and `Dockerfile`. Render reads
these automatically.

### 1.1 Add the model checkpoint to a release asset

The trained checkpoint (`models/checkpoints/best.pt`) is 90 MB — too large for
git but small enough for a GitHub release.

```bash
# From the repo root, with the best.pt already chosen:
gh release create v1.0.0 models/checkpoints/best.pt models/checkpoints/class_names.json \
  --title "LeafLens model v1.0.0" \
  --notes "ResNet-50 / 92.38% test top-1 / 47 classes"
```

Note the URL of `best.pt` from the release page. Render will download it
on container startup.

### 1.2 Update the Dockerfile to fetch the checkpoint

Edit `Dockerfile` to add a download step before `gunicorn` starts:

```dockerfile
# After installing dependencies, before CMD:
ARG MODEL_URL
RUN if [ -n "$MODEL_URL" ]; then \
      mkdir -p models/checkpoints && \
      curl -L -o models/checkpoints/best.pt "$MODEL_URL"; \
    fi
```

Then in Render's web UI, set the Docker build arg `MODEL_URL` to the release
asset URL from step 1.1.

### 1.3 Create the Render service

1. Log in to Render → **New +** → **Blueprint**.
2. Connect the `leaflens` GitHub repo.
3. Render reads `render.yaml`, creates:
   - `leaflens-api` (web service, Docker)
   - `leaflens-db` (PostgreSQL free)
4. Wait for the first build (~10 min — torch alone is heavy).
5. The service URL will be `https://leaflens-api.onrender.com` (or similar).

### 1.4 Seed the production database

The Postgres database is created empty. Run the seeder against it once:

```bash
# Locally, with the production DATABASE_URL exported:
export DATABASE_URL="$(render secrets show leaflens-db --connection-string)"
source .venv/bin/activate
python scripts/seed_db.py
unset DATABASE_URL
```

(If you don't have the `render` CLI, copy the connection string from the
Render dashboard.)

### 1.5 Verify

```bash
curl https://leaflens-api.onrender.com/api/health
```

Should return `{"status": "ok", "num_classes": 47, ...}`.

---

## 2. Frontend — Vercel

### 2.1 Connect the repository

1. Log in to Vercel → **Add New** → **Project**.
2. Import the `leaflens` GitHub repo.
3. **Root directory**: set to `frontend`.
4. **Framework preset**: Vite (auto-detected).
5. **Environment variables**: add
   - `VITE_API_BASE_URL` = `https://leaflens-api.onrender.com`

### 2.2 Deploy

Click **Deploy**. First build is ~1 minute. The site goes live at a URL
like `https://leaflens-<hash>.vercel.app`.

### 2.3 Set up a custom URL (optional)

In the Vercel project settings, you can rename to `leaflens.vercel.app`
if available. Update the `ALLOWED_ORIGINS` env var on Render to match.

---

## 3. Smoke test the full deployment

```bash
# Health
curl https://leaflens-api.onrender.com/api/health

# Predict (with a sample image)
curl -X POST https://leaflens-api.onrender.com/api/predict \
  -F "image=@data/raw/house_plant_species/Pothos\ \(Ivy\ arum\)/1.jpg"

# Open frontend
open https://leaflens.vercel.app
```

Then upload a phone photo through the web UI and confirm you see the species
+ care card.

---

## 4. Render free-tier notes

- The web service **sleeps after 15 minutes of inactivity**. First request
  after sleep takes 30–60 seconds while Render boots the container. Demo
  tip: hit `/api/health` once before walking on stage.
- PostgreSQL free instances **expire after 90 days**. For an academic project
  this is fine; for production, upgrade or migrate.
- Outbound bandwidth is metered (100 GB/month). LeafLens at academic scale
  is nowhere near that ceiling.

---

## 5. Rollback

If a deployment goes bad:
- Render: dashboard → service → Deploys → click any previous deploy → **Redeploy**.
- Vercel: dashboard → project → Deployments → click a previous one → **Promote to Production**.

Both providers keep a history of every deploy.

---

## 6. Tear-down (when the project is done)

- Render: Settings → Delete Service (both `leaflens-api` and `leaflens-db`).
- Vercel: Settings → General → Delete Project.
- GitHub: optional — `gh repo delete luigy23/leaflens --yes` to remove the repo.

Then run the local `scripts/cleanup.sh --hard` to free disk space on the
laptop.
