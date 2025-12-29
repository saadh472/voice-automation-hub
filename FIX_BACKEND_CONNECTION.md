# 🔧 Fix "Disconnected" Backend Status

## 🚨 The Problem

Your frontend shows "Disconnected" because it can't reach your backend. This is usually because:
- `VITE_API_URL` environment variable is not set in Netlify
- `VITE_API_URL` is pointing to the wrong URL
- Backend URL is incorrect

## ✅ Solution: Set Environment Variable in Netlify

### Step 1: Get Your Backend URL

**If backend is on Railway:**
- Your URL: `https://web-production-e10c.up.railway.app`
- Or check Railway dashboard → Settings → Networking → Public Domain

**If backend is on Render:**
- Your URL: `https://your-backend.onrender.com`
- Check Render dashboard → Your service → URL

### Step 2: Add Environment Variable in Netlify

1. Go to your **Netlify dashboard**
2. Click on your site
3. Go to **"Site settings"** → **"Environment variables"**
4. Click **"Add variable"** or **"Add environment variable"**
5. **Key:** `VITE_API_URL`
6. **Value:** Your backend URL (include `https://`)
   - Example: `https://web-production-e10c.up.railway.app`
   - **Important:** Include `https://` at the start!
7. Click **"Save"**

### Step 3: Redeploy Frontend

1. Go to **"Deploys"** tab
2. Click **"Trigger deploy"** → **"Clear cache and deploy site"**
3. Wait 2-3 minutes
4. Your frontend will reconnect to backend!

---

## 🔍 Verify Backend is Running

### Test Backend Directly

1. Open a new browser tab
2. Go to: `https://your-backend-url/api/health`
3. You should see: `{"status":"UP"}`

**If you see this, backend is working!**

**If you get an error, backend might be down or URL is wrong.**

---

## 📋 Quick Fix Checklist

- [ ] Got backend URL from Railway/Render
- [ ] Added `VITE_API_URL` in Netlify environment variables
- [ ] Value includes `https://` at the start
- [ ] Redeployed frontend after adding variable
- [ ] Tested backend directly: `/api/health` works
- [ ] Frontend now shows "Online" instead of "Disconnected"

---

## 🎯 Common Issues

### Issue 1: Environment Variable Not Set
**Solution:** Add `VITE_API_URL` in Netlify → Environment variables

### Issue 2: Wrong Backend URL
**Solution:** 
- Check Railway/Render dashboard for correct URL
- Make sure it includes `https://`
- No trailing slash

### Issue 3: Backend is Down
**Solution:**
- Check Railway/Render dashboard
- Verify backend service is "Active"
- Check backend logs for errors

### Issue 4: CORS Error
**Solution:**
- Backend should already have CORS enabled
- If not, check backend CORS configuration

---

## ✅ Correct Environment Variable

**In Netlify:**
- **Key:** `VITE_API_URL`
- **Value:** `https://web-production-e10c.up.railway.app`
  - (Replace with your actual backend URL)

**Important:**
- ✅ Include `https://`
- ✅ No trailing slash
- ✅ Full URL (not just domain)

---

## 🎉 After Fixing

Once you:
1. Add `VITE_API_URL` in Netlify
2. Redeploy frontend
3. Wait for deployment

Your frontend should:
- ✅ Show "Online" status (green)
- ✅ Connect to backend
- ✅ Voice commands work
- ✅ All features work!

---

## 🐛 Still Disconnected?

### Check These:

1. **Backend URL:**
   - Test directly: `https://your-backend-url/api/health`
   - Should return: `{"status":"UP"}`

2. **Environment Variable:**
   - Check Netlify → Environment variables
   - Verify `VITE_API_URL` is set correctly
   - Value should be full URL with `https://`

3. **Redeploy:**
   - Must redeploy after adding environment variable
   - Clear cache when redeploying

4. **Backend Status:**
   - Check Railway/Render dashboard
   - Backend should be "Active"
   - Check logs for errors

---

## 📚 Quick Reference

**Railway Backend URL:**
- Format: `https://your-service-production.up.railway.app`
- Find in: Railway → Settings → Networking

**Render Backend URL:**
- Format: `https://your-service.onrender.com`
- Find in: Render → Your service → URL

**Netlify Environment Variable:**
- Key: `VITE_API_URL`
- Value: Your backend URL (with `https://`)

---

**Add the environment variable and redeploy - that should fix it!** 🚀

