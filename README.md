# 🎤 Voice Automation Hub

**Case Study 5: Voice-Controlled Automation Hub**

A comprehensive, portable system that provides natural language control for home automation through voice commands, translating spoken language into device actions.

## 🎯 **PORTABLE & SELF-CONTAINED**

This project is **fully portable** - just extract the zip file and double-click `LAUNCH.bat`!

- ✅ **No Maven installation needed** - Maven wrapper included
- ✅ **Works from any location** - All paths are relative
- ✅ **Automatic dependency management** - Everything installs automatically
- ✅ **One-click launch** - Just double-click `LAUNCH.bat`

## 🏗️ Architectural Pattern

**INTERPRETER with SHARED REPOSITORY**

- **INTERPRETER**: Parses natural language commands, grammar tree for command interpretation, context-aware command resolution
- **SHARED REPOSITORY**: Central command history database, shared context between interpreters, user preference persistence

## 🎨 Design Patterns

1. **Interpreter Pattern** - Parses natural language commands into executable actions
2. **Composite Pattern** - Handles complex multi-device commands
3. **Visitor Pattern** - Executes commands on different device types
4. **Singleton Pattern** - Manages service instances (thread-safe)
5. **Repository Pattern** - Stores command history and user preferences

## 🚀 Quick Start

### 📥 Getting the Project

**From GitHub:**
```bash
git clone https://github.com/saadh472/voice-automation-hub.git
cd voice-automation-hub
```

**Or Download ZIP:**
1. Go to: https://github.com/saadh472/voice-automation-hub
2. Click "Code" → "Download ZIP"
3. Extract and open the folder

### Prerequisites

**Required:**
- **Java 11+** - [Download Oracle JDK](https://www.oracle.com/java/technologies/downloads/) or [OpenJDK](https://adoptium.net/)
- **Node.js 16+ (LTS recommended)** - [Download](https://nodejs.org/)
  - ⚠️ **Important**: Check "Add to PATH" during installation
  - ⚠️ **Important**: RESTART your computer after installing Node.js

**Not Required:**
- ❌ **Maven** - Included as wrapper (auto-downloads if needed)

### Launch Application

**Just double-click:** `LAUNCH.bat`

**Or see:** `HOW_TO_RUN.md` for detailed instructions

The launcher will:
- ✅ Check all prerequisites automatically
- ✅ Start backend server (port 8080)
- ✅ Start frontend server (port 3000)
- ✅ Install dependencies if needed
- ✅ Open browser automatically when ready

**First Run:**
- ⏱️ May take 2-3 minutes (installing dependencies)
- 📦 Downloads Maven wrapper if needed
- 📦 Installs Node.js packages

**Subsequent Runs:**
- ⏱️ Takes 30-60 seconds (servers starting)

## 📁 Project Structure

```
voice-automation-hub/
├── 🚀 LAUNCH.bat              ← START HERE! Double-click this
├── 📄 START_HERE.txt          ← Quick reference guide
├── 📖 README.md               ← This file (full documentation)
├── ❓ TROUBLESHOOTING.md       ← Help with common issues
│
├── backend/                   ← Java Spring Boot Backend
│   ├── mvnw.cmd               ← Maven wrapper (no Maven needed!)
│   ├── .mvn/                  ← Maven wrapper files
│   ├── pom.xml                ← Maven configuration
│   └── src/main/java/com/automation/voice/
│       └── App.java           ← All patterns implemented here
│
└── frontend/                  ← React TypeScript Frontend
    ├── package.json           ← Node.js dependencies
    ├── vite.config.ts         ← Vite configuration
    └── src/
        ├── App.tsx            ← Main React component
        └── App.css            ← Styles
```

## ✨ Features

### 🎙️ Voice Command Interface
- Simulated voice recognition
- Real-time waveform visualization
- Confidence scoring
- Alternative interpretations

### ⚡ Command Builder
- Type natural language commands
- Instant interpretation
- Alternative suggestions
- Example commands

### 🏠 Device Management
- View all available devices
- See command vocabulary for each device
- Device status indicators

### 📜 Command History
- View all executed commands
- See confidence scores
- View timestamps
- Provide feedback for ML training

## 🎮 Usage

### Voice Tab
1. Click "Start Listening"
2. Wait for simulated voice input
3. View interpreted command
4. See confidence and alternatives

### Builder Tab
1. Type a command (e.g., "Turn on the living room light")
2. Click "Execute" or press Enter
3. View results and alternatives

### Devices Tab
- Browse available devices
- See command vocabulary
- Understand device capabilities

### History Tab
- Review all executed commands
- See confidence scores
- Provide feedback (correct/incorrect)

## 🔧 Troubleshooting

### Common Issues

**"Java not found"**
- Install Java 11+ from [Oracle](https://www.oracle.com/java/technologies/downloads/) or [OpenJDK](https://adoptium.net/)
- Make sure Java is in your system PATH
- Or set JAVA_HOME environment variable

**"Node.js not found"**
- Install Node.js LTS from [nodejs.org](https://nodejs.org/)
- ⚠️ Check "Add to PATH" during installation
- ⚠️ RESTART your computer after installation
- Run `node --version` in command prompt to verify

**"Connection Error" in browser**
- Wait 60 seconds for servers to fully start
- Refresh browser (F5)
- Check Backend window for "Started App"
- Check Frontend window for "Local: http://localhost:3000"
- See `TROUBLESHOOTING.md` for detailed help

**"Port already in use"**
- Close other applications using ports 8080 or 3000
- Or change ports in configuration files
- Restart your computer if needed

**Servers not starting**
- Check the Backend and Frontend windows for error messages
- Make sure Java and Node.js are properly installed
- Try running `LAUNCH.bat` again

### Detailed Help

See `TROUBLESHOOTING.md` for:
- Step-by-step diagnosis
- Common error solutions
- Manual start instructions
- Port configuration

## 🛠️ Development

### Backend (Java Spring Boot)
```bash
cd backend
mvnw.cmd spring-boot:run
```

### Frontend (React TypeScript)
```bash
cd frontend
npm install
npm run dev
```

### Build for Production
```bash
# Backend
cd backend
mvnw.cmd clean package

# Frontend
cd frontend
npm run build
```

## 📚 Technical Details

### Backend Technologies
- **Java 11**
- **Spring Boot 2.7.0**
- **Maven** (wrapper included)
- **REST API**

### Frontend Technologies
- **React 18**
- **TypeScript 5**
- **Vite 5**
- **Axios** (HTTP client)

### API Endpoints
- `GET /api/devices` - List all devices
- `POST /api/interpret` - Interpret a command
- `POST /api/execute` - Execute a command
- `GET /api/history` - Get command history
- `GET /api/health` - Health check endpoint

## 🎓 Educational Value

This project demonstrates:
- **Architectural Patterns**: Interpreter, Shared Repository
- **Design Patterns**: Interpreter, Composite, Visitor, Singleton, Repository
- **Full-Stack Development**: Java backend + React frontend
- **REST API Design**: Clean API structure
- **Modern UI/UX**: Professional, responsive interface
- **Error Handling**: Comprehensive error handling and validation
- **Thread Safety**: Thread-safe implementations

## 📝 License

This project is created for educational purposes as part of a Software Design and Architecture course.

## 🤝 Contributing

This is an educational project. Feel free to:
- Study the code
- Modify and experiment
- Learn from the patterns

## 📞 Support

- **Quick Start**: See `START_HERE.txt`
- **Troubleshooting**: See `TROUBLESHOOTING.md`
- **Full Docs**: This README.md

---

**Ready to start? Double-click `LAUNCH.bat` now!** 🚀
