# 🔧 Fix Railway "mvnw: No such file or directory" Error

## 🚨 The Problem

Railway can't find or execute the Maven wrapper (`mvnw`). This happens because:
1. The file might not be executable on Linux
2. Railway might be looking in the wrong directory
3. The build command needs adjustment

## ✅ Solution 1: Fix Build Command in Railway Settings

### Step 1: Go to Railway Settings
1. Click on your service in Railway
2. Go to **"Settings"** tab
3. Scroll to **"Deploy"** section

### Step 2: Update Build Command
Change the **Build Command** to:

```bash
chmod +x backend/mvnw && cd backend && bash mvnw clean package -DskipTests
```

This:
- Makes mvnw executable (`chmod +x`)
- Changes to backend directory
- Uses `bash mvnw` instead of `./mvnw`

### Step 3: Verify Root Directory
Make sure **Root Directory** is set to: `backend`

### Step 4: Save and Redeploy
1. Settings auto-save
2. Railway will redeploy automatically
3. Wait for build to complete

---

## ✅ Solution 2: Use Maven Directly (Alternative)

If Solution 1 doesn't work, use Maven directly:

### Update Build Command:
```bash
cd backend && mvn clean package -DskipTests
```

Railway's Nixpacks should have Maven installed automatically.

---

## ✅ Solution 3: Set Root Directory Correctly

The most important setting:

1. Go to **Settings** → **Source**
2. Set **Root Directory** to: `backend`
3. This makes Railway work from the backend folder directly

Then update Build Command to:
```bash
./mvnw clean package -DskipTests
```

(No `cd backend` needed if root directory is set correctly)

---

## 🎯 Recommended Fix (Try This First)

### In Railway Settings:

1. **Root Directory:** `backend` ✅
2. **Build Command:** 
   ```
   chmod +x mvnw && bash mvnw clean package -DskipTests
   ```
3. **Start Command:**
   ```
   java -jar target/*.jar
   ```

Since Root Directory is `backend`, you don't need `cd backend` in the commands!

---

## 📋 Step-by-Step Fix

1. **Open Railway** → Click your service
2. **Settings** tab
3. **Source** section:
   - **Root Directory:** `backend` ✅
4. **Deploy** section:
   - **Build Command:** `chmod +x mvnw && bash mvnw clean package -DskipTests`
   - **Start Command:** `java -jar target/*.jar`
5. **Save** (auto-saves)
6. **Wait** for redeploy (2-3 minutes)
7. **Check** deployment status

---

## 🐛 Still Not Working?

### Check Build Logs:
1. Click on the failed deployment
2. Click "View Logs"
3. Look for specific error messages
4. Share the error and I'll help fix it

### Alternative: Use Maven Directly
If mvnw keeps failing, use:
```bash
mvn clean package -DskipTests
```

Railway should have Maven installed automatically.

---

## ✅ Quick Fix Summary

**Most Common Solution:**
1. Set **Root Directory** = `backend`
2. Set **Build Command** = `chmod +x mvnw && bash mvnw clean package -DskipTests`
3. Set **Start Command** = `java -jar target/*.jar`

**Try this and let me know if it works!** 🚀

