package com.automation.voice;

import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.concurrent.ConcurrentHashMap;
import java.util.stream.Collectors;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

/**
 * Voice Automation Hub - Case Study 5
 * Architectural Pattern: INTERPRETER with SHARED REPOSITORY
 * Design Patterns: Interpreter, Composite, Visitor, Singleton
 * 
 * Robust implementation with comprehensive error handling and validation
 */
@SpringBootApplication
@RestController
@CrossOrigin(origins = "*")
public class App {
    
    private static final Set<String> VALID_DEVICES = Collections.unmodifiableSet(new HashSet<>(Arrays.asList(
        "living room light", "bedroom light", "kitchen light", "thermostat", "fan", "door lock"
    )));
    
    private static final Set<String> VALID_ACTIONS = Collections.unmodifiableSet(new HashSet<>(Arrays.asList(
        "ON", "OFF", "INCREASE", "DECREASE", "SET", "DIM", "BRIGHTEN", "LOCK", "UNLOCK"
    )));

    public static void main(String[] args) {
        try {
            SpringApplication.run(App.class, args);
            System.out.println("\n✅ Voice Automation Hub Started Successfully!");
            System.out.println("   Backend: http://localhost:8080");
            System.out.println("   Health: http://localhost:8080/api/health\n");
        } catch (Exception e) {
            System.err.println("❌ Failed to start application: " + e.getMessage());
            e.printStackTrace();
            System.exit(1);
        }
    }

    // ========== INTERPRETER PATTERN ==========
    interface CommandExpression {
        void interpret(VoiceCommandContext context) throws InterpretationException;
        double getConfidence();
        boolean isValid();
    }

    static class DeviceCommandExpression implements CommandExpression {
        private final String deviceName;
        private final String action;
        private final String parameter;
        private double confidence = 0.0;
        private boolean valid = false;

        DeviceCommandExpression(String device, String action, String param) {
            this.deviceName = (device != null) ? device.trim() : "unknown";
            this.action = (action != null) ? action.trim() : "UNKNOWN";
            this.parameter = (param != null && !param.trim().isEmpty()) ? param.trim() : null;
            this.valid = validate();
        }

        private boolean validate() {
            if (deviceName == null || deviceName.isEmpty() || deviceName.equals("unknown")) {
                return false;
            }
            if (action == null || action.isEmpty() || action.equals("UNKNOWN")) {
                return false;
            }
            return true;
        }

        public boolean isValid() {
            return valid;
        }

        public void interpret(VoiceCommandContext context) throws InterpretationException {
            if (context == null) {
                throw new InterpretationException("Context cannot be null");
            }
            if (!valid) {
                throw new InterpretationException("Invalid command: device=" + deviceName + ", action=" + action);
            }
            context.addInterpretedCommand(this);
            this.confidence = calculateConfidence(context);
            context.setConfidence(Math.max(context.getConfidence(), this.confidence));
        }

        public double getConfidence() {
            return confidence;
        }

        private double calculateConfidence(VoiceCommandContext context) {
            double base = 0.5; // Higher base confidence
            
            // Device validation (more weight)
            if (VALID_DEVICES.contains(deviceName)) {
                base += 0.35; // Valid device name
            } else if (context.getAvailableDevices().contains(deviceName)) {
                base += 0.25; // Device found in context
            } else {
                base -= 0.3; // Invalid device (heavier penalty)
            }
            
            // Action validation (more weight)
            if (VALID_ACTIONS.contains(action)) {
                base += 0.25; // Valid action
            } else {
                base -= 0.3; // Invalid action (heavier penalty)
            }
            
            // Bonus for complete commands
            if (deviceName != null && !deviceName.equals("unknown") && 
                action != null && !action.equals("UNKNOWN")) {
                base += 0.15; // Complete command
            }
            
            // Bonus for parameter presence (if applicable)
            if (parameter != null && !parameter.isEmpty()) {
                try {
                    int paramValue = Integer.parseInt(parameter);
                    // Validate parameter makes sense for the device/action
                    if (deviceName.contains("light") && paramValue >= 0 && paramValue <= 100) {
                        base += 0.1; // Valid brightness parameter
                    } else if (deviceName.equals("thermostat") && paramValue >= 60 && paramValue <= 85) {
                        base += 0.1; // Valid temperature parameter
                    }
                } catch (NumberFormatException e) {
                    // Invalid parameter format, no bonus
                }
            }
            
            // Penalty for unknown/UNKNOWN values
            if (deviceName.equals("unknown")) {
                base -= 0.4;
            }
            if (action.equals("UNKNOWN")) {
                base -= 0.4;
            }
            
            return Math.min(1.0, Math.max(0.0, base));
        }

        // Getters
        public String getDeviceName() { return deviceName; }
        public String getAction() { return action; }
        public String getParameter() { return parameter; }
    }

    // ========== COMPOSITE PATTERN ==========
    static class CompositeCommand implements CommandExpression {
        private final List<CommandExpression> commands = new ArrayList<>();
        private final String name;

        CompositeCommand(String name) {
            this.name = (name != null) ? name.trim() : "composite";
        }

        void add(CommandExpression cmd) {
            if (cmd != null) {
                commands.add(cmd);
            }
        }

        public void interpret(VoiceCommandContext context) throws InterpretationException {
            if (context == null) {
                throw new InterpretationException("Context cannot be null");
            }
            if (commands.isEmpty()) {
                throw new InterpretationException("Composite command '" + name + "' is empty");
            }
            for (CommandExpression cmd : commands) {
                cmd.interpret(context);
            }
        }

        public double getConfidence() {
            if (commands.isEmpty()) return 0.0;
            return commands.stream()
                .mapToDouble(CommandExpression::getConfidence)
                .average()
                .orElse(0.0);
        }

