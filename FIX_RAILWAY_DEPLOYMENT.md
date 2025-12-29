# 🔧 Fix Railway Deployment - Build Failed

## 🚨 Your Build Failed - Here's How to Fix It

### Step 1: Check the Build Logs

1. In Railway, click on your **"web"** service
2. Click on the **"Deployments"** tab (or click the failed deployment)
3. Click **"View Logs"** or **"View Build Logs"**
4. **Scroll to the bottom** to see the error message
5. **Copy the error** - this tells us what went wrong

---

## 🔍 Common Issues & Fixes

### Issue 1: Root Directory Not Set

**Error:** "Cannot find pom.xml" or "No such file or directory"

**Fix:**
1. Click on your **"web"** service
2. Go to **"Settings"** tab
3. Scroll to **"Source"** section
4. Set **Root Directory:** `backend`
5. Click **"Save"**
6. Railway will redeploy automatically

---

### Issue 2: Maven Wrapper Not Executable

**Error:** "Permission denied" or "./mvnw: not found"

**Fix:**
1. Go to **"Settings"** → **"Deploy"**
2. Change **Build Command** to:
   ```
   chmod +x backend/mvnw && cd backend && ./mvnw clean package -DskipTests
   ```
3. Or use:
   ```
   cd backend && bash mvnw clean package -DskipTests
   ```

---

### Issue 3: Java Version Issues

**Error:** "Java version" or "Unsupported class file version"

**Fix:**
1. Go to **"Settings"** → **"Variables"**
2. Add environment variable:
   - **Key:** `JAVA_VERSION`
   - **Value:** `17`
3. Or Railway should auto-detect Java 17

---

### Issue 4: Build Command Wrong

**Error:** "Command not found" or build fails

**Fix:**
1. Go to **"Settings"** → **"Deploy"**
2. Set **Build Command:**
   ```
   cd backend && ./mvnw clean package -DskipTests
   ```
3. Set **Start Command:**
   ```
   cd backend && java -jar target/*.jar
   ```

---

## ✅ Correct Railway Configuration

### Settings Tab:
- **Root Directory:** `backend`
- **Build Command:** `./mvnw clean package -DskipTests`
- **Start Command:** `java -jar target/*.jar`

### Or Alternative (if wrapper issues):
- **Build Command:** `cd backend && bash mvnw clean package -DskipTests`
- **Start Command:** `cd backend && java -jar target/*.jar`

---

## 🔄 Redeploy After Fixing

1. After changing settings, Railway will **auto-redeploy**
2. Or click **"Redeploy"** button manually
3. Watch the logs to see if it works

---

## 📋 Step-by-Step Fix (Most Common)

### If Root Directory is Wrong:

1. Click **"web"** service
2. Click **"Settings"** tab
3. Find **"Source"** section
4. Change **Root Directory** from empty to: `backend`
5. Click **"Save"** (or it auto-saves)
6. Wait for automatic redeploy
7. Check if build succeeds

---

## 🐛 Still Not Working?

### Check Build Logs:

1. Click on failed deployment
2. Click **"View Logs"**
3. Look for error messages like:
   - "No such file or directory" → Root directory wrong
   - "Permission denied" → Maven wrapper issue
   - "Cannot find pom.xml" → Root directory wrong
   - "Java version" → Java version issue

### Share the Error:

Copy the last 20-30 lines of the build log and I can help you fix it!

---

## ✅ Quick Checklist

- [ ] Root Directory set to `backend`
- [ ] Build Command: `./mvnw clean package -DskipTests`
- [ ] Start Command: `java -jar target/*.jar`
- [ ] Checked build logs for specific error
- [ ] Redeployed after fixing settings

---

## 💡 Pro Tip

**Most common issue:** Root Directory not set to `backend`

Railway tries to build from the root, but your `pom.xml` is in the `backend` folder!

**Fix:** Set Root Directory to `backend` in Settings → Source

---

**Try fixing the Root Directory first - that's usually the problem!** 🚀

