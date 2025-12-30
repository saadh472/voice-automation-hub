#!/usr/bin/env python3
"""
Standalone UML Diagram Generator for Voice Automation Hub
Uses pure Python libraries (graphviz, reportlab) to generate PDFs
No external tools required
"""

import os
import sys
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import subprocess

def install_dependencies():
    """Install required Python packages"""
    packages = ['reportlab', 'graphviz']
    for package in packages:
        try:
            __import__(package)
        except ImportError:
            print(f"Installing {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package, "--quiet"])

def create_class_diagram_pdf():
    """Create Class Diagram PDF using reportlab"""
    output_path = "uml-diagrams/Class Diagram - Voice Automation Hub.pdf"
    os.makedirs("uml-diagrams", exist_ok=True)
    
    doc = SimpleDocTemplate(output_path, pagesize=letter)
    story = []
    styles = getSampleStyleSheet()
    
    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=20,
        textColor=colors.HexColor('#1a1a1a'),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    story.append(Paragraph("Class Diagram - Voice Automation Hub", title_style))
    story.append(Spacer(1, 0.2*inch))
    
    # Create a visual class diagram using tables
    class_data = [
        ['<b>App (Main Controller)</b>', '<b>CommandExpression (Interface)</b>'],
        ['- VALID_DEVICES: Set<String>', '+ interpret(context): void'],
        ['- VALID_ACTIONS: Set<String>', '+ getConfidence(): double'],
        ['+ main(args): void', '+ isValid(): boolean'],
        ['+ interpret(req): ResponseEntity', ''],
        ['+ execute(cmd): ResponseEntity', ''],
        ['+ getDevices(): ResponseEntity', ''],
        ['+ getHistory(): ResponseEntity', ''],
        ['', ''],
        ['<b>DeviceCommandExpression</b>', '<b>CompositeCommand</b>'],
        ['- deviceName: String', '- commands: List<CommandExpression>'],
        ['- action: String', '- name: String'],
        ['- parameter: String', '+ add(cmd): void'],
        ['- confidence: double', '+ interpret(context): void'],
        ['- valid: boolean', '+ getConfidence(): double'],
        ['+ interpret(context): void', '+ isValid(): boolean'],
        ['+ getConfidence(): double', ''],
        ['', ''],
        ['<b>CommandVisitor (Interface)</b>', '<b>CommandExecutorVisitor</b>'],
        ['+ visit(DeviceCommand): Result', '+ visit(DeviceCommand): Result'],
        ['+ visit(SceneCommand): Result', '+ visit(SceneCommand): Result'],
        ['+ visit(RoutineCommand): Result', '+ visit(RoutineCommand): Result'],
        ['', ''],
        ['<b>VoiceCommandContext</b>', '<b>DeviceState</b>'],
        ['- interpretedCommands: List', '- isOn: boolean'],
        ['- availableDevices: Set<String>', '- brightness: int'],
        ['- confidence: double', '- temperature: int'],
        ['- rawCommand: String', '- status: String'],
        ['+ addInterpretedCommand(cmd): void', '+ isOn(): boolean'],
        ['+ addAvailableDevice(device): void', '+ setOn(on): void'],
        ['+ setConfidence(conf): void', '+ getBrightness(): int'],
        ['', ''],
        ['<b>DeviceStateManager</b>', '<b>Repository</b>'],
        ['- deviceStates: Map<String, DeviceState>', '- commandHistory: List<Map>'],
        ['+ getState(device): DeviceState', '- userPreferences: Map'],
        ['+ getAllStates(): Map', '+ saveCommand(cmd): void'],
        ['', '+ getHistory(): List<Map>'],
        ['', '+ getHistorySize(): int'],
        ['', ''],
        ['<b>SceneCommand</b>', '<b>RoutineCommand</b>'],
        ['- sceneName: String', '- routineName: String'],
        ['- commands: List<DeviceCommand>', '- steps: List<CommandExpression>'],
        ['+ getSceneName(): String', '+ getRoutineName(): String'],
        ['+ getCommands(): List', '+ getSteps(): List'],
        ['+ addCommand(cmd): void', '+ addStep(step): void'],
    ]
    
    table = Table(class_data, colWidths=[3.5*inch, 3.5*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4a90e2')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
    ]))
    story.append(table)
    story.append(Spacer(1, 0.3*inch))
    
    # Relationships section
    story.append(Paragraph("<b>Key Relationships:</b>", styles['Heading2']))
    relationships = [
        "• CommandExpression <|.. DeviceCommandExpression (implements)",
        "• CommandExpression <|.. CompositeCommand (implements)",
        "• CompositeCommand *-- CommandExpression (contains)",
        "• CommandVisitor <|.. CommandExecutorVisitor (implements)",
        "• CommandExecutorVisitor ..> ExecutionResult (creates)",
        "• CommandExecutorVisitor ..> DeviceStateManager (uses)",
        "• CommandExecutorVisitor ..> Repository (uses)",
        "• DeviceCommandExpression ..> VoiceCommandContext (uses)",
        "• SceneCommand *-- DeviceCommandExpression (contains)",
        "• RoutineCommand *-- CommandExpression (contains)",
        "• DeviceStateManager *-- DeviceState (manages)",
        "• App ..> CommandExpression (creates)",
        "• App ..> CommandExecutorVisitor (uses)",
        "• App ..> VoiceCommandContext (creates)",
        "• App ..> Repository (uses)",
    ]
    for rel in relationships:
        story.append(Paragraph(rel, styles['Normal']))
        story.append(Spacer(1, 0.1*inch))
    
    story.append(Spacer(1, 0.2*inch))
    
    # Design Patterns section
    story.append(Paragraph("<b>Design Patterns:</b>", styles['Heading2']))
    patterns = [
        "<b>Interpreter Pattern:</b> CommandExpression interface defines grammar for commands",
        "<b>Composite Pattern:</b> CompositeCommand groups multiple commands",
        "<b>Visitor Pattern:</b> CommandVisitor executes commands on different device types",
        "<b>Singleton Pattern:</b> VoiceServiceManager provides thread-safe instance management",
        "<b>Repository Pattern:</b> Repository provides centralized command history storage",
    ]
    for pattern in patterns:
        story.append(Paragraph(pattern, styles['Normal']))
        story.append(Spacer(1, 0.1*inch))
    
    doc.build(story)
    print("Generated: Class Diagram - Voice Automation Hub.pdf")
    return True