        public boolean isValid() {
            return !commands.isEmpty() && commands.stream().allMatch(CommandExpression::isValid);
        }

        public String getName() {
            return name;
        }
    }

    // ========== VISITOR PATTERN ==========
    interface CommandVisitor {
        ExecutionResult visit(DeviceCommandExpression command);
        ExecutionResult visit(SceneCommand command);
        ExecutionResult visit(RoutineCommand command);
    }

    static class CommandExecutorVisitor implements CommandVisitor {
        public ExecutionResult visit(DeviceCommandExpression cmd) {
            if (cmd == null || !cmd.isValid()) {
                return new ExecutionResult(false, "Invalid command cannot be executed");
            }
            try {
                String deviceName = cmd.getDeviceName();
                String action = cmd.getAction();
                DeviceState state = DeviceStateManager.getState(deviceName);
                
                // Simulate realistic device control
                String result;
                switch (action) {
                    case "ON":
                        state.setOn(true);
                        result = String.format("✅ %s turned ON successfully", deviceName);
                        break;
                    case "OFF":
                        state.setOn(false);
                        result = String.format("✅ %s turned OFF successfully", deviceName);
                        break;
                    case "INCREASE":
                        if (deviceName.contains("light")) {
                            int newBrightness = Math.min(100, state.getBrightness() + 20);
                            state.setBrightness(newBrightness);
                            result = String.format("✅ %s brightness increased to %d%%", deviceName, newBrightness);
                        } else if (deviceName.equals("thermostat")) {
                            int newTemp = Math.min(85, state.getTemperature() + 2);
                            state.setTemperature(newTemp);
                            result = String.format("✅ Thermostat temperature increased to %d°F", newTemp);
                        } else if (deviceName.equals("fan")) {
                            result = String.format("✅ %s speed increased", deviceName);
                        } else {
                            result = String.format("✅ %s increased", deviceName);
                        }
                        break;
                    case "DECREASE":
                        if (deviceName.contains("light")) {
                            int newBrightness = Math.max(0, state.getBrightness() - 20);
                            state.setBrightness(newBrightness);
                            result = String.format("✅ %s brightness decreased to %d%%", deviceName, newBrightness);
                        } else if (deviceName.equals("thermostat")) {
                            int newTemp = Math.max(60, state.getTemperature() - 2);
                            state.setTemperature(newTemp);
                            result = String.format("✅ Thermostat temperature decreased to %d°F", newTemp);
                        } else if (deviceName.equals("fan")) {
                            result = String.format("✅ %s speed decreased", deviceName);
                        } else {
                            result = String.format("✅ %s decreased", deviceName);
                        }
                        break;
                    case "DIM":
                        state.setBrightness(Math.max(0, state.getBrightness() - 30));
                        result = String.format("✅ %s dimmed to %d%% brightness", deviceName, state.getBrightness());
                        break;
                    case "BRIGHTEN":
                        state.setBrightness(Math.min(100, state.getBrightness() + 30));
                        result = String.format("✅ %s brightened to %d%% brightness", deviceName, state.getBrightness());
                        break;
                    case "SET":
                        if (cmd.getParameter() != null) {
                            try {
                                int value = Integer.parseInt(cmd.getParameter());
                                if (deviceName.equals("thermostat")) {
                                    state.setTemperature(value);
                                    result = String.format("✅ Thermostat set to %d°F", value);
                                } else if (deviceName.contains("light")) {
                                    state.setBrightness(value);
                                    result = String.format("✅ %s brightness set to %d%%", deviceName, value);
                                } else {
                                    result = String.format("✅ %s set to %s", deviceName, cmd.getParameter());
                                }
                            } catch (NumberFormatException e) {
                                result = String.format("✅ %s configured", deviceName);
                            }
                        } else {
                            result = String.format("✅ %s configured", deviceName);
                        }
                        break;
                    case "LOCK":
                        state.setOn(true);
                        result = String.format("✅ %s locked successfully", deviceName);
                        break;
                    case "UNLOCK":
                        state.setOn(false);
                        result = String.format("✅ %s unlocked successfully", deviceName);
                        break;
                    default:
                        result = String.format("✅ Command executed on %s", deviceName);
                }
                
                Repository.saveCommand(cmd);
                return new ExecutionResult(true, result);
            } catch (Exception e) {
                return new ExecutionResult(false, "Execution failed: " + e.getMessage());
            }
        }

        public ExecutionResult visit(SceneCommand scene) {
            if (scene == null || scene.getCommands().isEmpty()) {
                return new ExecutionResult(false, "Empty scene cannot be executed");
            }
            boolean allSuccess = true;
            List<String> results = new ArrayList<>();
            for (DeviceCommandExpression cmd : scene.getCommands()) {
                ExecutionResult r = visit(cmd);
                results.add(r.message);
                if (!r.success) allSuccess = false;
            }
            return new ExecutionResult(allSuccess, "Scene '" + scene.getSceneName() + "' executed: " + String.join(", ", results));
        }

        public ExecutionResult visit(RoutineCommand routine) {
            if (routine == null || routine.getSteps().isEmpty()) {
                return new ExecutionResult(false, "Empty routine cannot be executed");
            }
            boolean allSuccess = true;
            List<String> results = new ArrayList<>();
            for (CommandExpression step : routine.getSteps()) {
                if (step instanceof DeviceCommandExpression) {
                    ExecutionResult r = visit((DeviceCommandExpression) step);
                    results.add(r.message);
                    if (!r.success) allSuccess = false;
                }
            }
            return new ExecutionResult(allSuccess, "Routine executed: " + String.join(", ", results));
        }
    }

    static class ExecutionResult {
        final boolean success;
        final String message;
        final LocalDateTime timestamp;

