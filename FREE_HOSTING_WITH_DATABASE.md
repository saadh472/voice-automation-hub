# 🆓 Free Hosting Services with Database Support

## 🏆 Best Options for Your Project (Java Spring Boot + React)

### 1. **Render** ⭐ (Recommended)
**Website:** https://render.com

**Free Tier Includes:**
- ✅ Web Service (Backend) - Free
- ✅ PostgreSQL Database - Free (90 days, then $7/month)
- ✅ Static Site (Frontend) - Free
- ✅ Auto-deploy from GitHub
- ✅ SSL certificates included

**Limitations:**
- Apps sleep after 15 minutes of inactivity (free tier)
- Database free for 90 days, then paid

**Perfect for:** Full-stack apps with database

---

### 2. **Railway** ⭐ (Great for Java)
**Website:** https://railway.app

**Free Tier Includes:**
- ✅ $5 free credit monthly
- ✅ PostgreSQL, MySQL, MongoDB databases
- ✅ Auto-detects Java/Spring Boot
- ✅ Auto-deploy from GitHub
- ✅ SSL included

**Limitations:**
- $5 credit = ~500 hours/month
- Credit expires monthly

**Perfect for:** Java applications with databases

---

### 3. **Fly.io**
**Website:** https://fly.io

**Free Tier Includes:**
- ✅ PostgreSQL databases
- ✅ 3 shared-cpu VMs free
- ✅ 3GB persistent volumes
- ✅ 160GB outbound data transfer

**Limitations:**
- Limited resources on free tier

**Perfect for:** Apps needing persistent storage

---

### 4. **Supabase** (PostgreSQL + Backend)
**Website:** https://supabase.com

**Free Tier Includes:**
- ✅ PostgreSQL database (500MB)
- ✅ Authentication
- ✅ Real-time subscriptions
- ✅ Storage (1GB)
- ✅ API auto-generated

**Limitations:**
- 500MB database storage
- 2GB bandwidth/month

**Perfect for:** Apps needing database + auth

---

### 5. **PlanetScale** (MySQL)
**Website:** https://planetscale.com

**Free Tier Includes:**
- ✅ MySQL database (5GB storage)
- ✅ Branching (like Git for databases)
- ✅ Unlimited reads
- ✅ 1 billion row reads/month

**Limitations:**
- 1 database
- 5GB storage limit

**Perfect for:** MySQL-based applications

---

### 6. **MongoDB Atlas** (MongoDB)
**Website:** https://www.mongodb.com/cloud/atlas

**Free Tier Includes:**
- ✅ MongoDB database (512MB storage)
- ✅ Shared cluster
- ✅ 500MB storage

**Limitations:**
- 512MB storage
- Shared resources

**Perfect for:** NoSQL/MongoDB applications

---

### 7. **Neon** (PostgreSQL Serverless)
**Website:** https://neon.tech

**Free Tier Includes:**
- ✅ PostgreSQL database (3GB storage)
- ✅ Serverless (auto-scales)
- ✅ Branching support
- ✅ 5 projects

**Limitations:**
- 3GB storage
- Limited compute hours

**Perfect for:** Modern PostgreSQL apps

---

## 🎯 Recommended Setup for Your Project

### Option A: Render (Easiest)
1. **Backend + Database on Render:**
   - Deploy Spring Boot as Web Service
   - Add PostgreSQL database
   - Connect them automatically

2. **Frontend on Vercel:**
   - Deploy React app
   - Free and fast

**Total Cost:** FREE (database free for 90 days)

---

### Option B: Railway (Best for Java)
1. **Everything on Railway:**
   - Backend service
   - PostgreSQL database
   - Frontend static site
   - All connected automatically

**Total Cost:** FREE ($5 credit/month)

---

### Option C: Separate Services
1. **Backend:** Render or Railway
2. **Database:** Supabase or Neon (free PostgreSQL)
3. **Frontend:** Vercel or Netlify

