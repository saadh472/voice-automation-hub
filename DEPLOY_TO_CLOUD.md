# ☁️ Deploy Voice Automation Hub to Cloud

GitHub **cannot run applications directly** - it only hosts code. However, you can deploy your application to cloud services so it runs online.

## 🌐 Option 1: GitHub Codespaces (Run in Cloud IDE)

**Best for:** Testing and development in the cloud

### Setup:
1. Go to your repository: https://github.com/saadh472/voice-automation-hub
2. Click the green **"Code"** button
3. Select **"Codespaces"** tab
4. Click **"Create codespace on main"**
5. Wait for the cloud environment to start (2-3 minutes)

### Run in Codespaces:
```bash
# Backend
cd backend
./mvnw spring-boot:run

# Frontend (in new terminal)
cd frontend
npm install
npm run dev
```

**Access:** Codespaces will show you the URLs to access your running app.

---

## 🚀 Option 2: Deploy to Cloud Services (Recommended for Production)

### Frontend Deployment (React/Vite)

#### A. Vercel (Easiest - Recommended)
1. Go to: https://vercel.com
2. Sign up with GitHub
3. Click **"New Project"**
4. Import: `saadh472/voice-automation-hub`
5. **Root Directory**: `frontend`
6. **Build Command**: `npm run build`
7. **Output Directory**: `dist`
8. Click **"Deploy"**

**Result:** Your frontend will be live at: `https://your-project.vercel.app`

#### B. Netlify
1. Go to: https://netlify.com
2. Sign up with GitHub
3. Click **"Add new site"** → **"Import an existing project"**
4. Select your repository
5. **Base directory**: `frontend`
6. **Build command**: `npm run build`
7. **Publish directory**: `dist`
8. Click **"Deploy site"**

### Backend Deployment (Spring Boot)

#### A. Render (Recommended - Free Tier)
1. Go to: https://render.com
2. Sign up with GitHub
3. Click **"New"** → **"Web Service"**
4. Connect repository: `saadh472/voice-automation-hub`
5. **Name**: `voice-automation-hub-backend`
6. **Root Directory**: `backend`
7. **Environment**: `Java`
8. **Build Command**: `./mvnw clean package -DskipTests`
9. **Start Command**: `java -jar target/*.jar`
10. Click **"Create Web Service"**

**Result:** Your backend will be live at: `https://your-backend.onrender.com`

#### B. Railway
1. Go to: https://railway.app
2. Sign up with GitHub
3. Click **"New Project"** → **"Deploy from GitHub repo"**
4. Select your repository
5. **Root Directory**: `backend`
6. Railway auto-detects Java and builds
7. Your backend will be live automatically

#### C. Heroku
1. Go to: https://heroku.com
2. Sign up
3. Install Heroku CLI
4. Run:
   ```bash
   cd backend
   heroku create your-app-name
   git push heroku main
   ```

---

## 🔗 Option 3: Full-Stack Deployment (Both Together)

### Render (Full Stack)
1. Deploy **Backend** as Web Service (see above)
2. Deploy **Frontend** as Static Site:
   - **Build Command**: `cd frontend && npm install && npm run build`
   - **Publish Directory**: `frontend/dist`
3. Update frontend API URL to point to backend URL

### Update Frontend API URL

After deploying backend, update `frontend/src/App.tsx`:

```typescript
// Change from:
const API_URL = 'http://localhost:8080';

// To your backend URL:
const API_URL = 'https://your-backend.onrender.com';
```

Then redeploy frontend.

---

## 📋 Quick Deploy Checklist

### Frontend:
- [ ] Sign up on Vercel/Netlify
- [ ] Connect GitHub repository
- [ ] Set root directory: `frontend`
- [ ] Set build command: `npm run build`
- [ ] Set output: `dist`
- [ ] Deploy

### Backend:
- [ ] Sign up on Render/Railway
- [ ] Connect GitHub repository
- [ ] Set root directory: `backend`
- [ ] Set build command: `./mvnw clean package`
- [ ] Set start command: `java -jar target/*.jar`
- [ ] Deploy

### Connect Them:
- [ ] Update frontend API URL to backend URL
- [ ] Redeploy frontend
- [ ] Test the full application

---

## 🎯 Recommended Setup

**For Quick Testing:**
- Use **GitHub Codespaces** (free, runs in cloud IDE)

**For Production/Sharing:**
- **Frontend**: Vercel (free, fast, easy)
- **Backend**: Render (free tier available)

---

## 💡 Important Notes

1. **GitHub Pages** only works for static sites (frontend only, no backend)
2. Your app needs **both** frontend and backend running
3. After deploying backend, **update frontend API URL** to point to backend
4. Free tiers may have limitations (sleeping apps, rate limits)

---

## 🚀 Quick Start: Deploy to Vercel + Render

### Step 1: Deploy Backend (Render)
1. https://render.com → Sign up
2. New Web Service → Connect GitHub
3. Repository: `saadh472/voice-automation-hub`
4. Root: `backend`
5. Build: `./mvnw clean package`
6. Start: `java -jar target/*.jar`
7. Deploy

### Step 2: Deploy Frontend (Vercel)
1. https://vercel.com → Sign up
2. New Project → Import GitHub repo
3. Repository: `saadh472/voice-automation-hub`
4. Root: `frontend`
5. Build: `npm run build`
6. Output: `dist`
7. **Environment Variable**: Add `VITE_API_URL=https://your-backend.onrender.com`
8. Deploy

---

## 📚 Resources

- **Vercel Docs**: https://vercel.com/docs
- **Render Docs**: https://render.com/docs
- **Railway Docs**: https://docs.railway.app
- **GitHub Codespaces**: https://github.com/features/codespaces

---

**Your app will be live on the internet! 🌍**