        ExecutionResult(boolean success, String message) {
            this.success = success;
            this.message = (message != null) ? message : "No message";
            this.timestamp = LocalDateTime.now();
        }
    }

    // ========== SINGLETON PATTERN (Thread-Safe) ==========
    static class VoiceServiceManager {
        private static volatile VoiceServiceManager instance;
        
        private VoiceServiceManager() {
            // Private constructor to prevent instantiation
        }
        
        static VoiceServiceManager getInstance() {
            if (instance == null) {
                synchronized (VoiceServiceManager.class) {
                    if (instance == null) {
                        instance = new VoiceServiceManager();
                    }
                }
            }
            return instance;
        }
    }

    // ========== DEVICE STATE MANAGEMENT ==========
    static class DeviceState {
        private boolean isOn = false;
        private int brightness = 100; // 0-100
        private int temperature = 72; // For thermostat
        private String status = "OFF";
        
        DeviceState() {}
        
        boolean isOn() { return isOn; }
        void setOn(boolean on) { 
            this.isOn = on; 
            this.status = on ? "ON" : "OFF";
        }
        
        int getBrightness() { return brightness; }
        void setBrightness(int brightness) { 
            this.brightness = Math.max(0, Math.min(100, brightness)); 
        }
        
        int getTemperature() { return temperature; }
        void setTemperature(int temp) { 
            this.temperature = Math.max(60, Math.min(85, temp)); 
        }
        
        String getStatus() { return status; }
    }
    
    // Device State Manager (Thread-Safe)
    static class DeviceStateManager {
        private static final Map<String, DeviceState> deviceStates = new ConcurrentHashMap<>();
        
        static {
            // Initialize all devices to OFF state
            for (String device : VALID_DEVICES) {
                deviceStates.put(device, new DeviceState());
            }
        }
        
        static DeviceState getState(String deviceName) {
            return deviceStates.computeIfAbsent(deviceName, k -> new DeviceState());
        }
        
        static Map<String, Map<String, Object>> getAllStates() {
            Map<String, Map<String, Object>> states = new HashMap<>();
            for (Map.Entry<String, DeviceState> entry : deviceStates.entrySet()) {
                Map<String, Object> state = new HashMap<>();
                DeviceState ds = entry.getValue();
                state.put("isOn", ds.isOn());
                state.put("status", ds.getStatus());
                if (entry.getKey().contains("light")) {
                    state.put("brightness", ds.getBrightness());
                }
                if (entry.getKey().equals("thermostat")) {
                    state.put("temperature", ds.getTemperature());
                }
                states.put(entry.getKey(), state);
            }
            return states;
        }
    }

    // ========== SHARED REPOSITORY PATTERN (Thread-Safe) ==========
    static class Repository {
        private static final List<Map<String, Object>> commandHistory = Collections.synchronizedList(new ArrayList<>());
        private static final Map<String, List<String>> userPreferences = new ConcurrentHashMap<>();
        private static final int MAX_HISTORY_SIZE = 1000;
        private static String lastRawCommand = "";

        static void setLastRawCommand(String rawCmd) {
            lastRawCommand = (rawCmd != null) ? rawCmd : "";
        }

        static void saveCommand(DeviceCommandExpression cmd) {
            if (cmd == null) {
                return;
            }
            try {
                Map<String, Object> record = new HashMap<>();
                record.put("device", cmd.getDeviceName());
                record.put("action", cmd.getAction());
                record.put("parameter", cmd.getParameter() != null ? cmd.getParameter() : "");
                record.put("timestamp", LocalDateTime.now().toString());
                record.put("confidence", cmd.getConfidence());
                record.put("rawCommand", lastRawCommand);
                
                synchronized (commandHistory) {
                    commandHistory.add(record);
                    // Limit history size to prevent memory issues
                    if (commandHistory.size() > MAX_HISTORY_SIZE) {
                        commandHistory.remove(0);
                    }
                }
            } catch (Exception e) {
                System.err.println("Error saving command to history: " + e.getMessage());
            }
        }

        static List<Map<String, Object>> getHistory() {
            synchronized (commandHistory) {
                return new ArrayList<>(commandHistory);
            }
        }

        static void savePreference(String userId, String preference) {
            if (userId == null || preference == null) {
                return;
            }
            userPreferences.computeIfAbsent(userId, k -> Collections.synchronizedList(new ArrayList<>())).add(preference);
        }
        
        static int getHistorySize() {
            synchronized (commandHistory) {
                return commandHistory.size();
            }
        }
    }

    // ========== CONTEXT ==========
    static class VoiceCommandContext {
        private final List<DeviceCommandExpression> interpretedCommands = new ArrayList<>();
        private final Set<String> availableDevices = new HashSet<>();
        private double confidence = 0.0;
        private String rawCommand = "";

        void addInterpretedCommand(DeviceCommandExpression cmd) {
            if (cmd != null) {
                interpretedCommands.add(cmd);
            }
        }

        void addAvailableDevice(String device) {
            if (device != null && !device.trim().isEmpty()) {
                availableDevices.add(device.trim());
            }
        }

        void setConfidence(double conf) {
            this.confidence = Math.max(0.0, Math.min(1.0, conf));
        }

        void setRawCommand(String cmd) {
            this.rawCommand = (cmd != null) ? cmd : "";
        }

        double getConfidence() {
            return confidence;
        }

        List<DeviceCommandExpression> getInterpretedCommands() {
            return new ArrayList<>(interpretedCommands);
        }

        Set<String> getAvailableDevices() {
            return new HashSet<>(availableDevices);
        }
        
        String getRawCommand() {
            return rawCommand;
        }
    }

    // ========== COMMAND MODELS ==========
    static class SceneCommand {
        private final String sceneName;
        private final List<DeviceCommandExpression> commands = new ArrayList<>();
        