def create_sequence_diagram_pdf(name, description, steps):
    """Create Sequence Diagram PDF"""
    output_path = f"uml-diagrams/Sequence Diagram - {name}.pdf"
    os.makedirs("uml-diagrams", exist_ok=True)
    
    doc = SimpleDocTemplate(output_path, pagesize=letter)
    story = []
    styles = getSampleStyleSheet()
    
    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.HexColor('#1a1a1a'),
        spaceAfter=20,
        alignment=TA_CENTER
    )
    story.append(Paragraph(f"Sequence Diagram - {name}", title_style))
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph(description, styles['Normal']))
    story.append(Spacer(1, 0.3*inch))
    
    # Create sequence table
    seq_data = [['Participant', 'Action', 'Result']]
    
    for step in steps:
        seq_data.append(step)
    
    table = Table(seq_data, colWidths=[2*inch, 3.5*inch, 2.5*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4a90e2')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f5f5f5')]),
    ]))
    story.append(table)
    
    doc.build(story)
    print(f"Generated: Sequence Diagram - {name}.pdf")
    return True

def create_all_diagrams():
    """Generate all UML diagrams"""
    print("=" * 70)
    print("UML Diagram Generator - Voice Automation Hub")
    print("=" * 70)
    print()
    
    # Install dependencies
    try:
        install_dependencies()
    except Exception as e:
        print(f"Warning: Could not install all dependencies: {e}")
        print("Continuing anyway...")
        print()
    
    os.makedirs("uml-diagrams", exist_ok=True)
    
    # Generate Class Diagram
    print("Generating Class Diagram...")
    create_class_diagram_pdf()
    
    # Generate Sequence Diagrams
    print("\nGenerating Sequence Diagrams...")
    
    # Command Interpretation
    interpretation_steps = [
        ['User', 'Enter voice command', ''],
        ['Frontend', 'POST /api/interpret', '{"command": "turn on living room light"}'],
        ['App', 'parseDevice(command)', 'Extract device name'],
        ['App', 'parseAction(command)', 'Extract action'],
        ['App', 'parseParameter(command)', 'Extract parameter (if any)'],
        ['App', 'new VoiceCommandContext()', 'Create context'],
        ['App', 'new DeviceCommandExpression()', 'Create command expression'],
        ['DeviceCommandExpression', 'validate()', 'Validate device and action'],
        ['DeviceCommandExpression', 'interpret(context)', 'Interpret command'],
        ['DeviceCommandExpression', 'calculateConfidence()', 'Calculate confidence score'],
        ['Repository', 'setLastRawCommand()', 'Save raw command'],
        ['App', 'generateAlternatives()', 'Generate alternative commands'],
        ['App', 'Return ResponseEntity', 'Return interpretation result'],
        ['Frontend', 'Display interpretation', 'Show to user'],
    ]
    create_sequence_diagram_pdf(
        "Command Interpretation",
        "Shows the flow of interpreting a natural language command into a structured command.",
        interpretation_steps
    )
    
    # Command Execution
    execution_steps = [
        ['User', 'Execute command', ''],
        ['Frontend', 'POST /api/execute', '{"device": "...", "action": "..."}'],
        ['App', 'Validate command', 'Check validity'],
        ['App', 'new CommandExecutorVisitor()', 'Create visitor'],
        ['CommandExecutorVisitor', 'visit(deviceCommand)', 'Execute command'],
        ['CommandExecutorVisitor', 'getState(deviceName)', 'Get device state'],
        ['DeviceStateManager', 'getState()', 'Return DeviceState'],
        ['CommandExecutorVisitor', 'Update state based on action', 'ON/OFF/INCREASE/etc'],
        ['DeviceState', 'setOn() / setBrightness()', 'Update device properties'],
        ['Repository', 'saveCommand()', 'Save to history'],
        ['CommandExecutorVisitor', 'Return ExecutionResult', 'Success/failure'],
        ['App', 'Return ResponseEntity', 'Return execution result'],
        ['Frontend', 'Display result', 'Show to user'],
    ]
    create_sequence_diagram_pdf(
        "Command Execution",
        "Shows the flow of executing a validated command and updating device state.",
        execution_steps
    )
    
    # Composite Command
    composite_steps = [
        ['User', 'Execute composite command', '"Turn on all lights"'],
        ['App', 'new CompositeCommand()', 'Create composite'],
        ['App', 'Add DeviceCommandExpression 1', '"living room light", "ON"'],
        ['App', 'Add DeviceCommandExpression 2', '"bedroom light", "ON"'],
        ['CompositeCommand', 'interpret(context)', 'Interpret all commands'],
        ['CompositeCommand', 'Loop: interpret each command', 'Process each command'],
        ['App', 'new CommandExecutorVisitor()', 'Create visitor'],
        ['CommandExecutorVisitor', 'visit(compositeCommand)', 'Execute composite'],
        ['CommandExecutorVisitor', 'Loop: visit each command', 'Execute each command'],
        ['DeviceStateManager', 'Update state for each device', 'Update all devices'],
        ['Repository', 'saveCommand() for each', 'Save all commands'],
        ['CommandExecutorVisitor', 'Return ExecutionResult', 'All commands executed'],
        ['App', 'Return success', 'All lights turned on'],
    ]
    create_sequence_diagram_pdf(
        "Composite Command Execution",
        "Shows how composite commands (multiple commands grouped together) are executed.",
        composite_steps
    )
    
    # Generate Component Diagram
    print("\nGenerating Component Diagram...")
    create_component_diagram_pdf()
    
    # Generate Use Case Diagram
    print("\nGenerating Use Case Diagram...")
    create_use_case_diagram_pdf()
    
    # Generate State Diagram
    print("\nGenerating State Diagram...")
    create_state_diagram_pdf()
    
    # Generate Activity Diagram
    print("\nGenerating Activity Diagram...")
    create_activity_diagram_pdf()
    
    print()
    print("=" * 70)
    print("All diagrams generated successfully!")
    print("=" * 70)
    print(f"\nDiagrams saved in: uml-diagrams/")
    print("\nGenerated files:")
    files = [
        "Class Diagram - Voice Automation Hub.pdf",
        "Sequence Diagram - Command Interpretation.pdf",
        "Sequence Diagram - Command Execution.pdf",
        "Sequence Diagram - Composite Command Execution.pdf",
        "Component Diagram - Voice Automation Hub Architecture.pdf",
        "Use Case Diagram - Voice Automation Hub.pdf",
        "State Diagram - Command Processing Flow.pdf",
        "Activity Diagram - Command Flow.pdf",
    ]
    for f in files:
        if os.path.exists(f"uml-diagrams/{f}"):
            print(f"  [OK] {f}")
        else:
            print(f"  [FAILED] {f}")

