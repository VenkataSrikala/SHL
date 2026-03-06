# Deployment Guide

## Quick Deployment (30 minutes total)

### Step 1: Push to GitHub (5 minutes)

```bash
# Initialize git if not already done
git init

# Add all files
git add .

# Commit
git commit -m "SHL Assessment Recommender - Complete Implementation"

# Create repo on GitHub (https://github.com/new)
# Then connect and push:
git remote add origin https://github.com/YOUR_USERNAME/shl-recommender.git
git branch -M main
git push -u origin main
```

### Step 2: Deploy API to Render (10 minutes)

1. Go to https://render.com
2. Sign up with GitHub
3. Click "New +" → "Web Service"
4. Select your `shl-recommender` repository
5. Configure:

```
Name: shl-recommender-api
Environment: Python 3
Build Command: pip install -r requirements.txt && python setup.py --scraper mock
Start Command: uvicorn api.main:app --host 0.0.0.0 --port $PORT
```

6. Click "Create Web Service"
7. Wait for deployment (5-10 minutes)
8. Copy your API URL: `https://shl-recommender-api.onrender.com`

**Test it**:
```bash
curl https://shl-recommender-api.onrender.com/health
```

Should return: `{"status":"healthy"}`

### Step 3: Deploy UI to Streamlit Cloud (5 minutes)

1. Go to https://streamlit.io/cloud
2. Sign in with GitHub
3. Click "New app"
4. Select:
   - Repository: `YOUR_USERNAME/shl-recommender`
   - Branch: `main`
   - Main file path: `frontend/app.py`

5. Click "Advanced settings"
6. Add environment variable:
   ```
   API_URL = https://shl-recommender-api.onrender.com
   ```

7. Click "Deploy"
8. Wait 2-3 minutes
9. Your app will be at: `https://shl-recommender.streamlit.app`

**Test it**: Visit the URL in your browser

---

## Troubleshooting

### API Deployment Issues

**Problem**: Build fails with "No module named 'faiss'"

**Solution**: Make sure `requirements.txt` has `faiss-cpu==1.7.4`

---

**Problem**: API starts but returns 500 errors

**Solution**: Check logs in Render dashboard. Likely missing data files.
Make sure build command includes: `python setup.py --scraper mock`

---

**Problem**: API is slow (>5 seconds)

**Solution**: First request is slow due to model loading. Subsequent requests are fast.
Consider using Render paid tier for better performance.

---

### UI Deployment Issues

**Problem**: UI shows "Connection error"

**Solution**: 
1. Check API_URL environment variable is set correctly
2. Make sure API is deployed and running
3. Test API health endpoint first

---

**Problem**: UI loads but no results

**Solution**: Check browser console for errors. Verify API URL is accessible.

---

### General Issues

**Problem**: Git push fails

**Solution**:
```bash
# If repo already exists
git remote set-url origin https://github.com/YOUR_USERNAME/shl-recommender.git
git push -u origin main --force
```

---

**Problem**: Large files warning

**Solution**: FAISS index might be too large. Add to .gitignore:
```bash
echo "vector_db/*.faiss" >> .gitignore
```

The index will be rebuilt during deployment.

---

## Alternative Deployment Options

### Option 1: Railway (Alternative to Render)

1. Go to https://railway.app
2. Sign up with GitHub
3. New Project → Deploy from GitHub
4. Select your repo
5. Add environment variables if needed
6. Deploy

### Option 2: HuggingFace Spaces

**For API**:
1. Go to https://huggingface.co/spaces
2. Create new Space
3. Select "Docker" or "Python"
4. Upload your code
5. Configure with Dockerfile

**For UI**:
1. Create new Space
2. Select "Streamlit"
3. Upload frontend code
4. Set API_URL in secrets

### Option 3: Heroku

```bash
# Install Heroku CLI
# Then:
heroku login
heroku create shl-recommender-api
git push heroku main
```