**Total Cost:** FREE

---

## 📊 Comparison Table

| Service | Database Type | Free Storage | Best For |
|--------|--------------|--------------|----------|
| **Render** | PostgreSQL | 90 days free | Full-stack apps |
| **Railway** | PostgreSQL/MySQL/MongoDB | $5 credit/month | Java/Spring Boot |
| **Supabase** | PostgreSQL | 500MB | Apps with auth |
| **Neon** | PostgreSQL | 3GB | Serverless apps |
| **PlanetScale** | MySQL | 5GB | MySQL apps |
| **MongoDB Atlas** | MongoDB | 512MB | NoSQL apps |
| **Fly.io** | PostgreSQL | 3GB volumes | Persistent storage |

---

## 🚀 Quick Start: Render + PostgreSQL

### Step 1: Create Database
1. Go to: https://render.com
2. Sign up with GitHub
3. Click **"New"** → **"PostgreSQL"**
4. Name: `voice-automation-db`
5. Database: `voiceautomation`
6. User: `voiceuser`
7. Region: Choose closest
8. Click **"Create Database"**
9. **Copy the connection string** (you'll need it)

### Step 2: Deploy Backend
1. Click **"New"** → **"Web Service"**
2. Connect: `saadh472/voice-automation-hub`
3. **Root Directory:** `backend`
4. **Environment:** `Java`
5. **Build Command:** `./mvnw clean package -DskipTests`
6. **Start Command:** `java -jar target/*.jar`
7. **Add Environment Variable:**
   - Key: `DATABASE_URL`
   - Value: (paste connection string from Step 1)
8. Click **"Create Web Service"**

### Step 3: Deploy Frontend
1. Go to: https://vercel.com
2. Sign up with GitHub
3. **New Project** → Import `saadh472/voice-automation-hub`
4. **Root Directory:** `frontend`
5. **Build Command:** `npm run build`
6. **Output Directory:** `dist`
7. **Environment Variable:**
   - Key: `VITE_API_URL`
   - Value: `https://your-backend.onrender.com`
8. Click **"Deploy"**

---

## 💡 Adding Database to Your Project

Currently, your project uses in-memory storage. To add a database:

### 1. Add Database Dependencies

In `backend/pom.xml`, add:

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-data-jpa</artifactId>
</dependency>
<dependency>
    <groupId>org.postgresql</groupId>
    <artifactId>postgresql</artifactId>
    <scope>runtime</scope>
</dependency>
```

### 2. Update application.properties

In `backend/src/main/resources/application.properties`:

```properties
# Database Configuration
spring.datasource.url=${DATABASE_URL}
spring.datasource.username=${DB_USER}
spring.datasource.password=${DB_PASSWORD}
spring.jpa.hibernate.ddl-auto=update
spring.jpa.show-sql=true
```

### 3. Use Environment Variables

Render/Railway will automatically provide:
- `DATABASE_URL` - Full connection string
- Or separate: `DB_HOST`, `DB_USER`, `DB_PASSWORD`, `DB_NAME`

---

## 🎯 My Recommendation

**For Your Project:**

1. **Start with Railway** (easiest for Java):
   - Deploy backend + database together
   - $5 free credit monthly
   - Auto-detects Spring Boot

2. **Frontend on Vercel**:
   - Free, fast, easy
   - Auto-deploys from GitHub

**Total:** 100% FREE

---

## 📚 Resources

- **Render Docs**: https://render.com/docs
- **Railway Docs**: https://docs.railway.app
- **Supabase Docs**: https://supabase.com/docs
- **Neon Docs**: https://neon.tech/docs

---

## ✅ Quick Checklist

- [ ] Choose hosting service (Railway recommended)
- [ ] Create database
- [ ] Deploy backend
- [ ] Deploy frontend
- [ ] Connect frontend to backend URL
- [ ] Test the application

**Your app will be live with a database! 🎉**