        SceneCommand(String name) {
            this.sceneName = (name != null) ? name.trim() : "unnamed";
        }
        
        String getSceneName() {
            return sceneName;
        }
        
        List<DeviceCommandExpression> getCommands() {
            return new ArrayList<>(commands);
        }
        
        void addCommand(DeviceCommandExpression cmd) {
            if (cmd != null) {
                commands.add(cmd);
            }
        }
    }

    static class RoutineCommand {
        private final String routineName;
        private final List<CommandExpression> steps = new ArrayList<>();
        
        RoutineCommand(String name) {
            this.routineName = (name != null) ? name.trim() : "unnamed";
        }
        
        String getRoutineName() {
            return routineName;
        }
        
        List<CommandExpression> getSteps() {
            return new ArrayList<>(steps);
        }
        
        void addStep(CommandExpression step) {
            if (step != null) {
                steps.add(step);
            }
        }
    }

    // ========== CUSTOM EXCEPTIONS ==========
    static class InterpretationException extends Exception {
        InterpretationException(String message) {
            super(message);
        }
    }

    // ========== API ENDPOINTS ==========
    @PostMapping("/api/interpret")
    public ResponseEntity<Map<String, Object>> interpret(@RequestBody Map<String, String> req) {
        try {
            // Input validation
            if (req == null) {
                return ResponseEntity.badRequest().body(createErrorResponse("Request body cannot be null"));
            }
            
            String commandText = req.get("command");
            if (commandText == null || commandText.trim().isEmpty()) {
                return ResponseEntity.badRequest().body(createErrorResponse("Command text is required"));
            }
            
            commandText = commandText.trim();
            if (commandText.length() > 500) {
                return ResponseEntity.badRequest().body(createErrorResponse("Command text too long (max 500 characters)"));
            }

            VoiceCommandContext context = new VoiceCommandContext();
            context.setRawCommand(commandText);
            
            // Add available devices
            for (String device : VALID_DEVICES) {
                context.addAvailableDevice(device);
            }

            // Parse command
            String lower = commandText.toLowerCase().trim();
            String device = parseDevice(lower);
            String action = parseAction(lower);
            String parameter = parseParameter(lower);

            // Log for debugging
            System.out.println("Interpretation: command='" + commandText + 
                             "', device='" + device + "', action='" + action + 
                             "', parameter='" + parameter + "'");

            DeviceCommandExpression cmd = new DeviceCommandExpression(device, action, parameter);
            
            if (!cmd.isValid()) {
                System.out.println("Invalid command: device='" + device + "', action='" + action + "'");
                
                // Check if it's a greeting or casual conversation
                String lowerCmd = commandText.toLowerCase().trim();
                if (isGreeting(lowerCmd)) {
                    return ResponseEntity.badRequest().body(createErrorResponse(
                        "Hello! 👋 I'm your Voice Automation Hub. " +
                        "I can help you control your smart home devices. " +
                        "Try saying: 'Turn on the living room light' or 'Set thermostat to 72 degrees'"));
                }
                
                // Check if it's a question
                if (isQuestion(lowerCmd)) {
                    return ResponseEntity.badRequest().body(createErrorResponse(
                        "I can help you control your devices! " +
                        "Try commands like: 'Turn on the bedroom light', 'Dim the kitchen light', or 'Set thermostat to 70'"));
                }
                
                // Generic helpful error message
                return ResponseEntity.badRequest().body(createErrorResponse(
                    "I didn't understand that command. " +
                    "I can control lights, thermostat, fan, and door lock. " +
                    "Try: 'Turn on the living room light', 'Set thermostat to 72', or 'Dim the bedroom light'"));
            }

            cmd.interpret(context);
            
            // Save raw command for history
            Repository.setLastRawCommand(commandText);

            // Generate alternatives
            List<String> alternatives = generateAlternatives(commandText, device, action);

            Map<String, Object> response = new HashMap<>();
            response.put("interpretedCommands", context.getInterpretedCommands().stream()
                .map(c -> {
                    Map<String, Object> cmdMap = new HashMap<>();
                    cmdMap.put("device", c.getDeviceName());
                    cmdMap.put("action", c.getAction());
                    cmdMap.put("parameter", c.getParameter() != null ? c.getParameter() : "");
                    return cmdMap;
                })
                .collect(Collectors.toList()));
            response.put("confidence", context.getConfidence());
            response.put("rawCommand", commandText);
            response.put("alternatives", alternatives);
            response.put("command", Map.of(
                "device", device,
                "action", action,
                "parameter", parameter != null ? parameter : ""
            ));
            response.put("success", true);

            return ResponseEntity.ok(response);
            
        } catch (InterpretationException e) {
            return ResponseEntity.badRequest().body(createErrorResponse("Interpretation error: " + e.getMessage()));
        } catch (Exception e) {
            System.err.println("Error in interpret endpoint: " + e.getMessage());
            e.printStackTrace();
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                .body(createErrorResponse("Internal server error: " + e.getMessage()));
        }
    }

