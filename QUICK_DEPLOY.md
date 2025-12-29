# 🚀 Quick Deploy Guide - Launch Your App Online

Follow these simple steps to get your app running on the internet!

---

## 📋 Step-by-Step: Railway + Vercel (Easiest Method)

### 🎯 Part 1: Deploy Backend on Railway (10 minutes)

#### Step 1: Sign Up
1. Open your browser
2. Go to: **https://railway.app**
3. Click **"Start a New Project"** or **"Login"**
4. Click **"Login with GitHub"**
5. Authorize Railway to access your GitHub account

#### Step 2: Create New Project
1. After logging in, click **"New Project"** button (top right)
2. Select **"Deploy from GitHub repo"**
3. You'll see a list of your repositories
4. Find and click: **`saadh472/voice-automation-hub`**

#### Step 3: Configure Backend
Railway will start deploying automatically. You need to configure it:

1. Click on the service that was created
2. Go to **"Settings"** tab
3. Scroll down to **"Source"** section:
   - **Root Directory:** Type `backend`
4. Scroll to **"Deploy"** section:
   - **Build Command:** `./mvnw clean package -DskipTests`
   - **Start Command:** `java -jar target/*.jar`
5. Click **"Save"** or changes auto-save

#### Step 4: Add Database
1. In your Railway project dashboard, click **"+ New"** button
2. Select **"Database"**
3. Click **"Add PostgreSQL"**
4. Wait 1-2 minutes for database to be created
5. Railway automatically sets `DATABASE_URL` - you don't need to do anything!

#### Step 5: Get Your Backend URL
1. Click on your backend service (not the database)
2. Go to **"Settings"** tab
3. Scroll to **"Networking"** section
4. Find **"Public Domain"** or **"Generate Domain"**
5. Click **"Generate Domain"** if needed
6. **Copy the URL** (looks like: `voice-automation-backend-production.up.railway.app`)
7. **Save this URL** - you'll need it for frontend!

✅ **Backend is now live!** Test it: `https://your-backend-url.railway.app/api/health`

---

### 🎯 Part 2: Deploy Frontend on Vercel (10 minutes)

#### Step 1: Sign Up
1. Open a new browser tab
2. Go to: **https://vercel.com**
3. Click **"Sign Up"** or **"Login"**
4. Click **"Continue with GitHub"**
5. Authorize Vercel to access your GitHub account

#### Step 2: Import Project
1. After logging in, click **"Add New..."** → **"Project"**
2. You'll see your GitHub repositories
3. Find: **`saadh472/voice-automation-hub`**
4. Click **"Import"**

#### Step 3: Configure Frontend
1. **Project Name:** Keep default or change it
2. **Root Directory:** Click **"Edit"** and type: `frontend`
3. **Framework Preset:** Should auto-detect "Vite"
4. **Build Command:** Should be `npm run build` (auto-filled)
5. **Output Directory:** Should be `dist` (auto-filled)

#### Step 4: Add Environment Variable
1. Scroll down to **"Environment Variables"** section
2. Click **"Add"** or **"Add New"**
3. **Key:** `VITE_API_URL`
4. **Value:** Paste your Railway backend URL from Part 1, Step 5
   - Should look like: `https://voice-automation-backend-production.up.railway.app`
   - **Important:** Include `https://` at the start!
5. Click **"Add"**

#### Step 5: Deploy
1. Scroll to bottom
2. Click **"Deploy"** button
3. Wait 2-3 minutes for build to complete
4. You'll see: **"Congratulations! Your project has been deployed."**

#### Step 6: Get Your Frontend URL
1. After deployment, you'll see your project dashboard
2. Under **"Domains"**, you'll see your live URL
   - Looks like: `voice-automation-hub.vercel.app`
3. **Click the URL** to open your app!

✅ **Frontend is now live!** Your app is running on the internet!

---

## 🎉 You're Done!

### Your Live URLs:
- **Frontend:** `https://your-project.vercel.app` ← **This is your main app URL!**
- **Backend:** `https://your-backend.railway.app/api/health`
- **Database:** Automatically connected (no URL needed)

### Test Your App:
1. Open your frontend URL in browser
2. Try the voice commands
3. Everything should work!

---

## 🔄 Updating Your App

Whenever you push changes to GitHub:

### Railway (Backend):
- **Auto-deploys** automatically when you push to GitHub
- Just wait 2-3 minutes after pushing

### Vercel (Frontend):
- **Auto-deploys** automatically when you push to GitHub
- Just wait 1-2 minutes after pushing

**No manual steps needed!** Just push to GitHub and both will update.

---

## 🐛 Troubleshooting

### Backend not starting:
- Check Railway logs: Click service → "Deployments" → View logs
- Make sure Root Directory is set to `backend`
- Verify Build Command: `./mvnw clean package -DskipTests`

### Frontend can't connect:
- Check `VITE_API_URL` is set correctly in Vercel
- Make sure backend URL includes `https://`
- Verify backend is running (test `/api/health`)

### Database errors:
- Railway automatically sets `DATABASE_URL` - no action needed
- If errors, check Railway logs

### Build fails:
- Check build logs for error messages
- Make sure all files are pushed to GitHub
- Verify Java 11+ is available (Railway auto-provides)

---

## 📱 Share Your App

Once deployed, you can:
- Share your Vercel URL with anyone
- Add it to your portfolio
- Show it to your professor/classmates
- Use it from any device with internet!

---

## ✅ Quick Checklist

- [ ] Signed up on Railway
- [ ] Deployed backend from GitHub
- [ ] Set Root Directory to `backend`
- [ ] Added PostgreSQL database
- [ ] Copied backend URL
- [ ] Signed up on Vercel
- [ ] Imported project from GitHub
- [ ] Set Root Directory to `frontend`
- [ ] Added `VITE_API_URL` environment variable
- [ ] Deployed frontend
- [ ] Tested the app!

---

## 🎯 Summary

**Total Time:** ~20 minutes
**Cost:** FREE (both Railway and Vercel have free tiers)
**Difficulty:** Easy (just follow the steps)

**What You Get:**
- ✅ Live app on the internet
- ✅ Free database included
- ✅ Auto-deploy on every GitHub push
- ✅ Professional URLs
- ✅ SSL certificates (HTTPS) included

**Your app is now accessible from anywhere in the world! 🌍**

---

## 💡 Need Help?

If you get stuck:
1. Check the error messages in Railway/Vercel logs
2. Verify all settings match the guide above
3. Make sure you copied the backend URL correctly
4. Check that both services are "Deployed" (not "Building")

**You've got this! 🚀**