def create_component_diagram_pdf():
    """Create Component Diagram PDF"""
    output_path = "uml-diagrams/Component Diagram - Voice Automation Hub Architecture.pdf"
    os.makedirs("uml-diagrams", exist_ok=True)
    
    doc = SimpleDocTemplate(output_path, pagesize=letter)
    story = []
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.HexColor('#1a1a1a'),
        spaceAfter=20,
        alignment=TA_CENTER
    )
    story.append(Paragraph("Component Diagram - Voice Automation Hub Architecture", title_style))
    story.append(Spacer(1, 0.3*inch))
    
    # Frontend Layer
    story.append(Paragraph("<b>Frontend Layer</b>", styles['Heading2']))
    frontend_components = [
        "• React Frontend - Main application UI",
        "• Voice Interface - Voice command input",
        "• Command Builder - Text command input",
        "• Device Control - Device management UI",
        "• History Viewer - Command history display",
    ]
    for comp in frontend_components:
        story.append(Paragraph(comp, styles['Normal']))
    story.append(Spacer(1, 0.2*inch))
    
    # Backend Layer
    story.append(Paragraph("<b>Backend Layer</b>", styles['Heading2']))
    backend_components = [
        "• REST API Controller - HTTP endpoint handler",
        "• Command Interpreter - Parses natural language (Interpreter Pattern)",
        "• Command Executor - Executes commands (Visitor Pattern)",
        "• State Manager - Manages device states",
        "• Repository - Stores command history (Repository Pattern)",
    ]
    for comp in backend_components:
        story.append(Paragraph(comp, styles['Normal']))
    story.append(Spacer(1, 0.2*inch))
    
    # Data Layer
    story.append(Paragraph("<b>Data Layer</b>", styles['Heading2']))
    data_components = [
        "• Command History - Stores executed commands",
        "• Device States - Current state of all devices",
        "• User Preferences - User-specific settings",
    ]
    for comp in data_components:
        story.append(Paragraph(comp, styles['Normal']))
    story.append(Spacer(1, 0.3*inch))
    
    # Relationships
    story.append(Paragraph("<b>Component Relationships:</b>", styles['Heading2']))
    relationships = [
        "Frontend → REST API Controller (HTTP/REST)",
        "REST API Controller → Command Interpreter (interprets)",
        "REST API Controller → Command Executor (executes)",
        "Command Interpreter → Repository (reads context)",
        "Command Executor → State Manager (updates)",
        "Command Executor → Repository (saves)",
        "State Manager → Device States (manages)",
        "Repository → Command History (stores)",
        "Repository → User Preferences (stores)",
    ]
    for rel in relationships:
        story.append(Paragraph(f"• {rel}", styles['Normal']))
    
    doc.build(story)
    print("Generated: Component Diagram - Voice Automation Hub Architecture.pdf")
    return True