    @PostMapping("/api/execute")
    public ResponseEntity<Map<String, Object>> execute(@RequestBody Map<String, String> cmd) {
        try {
            if (cmd == null) {
                return ResponseEntity.badRequest().body(createErrorResponse("Command cannot be null"));
            }
            
            String device = cmd.get("device");
            String action = cmd.get("action");
            String parameter = cmd.get("parameter");
            
            if (device == null || device.trim().isEmpty()) {
                return ResponseEntity.badRequest().body(createErrorResponse("Device is required"));
            }
            if (action == null || action.trim().isEmpty()) {
                return ResponseEntity.badRequest().body(createErrorResponse("Action is required"));
            }

            CommandExecutorVisitor visitor = new CommandExecutorVisitor();
            DeviceCommandExpression deviceCmd = new DeviceCommandExpression(
                device.trim(),
                action.trim(),
                parameter != null ? parameter.trim() : null
            );
            
            if (!deviceCmd.isValid()) {
                return ResponseEntity.badRequest().body(createErrorResponse("Invalid command"));
            }
            
            ExecutionResult result = visitor.visit(deviceCmd);
            
            // Get updated device state after execution
            DeviceState updatedState = DeviceStateManager.getState(device.trim());
            Map<String, Object> deviceState = new HashMap<>();
            deviceState.put("isOn", updatedState.isOn());
            deviceState.put("status", updatedState.getStatus());
            if (device.contains("light")) {
                deviceState.put("brightness", updatedState.getBrightness());
            }
            if (device.equals("thermostat")) {
                deviceState.put("temperature", updatedState.getTemperature());
            }
            
            Map<String, Object> response = new HashMap<>();
            response.put("status", result.success ? "success" : "failed");
            response.put("message", result.message);
            response.put("timestamp", result.timestamp.toString());
            response.put("success", result.success);
            response.put("deviceState", deviceState);
            
            if (result.success) {
                return ResponseEntity.ok(response);
            } else {
                return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(response);
            }
            
        } catch (Exception e) {
            System.err.println("Error in execute endpoint: " + e.getMessage());
            e.printStackTrace();
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                .body(createErrorResponse("Execution failed: " + e.getMessage()));
        }
    }

    @GetMapping("/api/devices")
    public ResponseEntity<Map<String, Object>> getDevices() {
        try {
            Map<String, Object> response = new HashMap<>();
            response.put("devices", new ArrayList<>(VALID_DEVICES));
            response.put("states", DeviceStateManager.getAllStates());
            return ResponseEntity.ok(response);
        } catch (Exception e) {
            System.err.println("Error in getDevices endpoint: " + e.getMessage());
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                .body(Map.of("devices", Collections.emptyList(), "states", Collections.emptyMap()));
        }
    }
    
    @GetMapping("/api/devices/{deviceName}/status")
    public ResponseEntity<Map<String, Object>> getDeviceStatus(@PathVariable String deviceName) {
        try {
            if (!VALID_DEVICES.contains(deviceName)) {
                return ResponseEntity.badRequest().body(createErrorResponse("Device not found: " + deviceName));
            }
            
            DeviceState state = DeviceStateManager.getState(deviceName);
            Map<String, Object> status = new HashMap<>();
            status.put("device", deviceName);
            status.put("isOn", state.isOn());
            status.put("status", state.getStatus());
            if (deviceName.contains("light")) {
                status.put("brightness", state.getBrightness());
            }
            if (deviceName.equals("thermostat")) {
                status.put("temperature", state.getTemperature());
            }
            status.put("timestamp", LocalDateTime.now().toString());
            
            return ResponseEntity.ok(status);
        } catch (Exception e) {
            System.err.println("Error in getDeviceStatus endpoint: " + e.getMessage());
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                .body(createErrorResponse("Failed to get device status: " + e.getMessage()));
        }
    }

    @GetMapping("/api/history")
    public ResponseEntity<List<Map<String, Object>>> getHistory() {
        try {
            return ResponseEntity.ok(Repository.getHistory());
        } catch (Exception e) {
            System.err.println("Error in getHistory endpoint: " + e.getMessage());
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(Collections.emptyList());
        }
    }

    @GetMapping("/api/health")
    public ResponseEntity<Map<String, Object>> health() {
        Map<String, Object> health = new HashMap<>();
        try {
            health.put("status", "UP");
            health.put("timestamp", LocalDateTime.now().toString());
            health.put("historySize", Repository.getHistorySize());
            health.put("version", "1.0");
            return ResponseEntity.ok(health);
        } catch (Exception e) {
            health.put("status", "DOWN");
            health.put("error", e.getMessage());
            return ResponseEntity.status(HttpStatus.SERVICE_UNAVAILABLE).body(health);
        }
    }

    @ExceptionHandler(Exception.class)
    public ResponseEntity<Map<String, Object>> handleException(Exception e) {
        System.err.println("Unhandled exception: " + e.getMessage());
        e.printStackTrace();
        return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
            .body(createErrorResponse("An unexpected error occurred: " + e.getMessage()));
    }

    // ========== HELPER METHODS ==========
    private Map<String, Object> createErrorResponse(String message) {
        Map<String, Object> error = new HashMap<>();
        error.put("success", false);
        error.put("error", message);
        error.put("timestamp", LocalDateTime.now().toString());
        return error;
    }

    private boolean isGreeting(String text) {
        if (text == null || text.isEmpty()) return false;
        String lower = text.toLowerCase().trim();
        String[] greetings = {
            "hi", "hello", "hey", "greetings", "good morning", "good afternoon", 
            "good evening", "good night", "howdy", "hi there", "hello there",
            "hey there", "what's up", "whats up", "sup", "yo"
        };
        for (String greeting : greetings) {
            if (lower.equals(greeting) || lower.startsWith(greeting + " ") || 
                lower.matches("^" + greeting + "[!.,?]*$")) {
                return true;
            }
        }
        return false;
    }

    private boolean isQuestion(String text) {
        if (text == null || text.isEmpty()) return false;
        String lower = text.toLowerCase().trim();
        // Check for question words or question marks
        if (lower.endsWith("?") || lower.endsWith("?")) {
            return true;
        }
        String[] questionWords = {
            "what", "how", "when", "where", "why", "who", "which", "can you",
            "could you", "would you", "will you", "do you", "does", "is", "are",
            "what can", "what does", "how do", "how can"
        };
        for (String qWord : questionWords) {
            if (lower.startsWith(qWord + " ") || lower.startsWith(qWord + "?")) {
                return true;
            }
        }
        return false;
    }

