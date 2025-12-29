# 🚂 Railway Deployment - Complete Step-by-Step Guide

Follow these exact steps to get your Voice Automation Hub running on Railway.

---

## 📋 Prerequisites Checklist

Before starting, make sure:
- ✅ Your code is pushed to GitHub: `saadh472/voice-automation-hub`
- ✅ You have a GitHub account
- ✅ You have internet connection

---

## 🎯 Step 1: Sign Up on Railway (2 minutes)

### 1.1 Go to Railway
1. Open your web browser
2. Go to: **https://railway.app**
3. You'll see the Railway homepage

### 1.2 Sign Up
1. Click the **"Start a New Project"** button (big green button) OR **"Login"** button (top right)
2. Click **"Login with GitHub"**
3. You'll be redirected to GitHub
4. Click **"Authorize Railway"** or **"Install & Authorize"**
5. You'll be redirected back to Railway
6. You should now see the Railway dashboard

---

## 🎯 Step 2: Create New Project (1 minute)

### 2.1 Start New Project
1. In Railway dashboard, click the **"+ New Project"** button (top right, green button)
2. A dropdown menu will appear
3. Click **"Deploy from GitHub repo"**

### 2.2 Select Your Repository
1. Railway will show a list of your GitHub repositories
2. Look for: **`saadh472/voice-automation-hub`**
3. If you don't see it:
   - Click **"Configure GitHub App"** or **"Install Railway on GitHub"**
   - Select your repositories (or all repositories)
   - Click **"Install"** or **"Save"**
   - Refresh the page
4. Click on **`saadh472/voice-automation-hub`**

### 2.3 Project Created
1. Railway will automatically start deploying
2. You'll see a new project appear (might be named "voice-automation-hub" or similar)
3. Wait a moment - Railway is setting up

---

## 🎯 Step 3: Configure Backend Service (5 minutes)

### 3.1 Open Service Settings
1. You'll see a service card (might be called "web" or "voice-automation-hub")
2. **Click on the service card** (the rectangular box)
3. You'll see the service details page

### 3.2 Go to Settings
1. Look at the top tabs: **"Metrics"**, **"Deployments"**, **"Settings"**, etc.
2. Click on **"Settings"** tab
3. You'll see various configuration options

### 3.3 Set Root Directory
1. Scroll down to find **"Source"** section
2. Look for **"Root Directory"** field
3. **This is probably empty or wrong - this is the main issue!**
4. Click in the **"Root Directory"** field
5. Type exactly: `backend`
6. Press Enter or click outside the field
7. Railway will auto-save (you might see a "Saved" message)

### 3.4 Set Build Command
1. Scroll down to **"Deploy"** section
2. Find **"Build Command"** field
3. Click in the field
4. Type exactly:
   ```
   ./mvnw clean package -DskipTests
   ```
5. Press Enter or click outside
6. Auto-saves automatically

### 3.5 Set Start Command
1. Still in **"Deploy"** section
2. Find **"Start Command"** field
3. Click in the field
4. Type exactly:
   ```
   java -jar target/*.jar
   ```
5. Press Enter or click outside
6. Auto-saves automatically

### 3.6 Verify Settings
Double-check these are set correctly:
- ✅ **Root Directory:** `backend`
- ✅ **Build Command:** `./mvnw clean package -DskipTests`
- ✅ **Start Command:** `java -jar target/*.jar`

---

## 🎯 Step 4: Wait for Deployment (3-5 minutes)

### 4.1 Check Deployment Status
1. After saving settings, Railway will **automatically redeploy**
2. Go to **"Deployments"** tab
3. You'll see a new deployment starting
4. Status will show: **"Building..."** → **"Deploying..."** → **"Active"**

### 4.2 Watch the Logs
1. While deploying, click on the deployment
2. Click **"View Logs"** or **"Logs"** button
3. You'll see the build process:
   - Downloading dependencies
   - Building with Maven
   - Starting Spring Boot
4. **Wait for:** `Started App in X.XXX seconds`
5. If you see errors, scroll to bottom to see what failed

### 4.3 Success Indicators
You'll know it worked when you see:
- ✅ Status: **"Active"** (green)
- ✅ Logs show: **"Started App"**
- ✅ No red error messages

---

## 🎯 Step 5: Get Your Backend URL (2 minutes)

### 5.1 Generate Public Domain
1. Go to **"Settings"** tab
2. Scroll to **"Networking"** section
3. Look for **"Public Domain"** or **"Generate Domain"**
4. If you see **"Generate Domain"** button, click it
5. Railway will create a URL like: `your-service-production.up.railway.app`
6. **Copy this URL** - you'll need it for frontend!

### 5.2 Test Your Backend
1. Open a new browser tab
2. Go to: `https://your-backend-url.railway.app/api/health`
3. You should see: `{"status":"UP"}` or similar
4. If it works, your backend is live! ✅

---

## 🎯 Step 6: Add Database (Optional but Recommended) (2 minutes)

### 6.1 Add PostgreSQL
1. Go back to your Railway project dashboard
2. Click **"+ New"** button (top right)
3. A dropdown appears
4. Click **"Database"**
5. Click **"Add PostgreSQL"**