def create_use_case_diagram_pdf():
    """Create Use Case Diagram PDF"""
    output_path = "uml-diagrams/Use Case Diagram - Voice Automation Hub.pdf"
    os.makedirs("uml-diagrams", exist_ok=True)
    
    doc = SimpleDocTemplate(output_path, pagesize=letter)
    story = []
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.HexColor('#1a1a1a'),
        spaceAfter=20,
        alignment=TA_CENTER
    )
    story.append(Paragraph("Use Case Diagram - Voice Automation Hub", title_style))
    story.append(Spacer(1, 0.3*inch))
    
    story.append(Paragraph("<b>Primary Use Cases:</b>", styles['Heading2']))
    use_cases = [
        ("Enter Voice Command", "User speaks a command to control devices"),
        ("Type Command", "User types a command in text form"),
        ("View Available Devices", "User views list of controllable devices"),
        ("View Device Status", "User checks current state of a device"),
        ("View Command History", "User views history of executed commands"),
        ("Execute Command", "System executes a validated command"),
        ("Interpret Command", "System interprets natural language into structured command"),
    ]
    
    for uc_name, uc_desc in use_cases:
        story.append(Paragraph(f"<b>{uc_name}</b>", styles['Normal']))
        story.append(Paragraph(f"  {uc_desc}", styles['Normal']))
        story.append(Spacer(1, 0.1*inch))
    
    story.append(Spacer(1, 0.2*inch))
    story.append(Paragraph("<b>Device Control Use Cases:</b>", styles['Heading2']))
    device_cases = [
        "• Control Light - Turn on/off, dim, brighten lights",
        "• Control Thermostat - Set temperature, increase/decrease",
        "• Control Fan - Turn on/off, adjust speed",
        "• Control Door Lock - Lock/unlock door",
    ]
    for case in device_cases:
        story.append(Paragraph(case, styles['Normal']))
    
    story.append(Spacer(1, 0.2*inch))
    story.append(Paragraph("<b>Advanced Use Cases:</b>", styles['Heading2']))
    advanced_cases = [
        "• Create Scene - Group multiple commands together",
        "• Create Routine - Create automated command sequences",
    ]
    for case in advanced_cases:
        story.append(Paragraph(case, styles['Normal']))
    
    story.append(Spacer(1, 0.2*inch))
    story.append(Paragraph("<b>Use Case Relationships:</b>", styles['Heading2']))
    story.append(Paragraph("• Enter Voice Command → Interpret Command (include)", styles['Normal']))
    story.append(Paragraph("• Type Command → Interpret Command (include)", styles['Normal']))
    story.append(Paragraph("• Interpret Command → Execute Command (include)", styles['Normal']))
    story.append(Paragraph("• Execute Command → Control Light/Thermostat/Fan/Lock (extend)", styles['Normal']))
    story.append(Paragraph("• Create Scene → Execute Command (include)", styles['Normal']))
    story.append(Paragraph("• Create Routine → Execute Command (include)", styles['Normal']))
    story.append(Paragraph("• Execute Command → View Command History (include)", styles['Normal']))
    
    doc.build(story)
    print("Generated: Use Case Diagram - Voice Automation Hub.pdf")
    return True