    private String parseDevice(String text) {
        if (text == null || text.isEmpty()) {
            return "unknown";
        }
        
        text = text.toLowerCase().trim();
        
        // Normalize text: remove filler words and normalize spacing
        text = text.replaceAll("\\b(the|a|an|my|your|this|that|please|can you|could you|would you)\\b", " ").trim();
        text = text.replaceAll("\\s+", " ");
        
        // Create a scoring system for better matching
        int[] scores = new int[6]; // One for each device
        String[] deviceNames = {
            "living room light",
            "bedroom light",
            "kitchen light",
            "door lock",
            "thermostat",
            "fan"
        };
        
        // Priority 1: Exact multi-word device matches (highest score)
        String[][] devicePatterns = {
            {"living room light", "livingroom light", "living-room light", "living room lights", 
             "living room's light", "livingroom's light", "living rooms light"},
            {"bedroom light", "bedroom lights", "bed room light", "bed room lights", 
             "bedroom's light", "bed rooms light"},
            {"kitchen light", "kitchen lights", "kitchen's light", "kitchens light"},
            {"door lock", "doorlock", "door lock", "door's lock", "doors lock"},
            {"thermostat", "thermo stat", "thermo-stat", "temperature control", "temp control", 
             "thermostat control", "climate control"},
            {"fan", "ceiling fan", "room fan", "the fan", "a fan"}
        };
        
        for (int i = 0; i < devicePatterns.length; i++) {
            for (String pattern : devicePatterns[i]) {
                // Exact phrase match (highest priority)
                if (text.matches(".*\\b" + pattern.replace(" ", "\\s+").replace("-", "[-\\s]") + "\\b.*")) {
                    scores[i] += 100;
                }
                // Contains match
                else if (text.contains(pattern)) {
                    scores[i] += 50;
                }
            }
        }
        
        // Priority 2: Room + light combinations (flexible word order, partial matches)
        String[] roomKeywords = {"living", "livingroom", "living-room", "lounge"};
        String[] bedroomKeywords = {"bedroom", "bed room", "bed-room", "bed", "master bedroom"};
        String[] kitchenKeywords = {"kitchen", "kitchens"};
        String[] lightKeywords = {"light", "lamp", "lights", "lamps", "bulb", "bulbs", "lamp light"};
        
        // Check for living room light
        boolean hasLivingRoom = false;
        for (String room : roomKeywords) {
            if (text.contains(room)) {
                hasLivingRoom = true;
                break;
            }
        }
        boolean hasLight = false;
        for (String light : lightKeywords) {
            if (text.contains(light)) {
                hasLight = true;
                break;
            }
        }
        if (hasLivingRoom && hasLight) {
            scores[0] += 80;
        }
        
        // Check for bedroom light
        boolean hasBedroom = false;
        for (String room : bedroomKeywords) {
            if (text.contains(room)) {
                hasBedroom = true;
                break;
            }
        }
        if (hasBedroom && hasLight) {
            scores[1] += 80;
        }
        
        // Check for kitchen light
        boolean hasKitchen = false;
        for (String room : kitchenKeywords) {
            if (text.contains(room)) {
                hasKitchen = true;
                break;
            }
        }
        if (hasKitchen && hasLight) {
            scores[2] += 80;
        }
        
        // Priority 3: Device-specific keywords with context
        // Thermostat detection
        if (text.contains("thermostat") || text.contains("thermo")) {
            scores[4] += 60;
        }
        if ((text.contains("temperature") || text.contains("temp") || text.contains("heat") || 
             text.contains("cool") || text.contains("ac") || text.contains("air conditioning")) &&
            (text.contains("set") || text.contains("change") || text.contains("adjust") || 
             text.contains("increase") || text.contains("decrease") || text.contains("turn") ||
             text.contains("make") || text.contains("to"))) {
            scores[4] += 50;
        }
        
        // Fan detection (with false positive prevention)
        if (text.contains("fan") && 
            !text.contains("fantastic") && !text.contains("fancy") && 
            !text.contains("fan of") && !text.contains("big fan")) {
            scores[5] += 60;
        }
        if (text.contains("ceiling fan") || text.contains("room fan")) {
            scores[5] += 40;
        }
        
        // Door lock detection
        if (text.contains("door") && text.contains("lock") && !text.contains("unlock")) {
            scores[3] += 70;
        }
        if (text.contains("doorlock") || text.contains("door-lock")) {
            scores[3] += 60;
        }
        
        // Priority 4: Generic light (if light/lamp mentioned without specific room)
        boolean hasRoom = hasLivingRoom || hasBedroom || hasKitchen || text.contains("room");
        if (hasLight && !hasRoom) {
            // Default to living room light but with lower score
            scores[0] += 30;
        }
        
        // Priority 5: Context-based inference
        // If action is light-related but no device specified
        if ((text.contains("bright") || text.contains("dim") || text.contains("brightness")) &&
            !hasRoom) {
            scores[0] += 20;
        }
        
        // Find the device with highest score
        int maxScore = 0;
        int maxIndex = -1;
        for (int i = 0; i < scores.length; i++) {
            if (scores[i] > maxScore) {
                maxScore = scores[i];
                maxIndex = i;
            }
        }
        
        // Only return device if score is above threshold (to avoid false positives)
        if (maxIndex >= 0 && maxScore >= 30) {
            return deviceNames[maxIndex];
        }
        
        return "unknown";
    }