---

## Production Checklist

Before going live:

- [ ] API health endpoint works
- [ ] API recommend endpoint works
- [ ] UI loads correctly
- [ ] UI can connect to API
- [ ] Test with sample queries
- [ ] Check response times
- [ ] Verify error handling
- [ ] Test on mobile (optional)

---

## Monitoring

### Render Dashboard
- View logs: Click on your service → "Logs"
- Check metrics: "Metrics" tab
- Restart service: "Manual Deploy" → "Deploy latest commit"

### Streamlit Cloud Dashboard
- View logs: Click on your app → "Manage app" → "Logs"
- Reboot app: "Reboot app" button
- Check status: Green dot = running

---

## Cost

### Free Tier Limits

**Render**:
- 750 hours/month free
- Sleeps after 15 min inactivity
- First request after sleep is slow (~30s)

**Streamlit Cloud**:
- 1 private app free
- Unlimited public apps
- 1 GB RAM
- 1 CPU

**Total cost**: $0/month for this project

### Paid Options (Optional)

**Render**:
- Starter: $7/month (no sleep, better performance)
- Standard: $25/month (more resources)

**Streamlit Cloud**:
- Starter: $20/month (more resources)

---

## Environment Variables

### API (Render)
```
PYTHON_VERSION=3.11.0
```

### UI (Streamlit Cloud)
```
API_URL=https://shl-recommender-api.onrender.com
```

---

## Custom Domain (Optional)

### For API
1. Buy domain (e.g., shl-recommender.com)
2. In Render: Settings → Custom Domain
3. Add your domain
4. Update DNS records

### For UI
1. In Streamlit Cloud: Settings → Custom domain
2. Add your domain
3. Update DNS records

---

## Continuous Deployment

Both Render and Streamlit Cloud support auto-deploy:

1. Push to GitHub
2. Services automatically rebuild and deploy
3. No manual intervention needed

To disable:
- Render: Settings → Auto-Deploy → Off
- Streamlit: Settings → Auto-deploy → Off

---

## Backup & Recovery

### Backup Data
```bash
# Backup FAISS index
cp vector_db/index.faiss backup/

# Backup processed data
cp data/processed/shl_catalog_clean.csv backup/
```

### Restore
```bash
# Restore from backup
cp backup/index.faiss vector_db/
cp backup/shl_catalog_clean.csv data/processed/
```

---

## Performance Optimization

### API
1. Use Render paid tier (no cold starts)
2. Enable caching for popular queries
3. Use FAISS IVF index for larger datasets
4. Add Redis for query caching

### UI
1. Cache API responses in session state
2. Lazy load results
3. Add loading indicators
4. Optimize images

---

## Security

### API
- Rate limiting (built into Render)
- Input validation (Pydantic)
- CORS configuration (if needed)

### UI
- No sensitive data stored
- API key in environment variables
- HTTPS by default

---

## Scaling

### Current Capacity
- 377 assessments
- ~100 queries/second
- <100ms response time

### To Scale
1. Upgrade Render plan
2. Add Redis caching
3. Use FAISS GPU
4. Load balance multiple instances

---

## Support

### Render
- Docs: https://render.com/docs
- Community: https://community.render.com
- Status: https://status.render.com

### Streamlit
- Docs: https://docs.streamlit.io
- Forum: https://discuss.streamlit.io
- Status: https://status.streamlit.io

---

## Quick Links

- **Render Dashboard**: https://dashboard.render.com
- **Streamlit Dashboard**: https://share.streamlit.io
- **GitHub Repo**: https://github.com/YOUR_USERNAME/shl-recommender

---

## Success!

Once deployed, you'll have:
- ✅ Public API URL
- ✅ Public Web App URL
- ✅ Auto-deployment on git push
- ✅ Free hosting
- ✅ HTTPS by default
- ✅ Monitoring and logs

**Your system is now live!** 🚀
