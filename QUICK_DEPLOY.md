# ⚡ Quick Deployment Guide

## Fastest Way: Deploy to Render (5 minutes)

### Step 1: Prepare Your Code

1. **Handle the Model File**
   Since `model.pth` is in `.gitignore`, you have two options:
   
   **Option A**: Temporarily include it (if file < 100MB)
   ```bash
   git rm --cached model.pth
   git add model.pth
   git commit -m "Add model file for deployment"
   ```
   
   **Option B**: Use Git LFS for large files
   ```bash
   git lfs install
   git lfs track "*.pth"
   git add .gitattributes model.pth
   git commit -m "Add model with LFS"
   ```

2. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Ready for deployment"
   git push origin main
   ```

### Step 2: Deploy on Render

1. **Sign up**: https://render.com (use GitHub to sign in)

2. **Create New Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repo
   - Select the repository

3. **Configure Settings**
   - **Name**: `bu-chatbot` (or your choice)
   - **Region**: Choose closest to you
   - **Branch**: `main`
   - **Root Directory**: `BU-CHATBOTProject` (if your repo has this folder)
   - **Environment**: `Python 3`
   - **Build Command**:
     ```
     pip install -r requirements.txt && python -m nltk.downloader punkt wordnet averaged_perceptron_tagger
     ```
   - **Start Command**: `gunicorn app:app`

4. **Click "Create Web Service"**

5. **Wait for deployment** (2-5 minutes)

6. **Your app is live!** 🎉

   Example URL: `https://bu-chatbot.onrender.com`

### Step 3: Test

Visit your URL and try sending a message to the chatbot.

---

## Alternative: Railway (Even Easier)

1. **Push code to GitHub** (same as Step 1 above)

2. **Go to**: https://railway.app

3. **Sign up** with GitHub

4. **New Project** → **Deploy from GitHub repo**

5. **Select your repo**

6. **Configure**:
   - Build Command: `cd BU-CHATBOTProject && pip install -r requirements.txt && python -m nltk.downloader punkt wordnet averaged_perceptron_tagger`
   - Start Command: `cd BU-CHATBOTProject && gunicorn app:app --bind 0.0.0.0:$PORT`

7. **Done!** Railway auto-deploys on every push.

---

## Important Notes

✅ **Model File**: Make sure `model.pth` is accessible in your deployment
✅ **NLTK Data**: Included in build command above
✅ **API URL**: Already auto-detects production URL in `script.js`
✅ **Static Files**: Flask serves them automatically

---

## Troubleshooting

**"Model file not found" error?**
- Check if `model.pth` is in the same directory as `app.py`
- Verify it's committed to git (or uploaded separately)

**"NLTK data missing" error?**
- The build command includes NLTK downloads - wait for build to complete
- Check build logs on Render/Railway dashboard

**CORS errors?**
- Already handled with `flask-cors` in your app
- No additional configuration needed

---

## Next Steps After Deployment

1. **Custom Domain** (Optional): Add your own domain in Render/Railway settings
2. **Environment Variables**: Set production configs if needed
3. **Monitoring**: Check logs regularly for errors

---

**Need more details?** See `DEPLOYMENT.md` for all deployment options.

