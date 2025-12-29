# Troubleshooting Connection Errors

## Common Issue: "Connection Error" in Browser

### Quick Fixes

1. **Wait Longer**
   - Backend takes 30-60 seconds to start
   - Frontend takes 10-20 seconds to start
   - **Don't close the server windows!**

2. **Check Server Windows**
   - Look for "Backend Server" window
   - Should show: "Started App" or "Tomcat started"
   - Look for "Frontend Server" window
   - Should show: "Local: http://localhost:3000"

3. **Refresh Browser**
   - Press F5 or Ctrl+R
   - Wait a few seconds after refresh

### Step-by-Step Diagnosis

#### Step 1: Check Backend
1. Look for "Backend Server" window (minimized)
2. Should see: "✅ Voice Automation Hub Started!"
3. Should see: "Backend: http://localhost:8080"
4. If you see errors, note them down

#### Step 2: Check Frontend
1. Look for "Frontend Server" window (minimized)
2. Should see: "Local: http://localhost:3000"
3. Should see: "ready in XXX ms"
4. If you see errors, note them down

#### Step 3: Test Manually
1. Open browser
2. Go to: `http://localhost:8080/api/devices`
3. Should see: `["living room light","bedroom light",...]`
4. If this works, backend is running!

5. Go to: `http://localhost:3000`
6. Should see the application
7. If you see "Cannot GET /", frontend is not running

### Common Errors

#### "ERR_CONNECTION_REFUSED"
- **Cause**: Server not started yet
- **Fix**: Wait 30-60 seconds, then refresh

#### "ERR_EMPTY_RESPONSE"
- **Cause**: Server crashed or not responding
- **Fix**: Check server windows for errors

#### "CORS Error"
- **Cause**: Backend not allowing frontend
- **Fix**: Should be fixed, but check backend window

#### "Cannot GET /"
- **Cause**: Frontend not running
- **Fix**: Check Frontend window, restart if needed

### Manual Start (If Launcher Fails)

#### Start Backend Manually:
```bash
cd backend
mvn spring-boot:run
```
Wait for: "Started App"

#### Start Frontend Manually (New Terminal):
```bash
cd frontend
npm install
npm run dev
```
Wait for: "Local: http://localhost:3000"

### Still Not Working?

1. **Check Ports**
   - Port 8080: Backend
   - Port 3000: Frontend
   - Make sure nothing else is using these ports

2. **Check Firewall**
   - Windows Firewall might be blocking
   - Allow Java and Node.js through firewall

3. **Restart Everything**
   - Close all server windows
   - Close browser
   - Run LAUNCH.bat again
   - Wait 60 seconds
   - Open browser manually

4. **Check Logs**
   - Backend window shows all errors
   - Frontend window shows all errors
   - Look for red error messages

### Quick Test Script

Run `check-servers.bat` to test if servers are running.

---

**Most Common Solution: Just wait 60 seconds and refresh the browser!**



