# 🔧 Fix "mvn: command not found" Error

## 🚨 The Problem

Railway's build environment doesn't have Maven installed by default. The error shows:
```
/bin/bash: line 1: mvn: command not found
```

## ✅ Solution: Use Maven Wrapper

Since we added the Unix `mvnw` file to GitHub, we should use it instead of `mvn`.

---

## 🎯 Fix in Railway Settings

### Step 1: Update Build Command
1. Go to Railway → Your service → **Settings**
2. Scroll to **"Deploy"** section
3. Change **Build Command** to:

```bash
cd backend && chmod +x mvnw && ./mvnw clean package -DskipTests
```

This:
- Makes `mvnw` executable
- Uses the Maven wrapper (which downloads Maven if needed)

### Step 2: Verify Start Command
**Start Command** should be:
```bash
cd backend && java -jar target/*.jar
```

### Step 3: Set Root Directory (Recommended)
1. Go to **"Source"** section
2. Set **Root Directory** to: `backend`
3. Then Build Command can be simpler:
   ```bash
   chmod +x mvnw && ./mvnw clean package -DskipTests
   ```

---

## ✅ Alternative: Use Nixpacks Configuration

I've also created `nixpacks.toml` which tells Railway to install Maven.

**Option 1: Use Maven Wrapper (Recommended)**
- Build Command: `cd backend && chmod +x mvnw && ./mvnw clean package -DskipTests`

**Option 2: Let Nixpacks Install Maven**
- The `nixpacks.toml` file will tell Railway to install Maven
- Then you can use: `cd backend && mvn clean package -DskipTests`

---

## 📋 Complete Railway Settings

### Recommended Configuration:

1. **Root Directory:** `backend` ✅
2. **Build Command:** `chmod +x mvnw && ./mvnw clean package -DskipTests`
3. **Start Command:** `java -jar target/*.jar`

### Or if Root Directory is empty:

1. **Root Directory:** (empty)
2. **Build Command:** `cd backend && chmod +x mvnw && ./mvnw clean package -DskipTests`
3. **Start Command:** `cd backend && java -jar target/*.jar`

---

## 🎯 Quick Fix Steps

1. **Railway** → Click your service
2. **Settings** tab
3. **Deploy** section:
   - **Build Command:** `cd backend && chmod +x mvnw && ./mvnw clean package -DskipTests`
4. **Save** (auto-saves)
5. **Redeploy** or wait for auto-redeploy
6. **Check** if build succeeds

---

## ✅ Why This Works

- The `mvnw` (Maven wrapper) file is now on GitHub
- It will download Maven automatically if needed
- It works on Linux/Unix (Railway's environment)
- More reliable than relying on Railway to have Maven pre-installed

---

## 🐛 Still Not Working?

If the wrapper still fails, try:

1. **Check if mvnw file exists:**
   - Verify `backend/mvnw` is in your GitHub repo
   - It should be there (we just added it)

2. **Use Nixpacks config:**
   - The `nixpacks.toml` file should install Maven
   - Then use: `cd backend && mvn clean package -DskipTests`

3. **Check Railway logs:**
   - Look for specific error messages
   - Share the error and I'll help fix it

---

## 🎉 Success!

After updating the Build Command to use `./mvnw`, Railway should:
1. Find the Maven wrapper
2. Make it executable
3. Run the build
4. Deploy successfully!

**Try the fix above and let me know if it works!** 🚀

