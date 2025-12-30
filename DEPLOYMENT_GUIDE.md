# 🚀 Full-Stack Deployment Guide

Complete guide to deploy your Voice Automation Hub on various platforms.

## 📋 Table of Contents

1. [Current Setup](#current-setup)
2. [Platform Options](#platform-options)
3. [Deployment Methods](#deployment-methods)
4. [Platform-Specific Guides](#platform-specific-guides)
5. [Environment Variables](#environment-variables)
6. [Database Setup](#database-setup)
7. [Troubleshooting](#troubleshooting)

---

## 🎯 Current Setup

**Your project is already configured for:**
- ✅ **Railway** (backend) - `railway.json`, `nixpacks.toml`
- ✅ **Netlify** (frontend) - `netlify.toml`
- ✅ **Vercel** (frontend) - `vercel.json`
- ✅ **Render** (full-stack) - `render.yaml`
- ✅ **Heroku** (backend) - `Procfile`

---

## 🌐 Platform Options

### **Free Tier Available:**

| Platform | Backend | Frontend | Database | Free Tier |
|----------|---------|----------|----------|-----------|
| **Railway** | ✅ | ✅ | ✅ PostgreSQL | $5/month credit |
| **Render** | ✅ | ✅ | ✅ PostgreSQL | Free (with limits) |
| **Netlify** | ❌ | ✅ | ❌ | Free |
| **Vercel** | ❌ | ✅ | ❌ | Free |
| **Fly.io** | ✅ | ✅ | ✅ PostgreSQL | Free (limited) |
| **Heroku** | ✅ | ✅ | ✅ PostgreSQL | ❌ (paid only) |
| **DigitalOcean App Platform** | ✅ | ✅ | ✅ PostgreSQL | $5/month |
| **AWS** | ✅ | ✅ | ✅ RDS | Free tier (12 months) |
| **Google Cloud** | ✅ | ✅ | ✅ Cloud SQL | Free tier (12 months) |
| **Azure** | ✅ | ✅ | ✅ SQL Database | Free tier (12 months) |

---

## 🔧 Deployment Methods

### **Method 1: GitHub Integration (Recommended)**
- Connect GitHub repository
- Auto-deploy on push
- Automatic builds
- Environment variables in dashboard

### **Method 2: CLI Deployment**
- Install platform CLI
- Deploy from terminal
- More control over process

### **Method 3: Docker**
- Containerize application
- Deploy anywhere
- Consistent environment

---

## 📦 Platform-Specific Guides

### 1. **Railway** (Backend + Database)

**Already configured!** ✅

**Steps:**
1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub
3. Click "New Project" → "Deploy from GitHub"
4. Select your repository
5. Railway auto-detects `railway.json`
6. Add PostgreSQL database:
   - Click "New" → "Database" → "PostgreSQL"
7. Set environment variables:
   - `DATABASE_URL` (auto-set from database)
   - `PORT=8080`
8. Get backend URL from dashboard
9. Use this URL in frontend `VITE_API_URL`

**Configuration files:**
- `railway.json` ✅
- `nixpacks.toml` ✅

---

### 2. **Render** (Full-Stack)

**Already configured!** ✅

**Steps:**
1. Go to [render.com](https://render.com)
2. Sign up with GitHub
3. Click "New" → "Blueprint"
4. Connect your GitHub repository
5. Render auto-detects `render.yaml`
6. Review configuration:
   - Backend service
   - Frontend service
   - PostgreSQL database
7. Click "Apply"
8. Wait for deployment (5-10 minutes)

**Configuration file:**
- `render.yaml` ✅

**Note:** Free tier spins down after 15 minutes of inactivity.

---

### 3. **Netlify** (Frontend)

**Already configured!** ✅

**Steps:**
1. Go to [netlify.com](https://netlify.com)
2. Sign up with GitHub
3. Click "Add new site" → "Import an existing project"
4. Select your repository
5. Configure:
   - **Base directory:** `frontend`
   - **Build command:** `npm install && npm run build`
   - **Publish directory:** `frontend/dist`
6. Add environment variable:
   - `VITE_API_URL` = Your backend URL
7. Click "Deploy site"

**Configuration file:**
- `netlify.toml` ✅

---

### 4. **Vercel** (Frontend)

**Already configured!** ✅

**Steps:**
1. Go to [vercel.com](https://vercel.com)
2. Sign up with GitHub
3. Click "Add New Project"
4. Import your repository
5. Configure:
   - **Framework Preset:** Vite
   - **Root Directory:** `frontend`
   - **Build Command:** `npm run build`
   - **Output Directory:** `dist`
6. Add environment variable:
   - `VITE_API_URL` = Your backend URL
7. Click "Deploy"

**Configuration file:**
- `vercel.json` ✅

---

### 5. **Fly.io** (Backend + Frontend)

**Steps:**
1. Install Fly CLI:
   ```bash
   # Windows (PowerShell)
   iwr https://fly.io/install.ps1 -useb | iex
   
   # Mac/Linux
   curl -L https://fly.io/install.sh | sh
   ```

2. Sign up:
   ```bash
   fly auth signup
   ```

3. **Deploy Backend:**
   ```bash
   cd backend
   fly launch
   ```
   - Follow prompts
   - Select region
   - Don't deploy yet

4. Create `fly.toml` in `backend/`:
   ```toml
   app = "your-backend-app-name"
   primary_region = "iad"
   
   [build]
     builder = "paketobuildpacks/builder:base"
   
   [http_service]
     internal_port = 8080
     force_https = true
     auto_stop_machines = true
     auto_start_machines = true
     min_machines_running = 0
   
   [[services]]
     internal_port = 8080
     protocol = "tcp"
   ```

5. Deploy:
   ```bash
   fly deploy
   ```

6. **Deploy Frontend:**
   ```bash
   cd frontend
   fly launch
   ```
   - Select "Static" app type
   - Build command: `npm install && npm run build`
   - Output directory: `dist`

7. Add PostgreSQL:
   ```bash
   fly postgres create
   fly postgres attach <database-name> -a <backend-app-name>
   ```

---

### 6. **DigitalOcean App Platform**

**Steps:**
1. Go to [cloud.digitalocean.com](https://cloud.digitalocean.com)
2. Sign up
3. Go to "App Platform" → "Create App"
4. Connect GitHub repository
5. **Configure Backend:**
   - Type: Web Service
   - Source: `backend/`
   - Build Command: `./mvnw clean package -DskipTests`
   - Run Command: `java -jar target/*.jar`
   - HTTP Port: `8080`
6. **Configure Frontend:**
   - Type: Static Site
   - Source: `frontend/`
   - Build Command: `npm install && npm run build`
   - Output Directory: `dist`
7. **Add Database:**
   - Click "Add Resource" → "Database" → "PostgreSQL"
8. Set environment variables
9. Deploy

**Cost:** ~$5/month minimum

---

### 7. **Heroku** (Backend)

**Already configured!** ✅

**Note:** Heroku removed free tier. Paid plans start at $7/month.

**Steps:**
1. Install Heroku CLI:
   ```bash
   # Download from: https://devcenter.heroku.com/articles/heroku-cli
   ```

2. Login:
   ```bash
   heroku login
   ```

3. Create app:
   ```bash
   cd backend
   heroku create your-app-name
   ```

4. Add PostgreSQL:
   ```bash
   heroku addons:create heroku-postgresql:mini
   ```

5. Set environment variables:
   ```bash
   heroku config:set PORT=8080
   ```

6. Deploy:
   ```bash
   git push heroku main
   ```

**Configuration file:**
- `Procfile` ✅

---

### 8. **AWS (Amazon Web Services)**

**Backend (Elastic Beanstalk):**
1. Install AWS CLI
2. Install EB CLI:
   ```bash
   pip install awsebcli
   ```
3. Initialize:
   ```bash
   cd backend
   eb init
   ```
4. Create environment:
   ```bash
   eb create voice-automation-env
   ```
5. Deploy:
   ```bash
   eb deploy
   ```

**Frontend (S3 + CloudFront):**
1. Build frontend:
   ```bash
   cd frontend
   npm run build
   ```
2. Create S3 bucket
3. Upload `dist/` contents
4. Enable static website hosting
5. Create CloudFront distribution

**Database (RDS):**
1. Create RDS PostgreSQL instance
2. Get connection string
3. Set in backend environment variables

**Cost:** Free tier for 12 months, then pay-as-you-go

---

### 9. **Google Cloud Platform**

**Backend (Cloud Run):**
1. Install Google Cloud SDK
2. Build container:
   ```bash
   cd backend
   gcloud builds submit --tag gcr.io/PROJECT-ID/backend
   ```
3. Deploy:
   ```bash
   gcloud run deploy backend --image gcr.io/PROJECT-ID/backend
   ```

**Frontend (Firebase Hosting):**
1. Install Firebase CLI:
   ```bash
   npm install -g firebase-tools
   ```
2. Login:
   ```bash
   firebase login
   ```
3. Initialize:
   ```bash
   cd frontend
   firebase init hosting
   ```
4. Build and deploy:
   ```bash
   npm run build
   firebase deploy
   ```

**Database (Cloud SQL):**
1. Create Cloud SQL PostgreSQL instance
2. Get connection string
3. Set in backend environment variables

**Cost:** Free tier for 12 months, then pay-as-you-go

---

### 10. **Microsoft Azure**

**Backend (App Service):**
1. Install Azure CLI
2. Create resource group:
   ```bash
   az group create --name voice-automation --location eastus
   ```
3. Create app service:
   ```bash
   az webapp create --resource-group voice-automation --plan myAppServicePlan --name your-app-name --runtime "JAVA:11-java11"
   ```
4. Deploy:
   ```bash
   cd backend
   az webapp deploy --resource-group voice-automation --name your-app-name --type jar --src-path target/*.jar
   ```

**Frontend (Static Web Apps):**
1. Create Static Web App:
   ```bash
   az staticwebapp create --name your-app-name --resource-group voice-automation --location eastus
   ```
2. Connect to GitHub
3. Set build settings:
   - App location: `frontend`
   - Output location: `dist`

**Database (Azure Database for PostgreSQL):**
1. Create PostgreSQL server
2. Get connection string
3. Set in backend environment variables

**Cost:** Free tier for 12 months, then pay-as-you-go

---

## 🔐 Environment Variables

### **Backend Variables:**

```bash
# Database
DATABASE_URL=postgresql://user:password@host:5432/dbname

# Server
PORT=8080
SERVER_PORT=8080

# CORS (if needed)
ALLOWED_ORIGINS=https://your-frontend-url.com
```

### **Frontend Variables:**

```bash
# Backend API URL
VITE_API_URL=https://your-backend-url.com

# Example:
VITE_API_URL=https://web-production-e10c.up.railway.app
```

**How to set:**
- **Railway:** Project → Variables tab
- **Render:** Environment → Environment Variables
- **Netlify:** Site settings → Environment variables
- **Vercel:** Project settings → Environment Variables

---

## 🗄️ Database Setup

### **PostgreSQL Connection String Format:**

```
postgresql://username:password@host:port/database
```

### **Local Development (H2):**
Your `application.properties` already configured:
```properties
spring.datasource.url=jdbc:h2:mem:testdb
spring.datasource.driverClassName=org.h2.Driver
```

### **Production (PostgreSQL):**
Platforms auto-provide `DATABASE_URL`. Your backend already configured to use it!

---

## 🔄 Deployment Workflow

### **Recommended Setup:**

1. **Backend + Database:**
   - Railway (easiest, $5/month credit)
   - OR Render (free, spins down)

2. **Frontend:**
   - Netlify (easiest, free)
   - OR Vercel (free, fast)

### **Complete Deployment Steps:**

1. **Deploy Backend:**
   - Choose platform (Railway recommended)
   - Connect GitHub
   - Add PostgreSQL database
   - Get backend URL

2. **Deploy Frontend:**
   - Choose platform (Netlify recommended)
   - Connect GitHub
   - Set `VITE_API_URL` to backend URL
   - Deploy

3. **Test:**
   - Visit frontend URL
   - Check browser console for errors
   - Test API endpoints

---

## 🐛 Troubleshooting

### **Backend Issues:**

**"Build failed"**
- Check build logs
- Ensure Java 11+ is available
- Verify `pom.xml` is correct

**"Port not found"**
- Set `PORT` environment variable
- Check platform port requirements

**"Database connection failed"**
- Verify `DATABASE_URL` is set
- Check database is running
- Verify credentials

### **Frontend Issues:**

**"404 on routes"**
- Add redirect rule: `/* /index.html 200`
- Check `netlify.toml` or `vercel.json`

**"Backend disconnected"**
- Verify `VITE_API_URL` is set correctly
- Check backend is running
- Verify CORS settings

**"Build failed"**
- Check Node.js version (18+)
- Verify `package.json` is correct
- Check build logs

### **CORS Issues:**

If frontend can't connect to backend, add to backend:

```java
@CrossOrigin(origins = {"https://your-frontend-url.com", "http://localhost:3000"})
```

---

## 📝 Quick Reference

### **Current Configuration Files:**

- ✅ `railway.json` - Railway backend config
- ✅ `nixpacks.toml` - Railway build config
- ✅ `netlify.toml` - Netlify frontend config
- ✅ `vercel.json` - Vercel frontend config
- ✅ `render.yaml` - Render full-stack config
- ✅ `Procfile` - Heroku backend config

### **Recommended Platforms:**

**For Beginners:**
1. Railway (backend) + Netlify (frontend)
2. Render (full-stack, one platform)

**For Production:**
1. AWS / Google Cloud / Azure
2. DigitalOcean App Platform

**For Free:**
1. Render (backend + frontend)
2. Netlify (frontend) + Railway free tier

---

## 🎯 Next Steps

1. **Choose your platform(s)**
2. **Deploy backend first** (get URL)
3. **Deploy frontend** (set `VITE_API_URL`)
4. **Test everything**
5. **Monitor and optimize**

---

## 📚 Additional Resources

- [Railway Docs](https://docs.railway.app)
- [Render Docs](https://render.com/docs)
- [Netlify Docs](https://docs.netlify.com)
- [Vercel Docs](https://vercel.com/docs)
- [Fly.io Docs](https://fly.io/docs)

---

**Need help?** Check your platform's documentation or create an issue on GitHub!