    private String parseAction(String text) {
        if (text == null || text.isEmpty()) {
            return "UNKNOWN";
        }
        
        text = text.toLowerCase().trim();
        String[] words = text.split("\\s+");
        
        // Create scoring system for actions
        int onScore = 0, offScore = 0, lockScore = 0, unlockScore = 0;
        int brightenScore = 0, dimScore = 0, increaseScore = 0, decreaseScore = 0, setScore = 0;
        
        // Priority 1: Multi-word action phrases (most specific, highest score)
        String[][] onPatterns = {
            {"turn on", "switch on", "power on", "put on", "bring on", "get on"},
            {"enable", "activate", "start", "open", "wake up"},
            {"make on", "set on", "bring on", "get on"},
            {"turn it on", "switch it on", "power it on"}
        };
        
        String[][] offPatterns = {
            {"turn off", "switch off", "power off", "put off", "shut off", "get off"},
            {"disable", "deactivate", "stop", "close", "shut down"},
            {"make off", "set off", "turn it off", "switch it off"},
            {"power down", "shut down", "turn down"} // but not for brightness
        };
        
        for (String[] patterns : onPatterns) {
            for (String phrase : patterns) {
                if (text.contains(phrase)) {
                    onScore += 100;
                }
                // Also check with word boundaries for better matching
                if (text.matches(".*\\b" + phrase.replace(" ", "\\s+") + "\\b.*")) {
                    onScore += 50;
                }
            }
        }
        
        for (String[] patterns : offPatterns) {
            for (String phrase : patterns) {
                // Special handling for "turn down" - could be brightness or power
                if (phrase.equals("turn down") && (text.contains("brightness") || text.contains("light"))) {
                    dimScore += 50; // Prefer DIM over OFF for brightness context
                    continue;
                }
                if (text.contains(phrase)) {
                    offScore += 100;
                }
                if (text.matches(".*\\b" + phrase.replace(" ", "\\s+") + "\\b.*")) {
                    offScore += 50;
                }
            }
        }
        
        // Priority 2: Lock/Unlock actions (specific to door lock)
        if (text.contains("unlock") || text.matches(".*\\bun\\s+lock.*") || 
            text.contains("un lock") || text.contains("un-lock")) {
            unlockScore += 100;
        }
        if (text.contains("lock") && !text.contains("unlock") && 
            (text.contains("door") || text.contains("secure") || text.contains("lock the"))) {
            lockScore += 100;
        }
        
        // Priority 3: Brightness-specific actions (before generic increase/decrease)
        String[] brightenPatterns = {
            "brighten", "brighter", "make brighter", "more bright", "increase brightness",
            "brighten up", "make it brighter", "more brightness", "up the brightness",
            "brighten the", "increase the brightness"
        };
        for (String pattern : brightenPatterns) {
            if (text.contains(pattern)) {
                brightenScore += 80;
            }
        }
        
        String[] dimPatterns = {
            "dim", "dimmer", "less bright", "make dimmer", "decrease brightness",
            "dim down", "make it dimmer", "less brightness", "down the brightness",
            "dim the", "decrease the brightness", "lower the brightness"
        };
        for (String pattern : dimPatterns) {
            if (text.contains(pattern)) {
                dimScore += 80;
            }
        }
        
        // Priority 4: Increase/decrease actions (context-aware)
        boolean isLightContext = text.contains("light") || text.contains("brightness") || 
                                 text.contains("lamp") || text.contains("bulb");
        boolean isTempContext = text.contains("temperature") || text.contains("temp") || 
                               text.contains("heat") || text.contains("cool");
        
        String[] increasePatterns = {
            "increase", "raise", "higher", "turn up", "crank up", "go up",
            "make higher", "up", "boost", "amplify"
        };
        for (String pattern : increasePatterns) {
            if (text.contains(pattern)) {
                if (isLightContext && !isTempContext) {
                    brightenScore += 60; // Prefer BRIGHTEN for light context
                } else {
                    increaseScore += 50;
                }
            }
        }
        
        String[] decreasePatterns = {
            "decrease", "lower", "reduce", "turn down", "crank down", "go down",
            "make lower", "down", "reduce", "lessen"
        };
        for (String pattern : decreasePatterns) {
            if (text.contains(pattern)) {
                if (isLightContext && !isTempContext) {
                    dimScore += 60; // Prefer DIM for light context
                } else {
                    decreaseScore += 50;
                }
            }
        }
        
        // Priority 5: Set/change actions
        String[] setPatterns = {
            "set", "change", "adjust", "modify", "update", "make", "configure",
            "set to", "set at", "change to", "adjust to"
        };
        for (String pattern : setPatterns) {
            if (text.contains(pattern)) {
                setScore += 40;
            }
        }
        
        // Priority 6: Word order patterns (verb + on/off)
        for (int i = 0; i < words.length - 1; i++) {
            String currWord = words[i];
            String nextWord = words[i + 1];
            
            if (nextWord.equals("on")) {
                if (currWord.matches("turn|switch|put|bring|set|power|make|get")) {
                    onScore += 70;
                }
            }
            if (nextWord.equals("off")) {
                if (currWord.matches("turn|switch|put|shut|power|make|get")) {
                    offScore += 70;
                }
            }
        }
        
        // Priority 7: Standalone action words (with context validation)
        if (text.matches(".*\\bon\\b.*") && 
            !text.matches(".*\\b(turn|switch|put|bring|set|power|make|get)\\s+on\\b.*")) {
            if (text.contains("light") || text.contains("device") || text.contains("fan") ||
                text.contains("thermostat") || text.contains("lock") || text.contains("lamp")) {
                onScore += 30;
            }
        }
        if (text.matches(".*\\boff\\b.*") && 
            !text.matches(".*\\b(turn|switch|put|shut|power|make|get)\\s+off\\b.*")) {
            if (text.contains("light") || text.contains("device") || text.contains("fan") ||
                text.contains("thermostat") || text.contains("lock") || text.contains("lamp")) {
                offScore += 30;
            }
        }
        
        // Find action with highest score
        int maxScore = Math.max(Math.max(Math.max(Math.max(onScore, offScore), 
            Math.max(lockScore, unlockScore)), 
            Math.max(Math.max(brightenScore, dimScore), 
            Math.max(increaseScore, decreaseScore))), setScore);
        
        if (maxScore == 0) {
            return "UNKNOWN";
        }
        
        // Return action with highest score, with priority for specific actions
        if (unlockScore == maxScore) return "UNLOCK";
        if (lockScore == maxScore) return "LOCK";
        if (brightenScore == maxScore) return "BRIGHTEN";
        if (dimScore == maxScore) return "DIM";
        if (onScore == maxScore) return "ON";
        if (offScore == maxScore) return "OFF";
        if (increaseScore == maxScore) return "INCREASE";
        if (decreaseScore == maxScore) return "DECREASE";
        if (setScore == maxScore) return "SET";
        
        return "UNKNOWN";
    }