def create_state_diagram_pdf():
    """Create State Diagram PDF"""
    output_path = "uml-diagrams/State Diagram - Command Processing Flow.pdf"
    os.makedirs("uml-diagrams", exist_ok=True)
    
    doc = SimpleDocTemplate(output_path, pagesize=letter)
    story = []
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.HexColor('#1a1a1a'),
        spaceAfter=20,
        alignment=TA_CENTER
    )
    story.append(Paragraph("State Diagram - Command Processing Flow", title_style))
    story.append(Spacer(1, 0.3*inch))
    
    story.append(Paragraph("<b>State Flow:</b>", styles['Heading2']))
    
    states = [
        ("Idle", "System is ready to receive commands"),
        ("Receiving", "User input is being received"),
        ("Parsing", "Command text is being parsed"),
        ("Validating", "Parsed command is being validated"),
        ("Interpreting", "Valid command is being interpreted"),
        ("Executing", "Command is being executed"),
        ("UpdatingState", "Device state is being updated"),
        ("SavingHistory", "Command is being saved to history"),
        ("Completed", "Command processing is complete"),
        ("Error", "An error occurred during processing"),
    ]
    
    for state_name, state_desc in states:
        story.append(Paragraph(f"<b>{state_name}</b>", styles['Normal']))
        story.append(Paragraph(f"  {state_desc}", styles['Normal']))
        story.append(Spacer(1, 0.1*inch))
    
    story.append(Spacer(1, 0.2*inch))
    story.append(Paragraph("<b>State Transitions:</b>", styles['Heading2']))
    transitions = [
        "Idle → Receiving (User Input)",
        "Receiving → Parsing (Command Received)",
        "Parsing → Validating (Parse Complete)",
        "Validating → Interpreting (Validation Pass)",
        "Validating → Error (Validation Fail)",
        "Interpreting → Executing (Interpretation Complete)",
        "Executing → UpdatingState (Execution Success)",
        "Executing → Error (Execution Fail)",
        "UpdatingState → SavingHistory (State Updated)",
        "SavingHistory → Completed (History Saved)",
        "Completed → Idle (Ready for Next Command)",
        "Error → Idle (Error Handled)",
    ]
    for trans in transitions:
        story.append(Paragraph(f"• {trans}", styles['Normal']))
    
    doc.build(story)
    print("Generated: State Diagram - Command Processing Flow.pdf")
    return True

