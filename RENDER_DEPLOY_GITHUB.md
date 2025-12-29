# 🚀 Deploy to Render via GitHub (No API Key Needed)

## ✅ Quick Start - Deploy Without API Key

Render uses **GitHub OAuth** - no API key required!

---

## 📋 Step-by-Step Deployment

### Step 1: Sign Up on Render
1. Go to: **https://render.com**
2. Click **"Get Started for Free"**
3. Click **"Sign up with GitHub"**
4. Authorize Render to access your repositories
5. You're logged in!

### Step 2: Create Web Service (Backend)
1. Click **"New"** button (top right)
2. Select **"Web Service"**
3. You'll see your GitHub repositories
4. Find: **`saadh472/voice-automation-hub`**
5. Click **"Connect"** or select it

### Step 3: Configure Backend
1. **Name:** `voice-automation-backend` (or your choice)
2. **Region:** Choose closest to you
3. **Branch:** `main` (or `master`)
4. **Root Directory:** `backend`
5. **Environment:** `Java`
6. **Build Command:** `./mvnw clean package -DskipTests`
   - Or: `mvn clean package -DskipTests` (if Maven is available)
7. **Start Command:** `java -jar target/*.jar`

### Step 4: Add Environment Variables (Optional)
1. Scroll to **"Environment Variables"** section
2. If you have database:
   - **Key:** `DATABASE_URL`
   - **Value:** (your database connection string)
3. Click **"Add Environment Variable"**

### Step 5: Create Database (Optional)
1. Click **"New"** → **"PostgreSQL"**
2. **Name:** `voice-automation-db`
3. **Database:** `voiceautomation`
4. **User:** `voiceuser`
5. Click **"Create Database"**
6. Copy the **"Internal Database URL"**
7. Add it as `DATABASE_URL` in your backend service

### Step 6: Deploy
1. Scroll to bottom
2. Click **"Create Web Service"**
3. Wait 5-10 minutes for first build
4. Your backend will be live!

### Step 7: Get Your Backend URL
1. After deployment, you'll see your service dashboard
2. Under **"Service Details"**, you'll see your URL
3. Example: `voice-automation-backend.onrender.com`
4. **Copy this URL** - you'll need it for frontend!

---

## 🎨 Deploy Frontend (Static Site)

### Step 1: Create Static Site
1. Click **"New"** → **"Static Site"**
2. Connect: `saadh472/voice-automation-hub`

### Step 2: Configure Frontend
1. **Name:** `voice-automation-frontend`
2. **Root Directory:** `frontend`
3. **Build Command:** `npm install && npm run build`
4. **Publish Directory:** `dist`

### Step 3: Add Environment Variable
1. **Environment Variables** section
2. **Key:** `VITE_API_URL`
3. **Value:** Your backend URL from Step 7 above
   - Example: `https://voice-automation-backend.onrender.com`
4. Click **"Add"**

### Step 4: Deploy
1. Click **"Create Static Site"**
2. Wait 2-3 minutes
3. Your frontend will be live!

---

## 📋 Complete Configuration

### Backend Service:
- **Root Directory:** `backend`
- **Build Command:** `./mvnw clean package -DskipTests`
- **Start Command:** `java -jar target/*.jar`
- **Environment:** Java

### Frontend Static Site:
- **Root Directory:** `frontend`
- **Build Command:** `npm install && npm run build`
- **Publish Directory:** `dist`
- **Environment Variable:** `VITE_API_URL` = your backend URL

---

## ⚠️ Important Notes

### Free Tier Limitations:
- ⚠️ **Apps sleep after 15 minutes** of inactivity
- ⚠️ **First request after sleep:** Takes 30-60 seconds
- ⚠️ **Database:** Free for 90 days, then $7/month

### Build Time:
- **First build:** 5-10 minutes (downloading dependencies)
- **Subsequent builds:** 2-5 minutes

---

## 🐛 Troubleshooting

### Build Fails:
- Check Root Directory is `backend`
- Verify Build Command is correct
- Check build logs for errors

### App Won't Start:
- Verify Start Command: `java -jar target/*.jar`
- Check Java version (Render auto-provides)
- Check logs for errors

### Frontend 404:
- Verify Root Directory is `frontend`
- Check Publish Directory is `dist`
- Verify build completed successfully

---

## ✅ Deployment Checklist

- [ ] Signed up on Render with GitHub
- [ ] Created Web Service (backend)
- [ ] Set Root Directory to `backend`
- [ ] Set Build Command correctly
- [ ] Set Start Command correctly
- [ ] Backend deployed successfully
- [ ] Got backend URL
- [ ] Created Static Site (frontend)
- [ ] Set Root Directory to `frontend`
- [ ] Set `VITE_API_URL` environment variable
- [ ] Frontend deployed successfully
- [ ] Tested full application

---

## 🎉 Success!

After deployment:
- ✅ Backend: `https://your-backend.onrender.com`
- ✅ Frontend: `https://your-frontend.onrender.com`
- ✅ Your app is live!

**Note:** Free tier apps sleep after 15 minutes, so first request may be slow.

---

## 📚 Resources

- **Render Docs:** https://render.com/docs
- **Render Dashboard:** https://dashboard.render.com
- **Support:** https://render.com/docs/support

---

**No API key needed - just sign up with GitHub and deploy!** 🚀