    private String parseParameter(String text) {
        if (text == null || text.isEmpty()) {
            return null;
        }
        try {
            String lowerText = text.toLowerCase();
            boolean isTempContext = lowerText.contains("temperature") || lowerText.contains("temp") || 
                                  lowerText.contains("heat") || lowerText.contains("cool") ||
                                  lowerText.contains("thermostat");
            boolean isBrightnessContext = lowerText.contains("brightness") || lowerText.contains("bright") ||
                                        lowerText.contains("dim") || lowerText.contains("light level");
            
            // Pattern 1: "set to 72", "set 72", "to 72", "at 72", "set temperature to 72"
            java.util.regex.Pattern pattern1 = java.util.regex.Pattern.compile(
                "(?:set|to|at|temperature|temp|brightness|level|make|change|adjust)\\s*(?:to|at|is|the)?\\s*(\\d{1,3})");
            java.util.regex.Matcher matcher1 = pattern1.matcher(lowerText);
            if (matcher1.find()) {
                String num = matcher1.group(1);
                int value = Integer.parseInt(num);
                
                if (isTempContext) {
                    // Temperature range: 60-85°F (reasonable home temperature)
                    if (value >= 60 && value <= 85) {
                        return num;
                    }
                } else if (isBrightnessContext) {
                    // Brightness range: 0-100%
                    if (value >= 0 && value <= 100) {
                        return num;
                    }
                } else {
                    // Generic number: infer from value range
                    if (value >= 60 && value <= 85) {
                        // Likely temperature
                        return num;
                    } else if (value >= 0 && value <= 100) {
                        // Could be brightness or percentage
                        return num;
                    }
                }
            }
            
            // Pattern 2: Numbers with units or context words nearby
            // "72 degrees", "72°", "72 percent", "72%", "level 72"
            java.util.regex.Pattern pattern2 = java.util.regex.Pattern.compile(
                "\\b(\\d{1,3})\\s*(?:degrees?|°|percent|%|percentile|level)");
            java.util.regex.Matcher matcher2 = pattern2.matcher(lowerText);
            if (matcher2.find()) {
                String num = matcher2.group(1);
                int value = Integer.parseInt(num);
                
                if (lowerText.contains("degree") || lowerText.contains("°")) {
                    if (value >= 60 && value <= 85) {
                        return num;
                    }
                } else if (lowerText.contains("percent") || lowerText.contains("%")) {
                    if (value >= 0 && value <= 100) {
                        return num;
                    }
                }
            }
            
            // Pattern 3: Numbers after action words
            // "increase to 75", "decrease to 50", "make it 72"
            java.util.regex.Pattern pattern3 = java.util.regex.Pattern.compile(
                "(?:increase|decrease|raise|lower|make|set|change|adjust)\\s+(?:to|it|the|at)?\\s*(\\d{1,3})");
            java.util.regex.Matcher matcher3 = pattern3.matcher(lowerText);
            if (matcher3.find()) {
                String num = matcher3.group(1);
                int value = Integer.parseInt(num);
                
                if (isTempContext) {
                    if (value >= 60 && value <= 85) {
                        return num;
                    }
                } else {
                    if (value >= 0 && value <= 100) {
                        return num;
                    }
                }
            }
            
            // Pattern 4: Standalone numbers (last resort, with validation)
            java.util.regex.Pattern pattern4 = java.util.regex.Pattern.compile("\\b(\\d{1,3})\\b");
            java.util.regex.Matcher matcher4 = pattern4.matcher(text);
            while (matcher4.find()) {
                String num = matcher4.group(1);
                int value = Integer.parseInt(num);
                
                // Validate reasonable ranges based on context
                if (isTempContext) {
                    if (value >= 60 && value <= 85) {
                        return num;
                    }
                } else if (isBrightnessContext) {
                    if (value >= 0 && value <= 100) {
                        return num;
                    }
                } else {
                    // Generic: accept reasonable values
                    if (value >= 0 && value <= 100) {
                        return num;
                    }
                }
            }
        } catch (Exception e) {
            // Ignore parsing errors
        }
        return null;
    }

    private List<String> generateAlternatives(String original, String device, String action) {
        List<String> alts = new ArrayList<>();
        if (original == null || device == null || action == null) {
            return alts;
        }
        
        if (action.equals("ON")) {
            alts.add("Switch on the " + device);
            alts.add("Enable the " + device);
            alts.add("Turn the " + device + " on");
            alts.add("Activate the " + device);
        } else if (action.equals("OFF")) {
            alts.add("Switch off the " + device);
            alts.add("Disable the " + device);
            alts.add("Turn the " + device + " off");
            alts.add("Deactivate the " + device);
        } else if (action.equals("INCREASE")) {
            alts.add("Raise the " + device);
            alts.add("Turn up the " + device);
        } else if (action.equals("DECREASE")) {
            alts.add("Lower the " + device);
            alts.add("Turn down the " + device);
        }
        
        return alts;
    }
}
