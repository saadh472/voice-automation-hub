# 🚀 How to Run This Project from GitHub

## 📥 Step 1: Clone the Repository

### Option A: Using Git (Recommended)

```bash
# Clone the repository
git clone https://github.com/saadh472/voice-automation-hub.git

# Navigate to the project folder
cd voice-automation-hub
```

### Option B: Download as ZIP

1. Go to: https://github.com/saadh472/voice-automation-hub
2. Click the green **"Code"** button
3. Select **"Download ZIP"**
4. Extract the ZIP file to your desired location
5. Open the extracted folder

---

## ✅ Step 2: Prerequisites

Make sure you have installed:

1. **Java 11+**
   - Download: [Oracle JDK](https://www.oracle.com/java/technologies/downloads/) or [OpenJDK](https://adoptium.net/)
   - Verify: `java -version`

2. **Node.js 16+ (LTS recommended)**
   - Download: [nodejs.org](https://nodejs.org/)
   - ⚠️ **Important**: Check "Add to PATH" during installation
   - ⚠️ **Important**: RESTART your computer after installing
   - Verify: `node --version`

---

## 🚀 Step 3: Launch the Application

### Windows (Easiest Method)

**Just double-click:** `LAUNCH.bat`

The launcher will automatically:
- ✅ Check prerequisites
- ✅ Install dependencies (if needed)
- ✅ Start backend server (port 8080)
- ✅ Start frontend server (port 3000)
- ✅ Open browser automatically

**First Run:**
- ⏱️ Takes 2-3 minutes (downloading dependencies)
- 📦 Maven wrapper downloads automatically
- 📦 Node.js packages install automatically

**Subsequent Runs:**
- ⏱️ Takes 30-60 seconds (servers starting)

---

## 🔧 Step 4: Manual Launch (Alternative)

If `LAUNCH.bat` doesn't work, you can start manually:

### Start Backend:

```bash
cd backend
mvnw.cmd spring-boot:run
```

Wait for: `Started App in X.XXX seconds`

### Start Frontend (in a new terminal):

```bash
cd frontend
npm install
npm run dev
```

Wait for: `Local: http://localhost:3000/`

### Open Browser:

Go to: **http://localhost:3000**

---

## 🌐 Access the Application

Once both servers are running:

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8080
- **Health Check**: http://localhost:8080/api/health

---

## 📋 Quick Checklist

- [ ] Cloned/downloaded repository from GitHub
- [ ] Java 11+ installed and verified
- [ ] Node.js 16+ installed and verified
- [ ] Double-clicked `LAUNCH.bat`
- [ ] Waited for servers to start
- [ ] Browser opened automatically (or go to http://localhost:3000)

---

## ❓ Troubleshooting

### "Java not found"
- Install Java 11+ from [Oracle](https://www.oracle.com/java/technologies/downloads/) or [OpenJDK](https://adoptium.net/)
- Make sure Java is in your system PATH
- Restart your computer after installation

### "Node.js not found"
- Install Node.js LTS from [nodejs.org](https://nodejs.org/)
- ⚠️ Check "Add to PATH" during installation
- ⚠️ RESTART your computer after installation
- Verify: `node --version` in command prompt

### "Port already in use"
- Close other applications using ports 8080 or 3000
- Or kill the processes:
  ```bash
  # For port 8080
  netstat -ano | findstr :8080
  taskkill /PID <PID> /F
  
  # For port 3000
  netstat -ano | findstr :3000
  taskkill /PID <PID> /F
  ```

### "Connection Error" in browser
- Wait 60 seconds for servers to fully start
- Refresh browser (F5)
- Check Backend window for "Started App"
- Check Frontend window for "Local: http://localhost:3000"

### Servers not starting
- Check the Backend and Frontend windows for error messages
- Make sure Java and Node.js are properly installed
- Try running `LAUNCH.bat` again
- See `TROUBLESHOOTING.md` for detailed help

---

## 📖 More Information

- **Quick Start**: See `START_HERE.txt`
- **Troubleshooting**: See `TROUBLESHOOTING.md`
- **Full Documentation**: See `README.md`

---

## 🎯 Summary

1. **Clone**: `git clone https://github.com/saadh472/voice-automation-hub.git`
2. **Navigate**: `cd voice-automation-hub`
3. **Launch**: Double-click `LAUNCH.bat`
4. **Wait**: 30-60 seconds for servers to start
5. **Use**: Browser opens automatically at http://localhost:3000

**That's it! Your Voice Automation Hub is running! 🎉**