### 6.2 Database Created
1. Railway will create a PostgreSQL database
2. It automatically sets `DATABASE_URL` environment variable
3. Your backend will automatically connect to it
4. **No configuration needed!** Railway does it all

### 6.3 Verify Database
1. You'll see a new service card for the database
2. Status should be **"Active"** (green)
3. That's it - database is ready!

---

## 🎯 Step 7: Deploy Frontend on Vercel (10 minutes)

### 7.1 Sign Up on Vercel
1. Open a new browser tab
2. Go to: **https://vercel.com**
3. Click **"Sign Up"** or **"Login"**
4. Click **"Continue with GitHub"**
5. Authorize Vercel

### 7.2 Import Project
1. Click **"Add New..."** → **"Project"**
2. Find: **`saadh472/voice-automation-hub`**
3. Click **"Import"**

### 7.3 Configure Frontend
1. **Project Name:** Keep default or change
2. **Root Directory:** Click **"Edit"** → Type: `frontend`
3. **Framework Preset:** Should auto-detect "Vite" ✅
4. **Build Command:** Should be `npm run build` ✅
5. **Output Directory:** Should be `dist` ✅

### 7.4 Add Environment Variable
1. Scroll to **"Environment Variables"** section
2. Click **"Add"** or **"Add New"**
3. **Key:** Type: `VITE_API_URL`
4. **Value:** Paste your Railway backend URL from Step 5
   - Should be: `https://your-backend-url.railway.app`
   - **Important:** Include `https://` at the start!
5. Click **"Add"** or **"Save"**

### 7.5 Deploy
1. Scroll to bottom
2. Click **"Deploy"** button (big blue button)
3. Wait 2-3 minutes for build
4. You'll see: **"Congratulations! Your project has been deployed."**

### 7.6 Get Frontend URL
1. After deployment, you'll see your project dashboard
2. Under **"Domains"**, you'll see your live URL
3. Example: `voice-automation-hub.vercel.app`
4. **Click the URL** to open your app!

---

## ✅ Step 8: Test Your Application

### 8.1 Open Your App
1. Go to your Vercel frontend URL
2. Your app should load!

### 8.2 Test Features
1. Try clicking the microphone button
2. Try typing a command
3. Check if backend is connected (should show "Online" status)

### 8.3 If Something Doesn't Work
- Check backend URL is correct in Vercel environment variables
- Verify backend is running (test `/api/health`)
- Check browser console for errors (F12)

---

## 🐛 Troubleshooting Common Issues

### Issue: Build Failed
**Solution:**
1. Check Root Directory is set to `backend`
2. Check Build Command: `./mvnw clean package -DskipTests`
3. View logs to see specific error

### Issue: Service Won't Start
**Solution:**
1. Check Start Command: `java -jar target/*.jar`
2. Check logs for Java errors
3. Verify Java version (Railway auto-provides Java 17)

### Issue: Frontend Can't Connect
**Solution:**
1. Verify `VITE_API_URL` is set in Vercel
2. Check URL includes `https://`
3. Test backend URL directly: `https://your-backend.railway.app/api/health`

### Issue: Database Connection Errors
**Solution:**
1. Railway automatically sets `DATABASE_URL`
2. If errors, check database service is "Active"
3. Restart backend service

---

## 📋 Complete Checklist

### Railway Backend:
- [ ] Signed up on Railway
- [ ] Created new project from GitHub
- [ ] Set Root Directory to `backend`
- [ ] Set Build Command: `./mvnw clean package -DskipTests`
- [ ] Set Start Command: `java -jar target/*.jar`
- [ ] Deployment succeeded (Status: Active)
- [ ] Got backend URL
- [ ] Added PostgreSQL database
- [ ] Tested backend: `/api/health` works

### Vercel Frontend:
- [ ] Signed up on Vercel
- [ ] Imported project from GitHub
- [ ] Set Root Directory to `frontend`
- [ ] Added environment variable: `VITE_API_URL`
- [ ] Set value to Railway backend URL
- [ ] Deployment succeeded
- [ ] Got frontend URL
- [ ] Tested app - everything works!

---

## 🎉 Success!

If you completed all steps:
- ✅ Your backend is running on Railway
- ✅ Your frontend is running on Vercel
- ✅ Database is connected
- ✅ Your app is live on the internet!

**Your app URLs:**
- **Frontend:** `https://your-project.vercel.app` ← **Main app**
- **Backend:** `https://your-backend.railway.app`
- **Health Check:** `https://your-backend.railway.app/api/health`

---

## 💡 Pro Tips

1. **Auto-Deploy:** Every time you push to GitHub, both Railway and Vercel auto-deploy
2. **Logs:** Always check logs if something fails
3. **Settings:** Most issues are fixed by correct Root Directory
4. **Database:** Railway auto-connects database - no manual setup needed

---

## 📞 Need Help?

If you get stuck:
1. Check the error message in logs
2. Verify all settings match this guide
3. Make sure Root Directory is `backend` (most common issue!)

**You've got this! Follow the steps one by one and your app will be live! 🚀**