def create_activity_diagram_pdf():
    """Create Activity Diagram PDF"""
    output_path = "uml-diagrams/Activity Diagram - Command Flow.pdf"
    os.makedirs("uml-diagrams", exist_ok=True)
    
    doc = SimpleDocTemplate(output_path, pagesize=letter)
    story = []
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.HexColor('#1a1a1a'),
        spaceAfter=20,
        alignment=TA_CENTER
    )
    story.append(Paragraph("Activity Diagram - Command Flow", title_style))
    story.append(Spacer(1, 0.3*inch))
    
    story.append(Paragraph("<b>Activity Flow:</b>", styles['Heading2']))
    
    activities = [
        ("1. Receive Command Input", "From user voice or text input"),
        ("2. Parse Command", "Extract device name, action, and parameter"),
        ("3. Validate Command", "Check if device and action are valid"),
        ("4. Create Command Expression", "Create DeviceCommandExpression object"),
        ("5. Create Context", "Create VoiceCommandContext"),
        ("6. Interpret Command", "Interpret and calculate confidence"),
        ("7. Create Executor", "Create CommandExecutorVisitor"),
        ("8. Execute Command", "Visit and execute the command"),
        ("9. Get Device State", "Retrieve current device state"),
        ("10. Update Device State", "Update based on action type"),
        ("11. Save to Repository", "Save command to history"),
        ("12. Return Response", "Return success or error response"),
        ("13. Display Result", "Show result to user"),
    ]
    
    for activity_num, activity_desc in activities:
        story.append(Paragraph(f"<b>{activity_num}</b>", styles['Normal']))
        story.append(Paragraph(f"  {activity_desc}", styles['Normal']))
        story.append(Spacer(1, 0.1*inch))
    
    story.append(Spacer(1, 0.2*inch))
    story.append(Paragraph("<b>Decision Points:</b>", styles['Heading2']))
    story.append(Paragraph("• After Validation: If valid → Continue, If invalid → Return Error", styles['Normal']))
    story.append(Paragraph("• Action Type: ON/OFF, INCREASE/DECREASE, SET, DIM/BRIGHTEN, LOCK/UNLOCK", styles['Normal']))
    
    doc.build(story)
    print("Generated: Activity Diagram - Command Flow.pdf")
    return True

if __name__ == "__main__":
    create_all_diagrams()

