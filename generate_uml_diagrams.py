#!/usr/bin/env python3
"""
UML Diagram Generator for Voice Automation Hub
Generates professional UML diagrams in PDF format
"""

import os
import subprocess
import sys

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import plantuml
        return True
    except ImportError:
        print("Installing required dependencies...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "plantuml", "reportlab"])
            return True
        except:
            print("ERROR: Could not install dependencies automatically.")
            print("Please install manually: pip install plantuml reportlab")
            return False

def create_class_diagram():
    """Create Class Diagram"""
    plantuml_code = """
@startuml Class_Diagram_Voice_Automation_Hub
!theme plain
skinparam classAttributeIconSize 0
skinparam shadowing false
skinparam linetype ortho

package "Voice Automation Hub" {
    
    class App {
        - VALID_DEVICES : Set<String>
        - VALID_ACTIONS : Set<String>
        + main(String[]) : void
        + interpret(Map) : ResponseEntity
        + execute(Map) : ResponseEntity
        + getDevices() : ResponseEntity
        + getHistory() : ResponseEntity
        + health() : ResponseEntity
        - parseDevice(String) : String
        - parseAction(String) : String
        - parseParameter(String) : String
        - generateAlternatives(String, String, String) : List<String>
    }
    
    interface CommandExpression {
        + interpret(VoiceCommandContext) : void
        + getConfidence() : double
        + isValid() : boolean
    }
    
    class DeviceCommandExpression {
        - deviceName : String
        - action : String
        - parameter : String
        - confidence : double
        - valid : boolean
        + interpret(VoiceCommandContext) : void
        + getConfidence() : double
        + isValid() : boolean
        + getDeviceName() : String
        + getAction() : String
        + getParameter() : String
        - validate() : boolean
        - calculateConfidence(VoiceCommandContext) : double
    }
    
    class CompositeCommand {
        - commands : List<CommandExpression>
        - name : String
        + add(CommandExpression) : void
        + interpret(VoiceCommandContext) : void
        + getConfidence() : double
        + isValid() : boolean
        + getName() : String
    }
    
    interface CommandVisitor {
        + visit(DeviceCommandExpression) : ExecutionResult
        + visit(SceneCommand) : ExecutionResult
        + visit(RoutineCommand) : ExecutionResult
    }
    
    class CommandExecutorVisitor {
        + visit(DeviceCommandExpression) : ExecutionResult
        + visit(SceneCommand) : ExecutionResult
        + visit(RoutineCommand) : ExecutionResult
    }
    
    class ExecutionResult {
        + success : boolean
        + message : String
        + timestamp : LocalDateTime
    }
    
    class VoiceServiceManager {
        - instance : VoiceServiceManager
        - {static} getInstance() : VoiceServiceManager
    }
    
    class DeviceState {
        - isOn : boolean
        - brightness : int
        - temperature : int
        - status : String
        + isOn() : boolean
        + setOn(boolean) : void
        + getBrightness() : int
        + setBrightness(int) : void
        + getTemperature() : int
        + setTemperature(int) : void
        + getStatus() : String
    }
    
    class DeviceStateManager {
        - {static} deviceStates : Map<String, DeviceState>
        + {static} getState(String) : DeviceState
        + {static} getAllStates() : Map<String, Map<String, Object>>
    }
    
    class Repository {
        - {static} commandHistory : List<Map<String, Object>>
        - {static} userPreferences : Map<String, List<String>>
        - {static} MAX_HISTORY_SIZE : int
        - {static} lastRawCommand : String
        + {static} saveCommand(DeviceCommandExpression) : void
        + {static} getHistory() : List<Map<String, Object>>
        + {static} savePreference(String, String) : void
        + {static} getHistorySize() : int
        + {static} setLastRawCommand(String) : void
    }
    
    class VoiceCommandContext {
        - interpretedCommands : List<DeviceCommandExpression>
        - availableDevices : Set<String>
        - confidence : double
        - rawCommand : String
        + addInterpretedCommand(DeviceCommandExpression) : void
        + addAvailableDevice(String) : void
        + setConfidence(double) : void
        + setRawCommand(String) : void
        + getConfidence() : double
        + getInterpretedCommands() : List<DeviceCommandExpression>
        + getAvailableDevices() : Set<String>
        + getRawCommand() : String
    }
    
    class SceneCommand {
        - sceneName : String
        - commands : List<DeviceCommandExpression>
        + getSceneName() : String
        + getCommands() : List<DeviceCommandExpression>
        + addCommand(DeviceCommandExpression) : void
    }
    
    class RoutineCommand {
        - routineName : String
        - steps : List<CommandExpression>
        + getRoutineName() : String
        + getSteps() : List<CommandExpression>
        + addStep(CommandExpression) : void
    }
    
    class InterpretationException {
        + InterpretationException(String)
    }
}

' Relationships
CommandExpression <|.. DeviceCommandExpression
CommandExpression <|.. CompositeCommand
CommandExpression <-- CompositeCommand : contains
CommandVisitor <|.. CommandExecutorVisitor
CommandExecutorVisitor ..> ExecutionResult : creates
CommandExecutorVisitor ..> DeviceStateManager : uses
CommandExecutorVisitor ..> Repository : uses
DeviceCommandExpression ..> VoiceCommandContext : uses
DeviceCommandExpression ..> InterpretationException : throws
SceneCommand *-- DeviceCommandExpression : contains
RoutineCommand *-- CommandExpression : contains
CommandExecutorVisitor ..> SceneCommand : visits
CommandExecutorVisitor ..> RoutineCommand : visits
DeviceStateManager *-- DeviceState : manages
App ..> CommandExpression : creates
App ..> CommandExecutorVisitor : uses
App ..> VoiceCommandContext : creates
App ..> Repository : uses
App ..> DeviceStateManager : uses

note right of CommandExpression
  **Interpreter Pattern**
  Defines grammar for commands
end note

note right of CompositeCommand
  **Composite Pattern**
  Groups multiple commands
end note

note right of CommandVisitor
  **Visitor Pattern**
  Executes commands on devices
end note

note right of VoiceServiceManager
  **Singleton Pattern**
  Thread-safe instance management
end note

note right of Repository
  **Repository Pattern**
  Shared command history storage
end note

@enduml
"""
    return plantuml_code

def create_sequence_interpretation():
    """Create Sequence Diagram for Command Interpretation"""
    plantuml_code = """
@startuml Sequence_Command_Interpretation
!theme plain
skinparam shadowing false
skinparam sequenceArrowThickness 2

actor User
participant "Frontend\n(React)" as Frontend
participant "App\n(REST Controller)" as App
participant "VoiceCommandContext" as Context
participant "DeviceCommandExpression" as Expression
participant "Repository" as Repo

User -> Frontend: Enter voice command
activate Frontend

Frontend -> App: POST /api/interpret\n{"command": "turn on living room light"}
activate App

App -> App: parseDevice(command)
App -> App: parseAction(command)
App -> App: parseParameter(command)

App -> Context: new VoiceCommandContext()
activate Context
App -> Context: setRawCommand(command)
App -> Context: addAvailableDevice(devices)

App -> Expression: new DeviceCommandExpression\n(device, action, parameter)
activate Expression

Expression -> Expression: validate()
Expression -> Context: interpret(context)
Expression -> Expression: calculateConfidence(context)
Expression -> Context: addInterpretedCommand(this)
Expression -> Context: setConfidence(confidence)

deactivate Expression

App -> Repo: setLastRawCommand(command)
activate Repo
deactivate Repo

App -> App: generateAlternatives(command)
App -> Frontend: ResponseEntity\n{interpretedCommands, confidence, alternatives}
deactivate App
deactivate Context

Frontend -> User: Display interpretation\nwith confidence score
deactivate Frontend

@enduml
"""
    return plantuml_code

def create_sequence_execution():
    """Create Sequence Diagram for Command Execution"""
    plantuml_code = """
@startuml Sequence_Command_Execution
!theme plain
skinparam shadowing false
skinparam sequenceArrowThickness 2

actor User
participant "Frontend\n(React)" as Frontend
participant "App\n(REST Controller)" as App
participant "CommandExecutorVisitor" as Visitor
participant "DeviceStateManager" as StateMgr
participant "DeviceState" as State
participant "Repository" as Repo

User -> Frontend: Execute command
activate Frontend

Frontend -> App: POST /api/execute\n{device, action, parameter}
activate App

App -> App: Validate command
App -> App: new DeviceCommandExpression\n(device, action, parameter)

App -> Visitor: new CommandExecutorVisitor()
activate Visitor

App -> Visitor: visit(deviceCommand)
activate Visitor

Visitor -> Visitor: validate command

alt Valid Command
    Visitor -> StateMgr: getState(deviceName)
    activate StateMgr
    StateMgr -> State: get/create DeviceState
    activate State
    deactivate StateMgr
    
    alt Action: ON
        Visitor -> State: setOn(true)
        State -> State: status = "ON"
    else Action: OFF
        Visitor -> State: setOn(false)
        State -> State: status = "OFF"
    else Action: INCREASE/DECREASE
        Visitor -> State: setBrightness(value)
        Visitor -> State: setTemperature(value)
    else Action: SET
        Visitor -> State: setBrightness(parameter)
        Visitor -> State: setTemperature(parameter)
    end
    
    Visitor -> Repo: saveCommand(command)
    activate Repo
    Repo -> Repo: Add to commandHistory
    deactivate Repo
    
    Visitor -> StateMgr: getState(deviceName)
    activate StateMgr
    StateMgr -> State: get updated state
    deactivate StateMgr
    deactivate State
    
    Visitor -> App: ExecutionResult(success, message)
else Invalid Command
    Visitor -> App: ExecutionResult(false, "Invalid command")
end

deactivate Visitor

App -> Frontend: ResponseEntity\n{status, message, deviceState}
deactivate App

Frontend -> User: Display execution result
deactivate Frontend

@enduml
"""
    return plantuml_code

def create_sequence_composite():
    """Create Sequence Diagram for Composite Command Execution"""
    plantuml_code = """
@startuml Sequence_Composite_Command_Execution
!theme plain
skinparam shadowing false
skinparam sequenceArrowThickness 2

actor User
participant "App" as App
participant "CompositeCommand" as Composite
participant "DeviceCommandExpression" as DeviceCmd1
participant "DeviceCommandExpression" as DeviceCmd2
participant "CommandExecutorVisitor" as Visitor
participant "DeviceStateManager" as StateMgr
participant "Repository" as Repo

User -> App: Execute composite command\n"Turn on all lights"
activate App

App -> Composite: new CompositeCommand("all lights")
activate Composite

App -> DeviceCmd1: new DeviceCommandExpression\n("living room light", "ON")
activate DeviceCmd1
App -> Composite: add(deviceCmd1)
deactivate DeviceCmd1

App -> DeviceCmd2: new DeviceCommandExpression\n("bedroom light", "ON")
activate DeviceCmd2
App -> Composite: add(deviceCmd2)
deactivate DeviceCmd2

App -> Composite: interpret(context)
activate Composite

loop For each command
    Composite -> DeviceCmd1: interpret(context)
    activate DeviceCmd1
    DeviceCmd1 -> DeviceCmd1: calculateConfidence()
    deactivate DeviceCmd1
    
    Composite -> DeviceCmd2: interpret(context)
    activate DeviceCmd2
    DeviceCmd2 -> DeviceCmd2: calculateConfidence()
    deactivate DeviceCmd2
end

Composite -> Composite: getConfidence()\n(average of all commands)
deactivate Composite

App -> Visitor: new CommandExecutorVisitor()
activate Visitor

App -> Visitor: visit(compositeCommand)

loop For each command in composite
    Visitor -> DeviceCmd1: visit(deviceCmd1)
    activate DeviceCmd1
    Visitor -> StateMgr: getState("living room light")
    activate StateMgr
    StateMgr -> StateMgr: Update device state
    deactivate StateMgr
    Visitor -> Repo: saveCommand(deviceCmd1)
    activate Repo
    deactivate Repo
    deactivate DeviceCmd1
    
    Visitor -> DeviceCmd2: visit(deviceCmd2)
    activate DeviceCmd2
    Visitor -> StateMgr: getState("bedroom light")
    activate StateMgr
    StateMgr -> StateMgr: Update device state
    deactivate StateMgr
    Visitor -> Repo: saveCommand(deviceCmd2)
    activate Repo
    deactivate Repo
    deactivate DeviceCmd2
end

Visitor -> App: ExecutionResult\n(all commands executed)
deactivate Visitor

App -> User: All lights turned on
deactivate App

@enduml
"""
    return plantuml_code

def create_component_diagram():
    """Create Component Diagram"""
    plantuml_code = """
@startuml Component_Diagram_Voice_Automation_Hub
!theme plain
skinparam shadowing false
skinparam linetype ortho

package "Frontend Layer" {
    component [React Frontend] as Frontend
    component [Voice Interface] as VoiceUI
    component [Command Builder] as Builder
    component [Device Control] as DeviceUI
    component [History Viewer] as HistoryUI
}

package "Backend Layer" {
    component [REST API Controller] as API
    component [Command Interpreter] as Interpreter
    component [Command Executor] as Executor
    component [State Manager] as StateMgr
    component [Repository] as Repo
}

package "Data Layer" {
    database [Command History] as History
    database [Device States] as States
    database [User Preferences] as Preferences
}

Frontend --> API : HTTP/REST
VoiceUI --> Frontend
Builder --> Frontend
DeviceUI --> Frontend
HistoryUI --> Frontend

API --> Interpreter : interprets
API --> Executor : executes
Interpreter --> Repo : reads context
Executor --> StateMgr : updates
Executor --> Repo : saves
StateMgr --> States : manages
Repo --> History : stores
Repo --> Preferences : stores

note right of Interpreter
  **Interpreter Pattern**
  Parses natural language
  into command structures
end note

note right of Executor
  **Visitor Pattern**
  Executes commands
  on device types
end note

note right of Repo
  **Repository Pattern**
  Centralized data storage
  Thread-safe operations
end note

@enduml
"""
    return plantuml_code

def create_use_case_diagram():
    """Create Use Case Diagram"""
    plantuml_code = """
@startuml Use_Case_Diagram_Voice_Automation_Hub
!theme plain
skinparam shadowing false
skinparam linetype ortho

left to right direction

actor User

rectangle "Voice Automation Hub" {
    usecase "Enter Voice Command" as UC1
    usecase "Type Command" as UC2
    usecase "View Available Devices" as UC3
    usecase "View Device Status" as UC4
    usecase "View Command History" as UC5
    usecase "Execute Command" as UC6
    usecase "Interpret Command" as UC7
    usecase "Control Light" as UC8
    usecase "Control Thermostat" as UC9
    usecase "Control Fan" as UC10
    usecase "Control Door Lock" as UC11
    usecase "Create Scene" as UC12
    usecase "Create Routine" as UC13
}

User --> UC1
User --> UC2
User --> UC3
User --> UC4
User --> UC5
User --> UC6

UC1 ..> UC7 : <<include>>
UC2 ..> UC7 : <<include>>
UC7 ..> UC6 : <<include>>

UC6 ..> UC8 : <<extend>>
UC6 ..> UC9 : <<extend>>
UC6 ..> UC10 : <<extend>>
UC6 ..> UC11 : <<extend>>

UC12 ..> UC6 : <<include>>
UC13 ..> UC6 : <<include>>

UC6 ..> UC5 : <<include>>

note right of UC7
  System interprets
  natural language
  into structured command
end note

note right of UC6
  Executes command
  and updates device state
end note

@enduml
"""
    return plantuml_code

def create_state_diagram():
    """Create State Diagram"""
    plantuml_code = """
@startuml State_Diagram_Command_Processing
!theme plain
skinparam shadowing false
skinparam state {
    BackgroundColor LightBlue
    BorderColor DarkBlue
}

[*] --> Idle : System Start

state "Command Processing Flow" as Processing {
    Idle --> Receiving : User Input
    
    state Receiving {
        [*] --> Parsing
    }
    
    Receiving --> Parsing : Command Received
    Parsing --> Validating : Parse Complete
    
    state Validating {
        [*] --> CheckingDevice
        CheckingDevice --> CheckingAction
        CheckingAction --> CalculatingConfidence
    }
    
    Validating --> Interpreting : Validation Pass
    Validating --> Error : Validation Fail
    
    Interpreting --> Executing : Interpretation Complete
    Executing --> UpdatingState : Execution Success
    Executing --> Error : Execution Fail
    
    UpdatingState --> SavingHistory : State Updated
    SavingHistory --> Completed : History Saved
}

Completed --> Idle : Ready for Next Command
Error --> Idle : Error Handled

note right of Validating
  Validates device name,
  action, and parameters
end note

note right of Interpreting
  Calculates confidence
  score and alternatives
end note

note right of Executing
  Updates device state
  via Visitor pattern
end note

@enduml
"""
    return plantuml_code

def create_activity_diagram():
    """Create Activity Diagram"""
    plantuml_code = """
@startuml Activity_Diagram_Command_Flow
!theme plain
skinparam shadowing false
skinparam activity {
    BackgroundColor LightGreen
    BorderColor DarkGreen
}

start

:Receive Command Input;
note right: From user voice or text

:Parse Command;
partition "Parsing" {
    :Extract Device Name;
    :Extract Action;
    :Extract Parameter (if any);
}

:Validate Command;
if (Valid?) then (yes)
    :Create DeviceCommandExpression;
    :Create VoiceCommandContext;
    :Interpret Command;
    :Calculate Confidence Score;
    
    partition "Execution" {
        :Create CommandExecutorVisitor;
        :Visit DeviceCommandExpression;
        :Get Device State;
        
        if (Action Type?) then (ON/OFF)
            :Update Device Power State;
        else (INCREASE/DECREASE)
            :Update Device Value;
        else (SET)
            :Set Device to Parameter Value;
        else (DIM/BRIGHTEN)
            :Adjust Brightness;
        else (LOCK/UNLOCK)
            :Update Lock State;
        endif
        
        :Update DeviceStateManager;
    }
    
    :Save to Repository;
    :Update Command History;
    :Return Success Response;
else (no)
    :Generate Error Message;
    :Return Error Response;
endif

:Display Result to User;
stop

@enduml
"""
    return plantuml_code

def generate_pdf_from_plantuml(plantuml_code, output_filename):
    """Generate PDF from PlantUML code"""
    try:
        from plantuml import PlantUML
        
        # Create PlantUML instance
        plantuml = PlantUML(url='http://www.plantuml.com/plantuml/img/')
        
        # Generate PDF
        output_path = f"uml-diagrams/{output_filename}"
        os.makedirs("uml-diagrams", exist_ok=True)
        
        # Save PlantUML file first
        puml_path = output_path.replace('.pdf', '.puml')
        with open(puml_path, 'w', encoding='utf-8') as f:
            f.write(plantuml_code)
        
        # Try to generate PDF using plantuml.jar if available
        # Otherwise, generate PNG and convert to PDF
        try:
            # Try using plantuml command line tool
            result = subprocess.run(
                ['plantuml', '-tpdf', puml_path],
                capture_output=True,
                text=True,
                timeout=30
            )
            if result.returncode == 0:
                print(f"✓ Generated: {output_filename}")
                return True
        except (FileNotFoundError, subprocess.TimeoutExpired):
            pass
        
        # Fallback: Generate PNG and convert to PDF using reportlab
        try:
            from reportlab.lib.pagesizes import letter
            from reportlab.pdfgen import canvas
            from PIL import Image
            import requests
            from io import BytesIO
            
            # Generate PNG from PlantUML
            png_url = plantuml.get_url(plantuml_code)
            response = requests.get(png_url, timeout=30)
            
            if response.status_code == 200:
                img = Image.open(BytesIO(response.content))
                
                # Create PDF
                pdf_path = output_path
                c = canvas.Canvas(pdf_path, pagesize=letter)
                width, height = letter
                
                # Scale image to fit page
                img_width, img_height = img.size
                scale = min(width / img_width, height / img_height) * 0.9
                new_width = img_width * scale
                new_height = img_height * scale
                x = (width - new_width) / 2
                y = (height - new_height) / 2
                
                # Convert image to RGB if needed
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Save image temporarily
                temp_img = BytesIO()
                img.save(temp_img, format='PNG')
                temp_img.seek(0)
                
                # Draw image on PDF
                c.drawImage(temp_img, x, y, width=new_width, height=new_height)
                c.save()
                
                print(f"✓ Generated: {output_filename}")
                return True
        except Exception as e:
            print(f"⚠ Could not convert PNG to PDF: {e}")
            print(f"  PlantUML file saved: {puml_path}")
            print(f"  You can convert it manually using: plantuml -tpdf {puml_path}")
            return False
        
    except Exception as e:
        print(f"✗ Error generating {output_filename}: {e}")
        # Save PlantUML file anyway
        puml_path = f"uml-diagrams/{output_filename.replace('.pdf', '.puml')}"
        os.makedirs("uml-diagrams", exist_ok=True)
        with open(puml_path, 'w', encoding='utf-8') as f:
            f.write(plantuml_code)
        print(f"  PlantUML file saved: {puml_path}")
        print(f"  Install PlantUML: http://plantuml.com/download")
        print(f"  Then run: plantuml -tpdf {puml_path}")
        return False

def main():
    """Main function to generate all diagrams"""
    print("=" * 60)
    print("UML Diagram Generator for Voice Automation Hub")
    print("=" * 60)
    print()
    
    # Check dependencies
    if not check_dependencies():
        return
    
    # Create output directory
    os.makedirs("uml-diagrams", exist_ok=True)
    
    diagrams = [
        ("Class Diagram - Voice Automation Hub.pdf", create_class_diagram),
        ("Sequence Diagram - Command Interpretation.pdf", create_sequence_interpretation),
        ("Sequence Diagram - Command Execution.pdf", create_sequence_execution),
        ("Sequence Diagram - Composite Command Execution.pdf", create_sequence_composite),
        ("Component Diagram - Voice Automation Hub Architecture.pdf", create_component_diagram),
        ("Use Case Diagram - Voice Automation Hub.pdf", create_use_case_diagram),
        ("State Diagram - Command Processing Flow.pdf", create_state_diagram),
        ("Activity Diagram - Command Flow.pdf", create_activity_diagram),
    ]
    
    print("Generating UML diagrams...")
    print()
    
    success_count = 0
    for filename, diagram_func in diagrams:
        print(f"Generating {filename}...", end=" ")
        plantuml_code = diagram_func()
        if generate_pdf_from_plantuml(plantuml_code, filename):
            success_count += 1
    
    print()
    print("=" * 60)
    print(f"Generation complete: {success_count}/{len(diagrams)} diagrams generated")
    print("=" * 60)
    print()
    print("Diagrams saved in: uml-diagrams/")
    print()
    print("Note: If some PDFs weren't generated, PlantUML (.puml) files")
    print("      were saved. Install PlantUML to convert them:")
    print("      http://plantuml.com/download")
    print("      Then run: plantuml -tpdf uml-diagrams/*.puml")

if __name__ == "__main__":
    main()

