# 🚂 Railway Deployment - Ready to Deploy!

Your project is now **fully configured** for Railway deployment through GitHub!

## ✅ What's Been Updated on GitHub

1. ✅ **Unix Maven Wrapper** (`backend/mvnw`) - Added for Linux/Unix compatibility
2. ✅ **Railway Configuration** (`railway.json`) - Uses Maven directly (most reliable)
3. ✅ **All Files Committed** - Everything is on GitHub and ready

---

## 🚀 How to Deploy on Railway

### Step 1: Connect Railway to GitHub
1. Go to: https://railway.app
2. Sign up/Login with GitHub
3. Click **"+ New Project"**
4. Select **"Deploy from GitHub repo"**
5. Choose: `saadh472/voice-automation-hub`

### Step 2: Configure Settings (IMPORTANT!)

Railway will auto-detect your project, but you need to configure:

1. Click on your service
2. Go to **"Settings"** tab
3. **Source** section:
   - **Root Directory:** Set to `backend` ✅
4. **Deploy** section:
   - **Build Command:** `mvn clean package -DskipTests`
   - **Start Command:** `java -jar target/*.jar`

**OR** if Root Directory is empty:
- **Build Command:** `cd backend && mvn clean package -DskipTests`
- **Start Command:** `cd backend && java -jar target/*.jar`

### Step 3: Wait for Deployment
- Railway will build automatically
- Wait 3-5 minutes
- Check status: Should be **"Active"** (green)

### Step 4: Get Your URL
1. Go to **"Settings"** → **"Networking"**
2. Click **"Generate Domain"**
3. Copy your backend URL

---

## 📋 Configuration Options

### Option 1: Root Directory = `backend` (Recommended)
**Settings:**
- Root Directory: `backend`
- Build Command: `mvn clean package -DskipTests`
- Start Command: `java -jar target/*.jar`

### Option 2: Root Directory = empty
**Settings:**
- Root Directory: (empty)
- Build Command: `cd backend && mvn clean package -DskipTests`
- Start Command: `cd backend && java -jar target/*.jar`

---

## ✅ What's on GitHub Now

- ✅ `backend/mvnw` - Unix Maven wrapper (for Linux/Unix)
- ✅ `backend/mvnw.cmd` - Windows Maven wrapper
- ✅ `railway.json` - Railway configuration (uses Maven directly)
- ✅ All source code
- ✅ All configuration files

---

## 🎯 Quick Deploy Checklist

- [ ] Railway account created
- [ ] Connected to GitHub
- [ ] Selected `saadh472/voice-automation-hub` repository
- [ ] Set Root Directory to `backend`
- [ ] Set Build Command: `mvn clean package -DskipTests`
- [ ] Set Start Command: `java -jar target/*.jar`
- [ ] Deployment succeeded (Status: Active)
- [ ] Got backend URL
- [ ] Tested: `/api/health` works

---

## 🐛 Troubleshooting

### Build Fails
- Check Root Directory is set correctly
- Verify Build Command uses `mvn` (not `mvnw`)
- Check logs for specific errors

### Service Won't Start
- Verify Start Command: `java -jar target/*.jar`
- Check Java version (Railway auto-provides Java 17)

### Still Having Issues?
- Check Railway build logs
- Verify all files are on GitHub
- Make sure Root Directory is `backend`

---

## 🎉 Success!

Once deployed:
- ✅ Backend running on Railway
- ✅ Database can be added (Railway → + New → Database → PostgreSQL)
- ✅ Frontend can be deployed on Vercel
- ✅ Your app is live!

---

## 📚 Next Steps

1. **Deploy Backend on Railway** (this guide)
2. **Add PostgreSQL Database** (Railway → + New → Database)
3. **Deploy Frontend on Vercel** (see `QUICK_DEPLOY.md`)
4. **Set `VITE_API_URL`** to your Railway backend URL
5. **Test your app!**

---

**Your project is ready! Just connect Railway to GitHub and deploy! 🚀**

