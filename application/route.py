from datetime import datetime
import os,  time, json


from flask import render_template, request, jsonify, session, redirect, url_for
from application import app
from .logic import ATCommands, portIDAllocation, serialportSetup
import serial
import num2word

from application import app
#from .logic import SIM800C


# SIM800C module configuration
SIM800C_PORT = '/dev/ttyUSB0'  # Serial port for SIM800C (e.g., '/dev/ttyUSB0' or 'COM3')
POSSIBLE_PORTS = ['/dev/ttyUSB0', '/dev/ttyUSB1', '/dev/ttyUSB2', '/dev/ttyAMA0', '/dev/ttyS0', '/dev/ttyACM0']

SIM800C_PORT = None
for port in POSSIBLE_PORTS:
    try:
        SIM800C_PORT = serial.Serial(port, 9600, timeout=1)  # Adjust the baud rate as needed
        print(f"Serial port initialized successfully on {port}.")
        break  # Stop trying ports once a valid one is found
    except serial.SerialException as e:
        print(f"Error initializing serial port on {port}: {e}")
        SIM800C_PORT = None  # Reset to None if the port is unavailable

if SIM800C_PORT is None:
    print("No valid serial port found. SMS functionality will be disabled.")




@app.route('/', methods=['GET', 'POST'])
def home():
    
    """
    Home page route.
    Displays SIM800C module status.
    """
    try:
        serialportBuild     = portIDAllocation()
        SERIAL_PORTS        = serialportBuild.liveUSBPorts()
        firstKey            = list(SERIAL_PORTS.keys())[0]
        serialport          = SERIAL_PORTS[firstKey]
    except :
        return 'Serial port could not be detected!' #, {"Refresh": "3; url=/"}
        #pass
    serBuild        = serialportSetup(serialport)
    ser             = serBuild.serialSetup()
    try:
        serBuild        = serialportSetup(serialport)
        ser             = serBuild.serialSetup()
    except :
        return f"Serial port could not be initiated! Please run ' sudo chown $USER {serialport} '." #, {"Refresh": "3; url=/"}
        #pass
    
    module_detected = "No"
    #with serial.Serial('/dev/ttyUSB0', 9600, timeout=1) as ser:
    if ser:
        commandBuild        = ATCommands(ser)
        module_detected     = commandBuild.is_module_detected()
    

    #module_detected = sim800c.is_module_detected()
    
    sim_inserted = "" #sim800c.is_sim_inserted()
    signal_strength = "" #sim800c.get_signal_strength()

    try:
        sim_inserted = commandBuild.is_sim_inserted()
    except :
        pass
    
    # Default status values
    module_status = "Not Detected"
    sim_status = "Unknown"
    signal_strength = "N/A"

    # Check for SIM800C module detection
    print("module_status: ", module_status)
    try:
        response = commandBuild.is_module_detected()
        print("response: ", response); #time.sleep(300)
        if response:
            module_status = "Detected"
        else:
            module_status = "Not Detected"
    except Exception as e:
        module_status = f"Error: {e}"

    print("module_status: ", module_status)


    # Get the network signal level using AT+CSQ
    try:
        csq_response =  commandBuild.get_signal_strength() #" #sim800c.send_at_command("AT+CSQ")
        print("Signal strenght response: ", csq_response)
        signal_strength = "N/A"
        try:
            raw_rssi            = csq_response["raw_rssi"]
            signal_strength_dbm = csq_response["signal_strength_dbm"]
            signal_strength     = str(signal_strength_dbm) + "dbm"
            status              = csq_response["status"]
        except :
            pass
    except Exception as e:
        signal_strength = f"Error: {e}"

    
    return render_template('index.html',

        module_status=module_status, 
        sim_status=sim_status, 
        module_detected=module_detected,
        sim_inserted=sim_inserted,
        signal_strength=signal_strength,
        #network_operator=network_operator
        )


#
@app.route('/view_concerns')
def view_concerns():
    """
    Reads the concerns from the concerns.json file and displays them in a formatted table.
    """
    try:
        # Path to the JSON file that stores the concerns
        concerns_file_path = 'concerns.json'

        # Check if the file exists
        if os.path.exists(concerns_file_path):
            with open(concerns_file_path, 'r') as file:
                concerns = json.load(file)
        else:
            concerns = []

        # Render the table with the concerns
        return render_template('view_concerns.html', concerns=concerns)

    except Exception as e:
        print(f"Error reading concerns: {e}")
        return "An error occurred while fetching the concerns."


# Route for handling form submissions from the send_msg page
@app.route('/submit_concern', methods=['POST'])
def submit_concern():
    """
    Handles form submissions from the send_msg page.
    Processes the data, appends the new concern to a JSON file, and sends an SMS to the intended office.
    """
    try:
        serialportBuild     = portIDAllocation()
        SERIAL_PORTS        = serialportBuild.liveUSBPorts()
        firstKey            = list(SERIAL_PORTS.keys())[0]
        serialport          = SERIAL_PORTS[firstKey]
    except :
        return 'Serial port could not be detected!' #, {"Refresh": "3; url=/"}
        #pass
    serBuild        = serialportSetup(serialport)
    ser             = serBuild.serialSetup()
    try:
        serBuild        = serialportSetup(serialport)
        ser             = serBuild.serialSetup()
    except :
        return f"Serial port could not be initiated! Please run ' sudo chown $USER {serialport} '." #, {"Refresh": "3; url=/"}
        #pass
    
    
    #with serial.Serial('/dev/ttyUSB0', 9600, timeout=1) as ser:
    if ser:
        commandBuild        = ATCommands(ser)
    try:
        # Retrieve form data
        name            = request.form.get('name', '').strip()
        matric_number   = request.form.get('matric_number', '').strip()
        message         = request.form.get('message', '').strip()
        office          = session.get('selected_office', {})

        # Validate the message (required field)
        if not message:
            return redirect(url_for('send_msg'))

        # Log the submission (for debugging purposes)
        print(f"New concern submitted:")
        print(f"Name: {name}")
        print(f"Matric Number: {matric_number}")
        print(f"Message: {message}")
        print(f"Office: {office.get('name', 'Unknown Office')}")

        # Prepare the concern data to append
        concern_data = {
            'name': name,
            'matric_number': matric_number,
            'message': message,
            'office': office.get('name', 'Unknown Office'),
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'sms_sent': False  # Default to False until we attempt to send the SMS
        }

        # Path to the JSON file that stores the concerns
        concerns_file_path = 'concerns.json'

        # Check if the file exists
        if os.path.exists(concerns_file_path):
            # Load existing data and append the new concern
            with open(concerns_file_path, 'r') as file:
                concerns = json.load(file)
        else:
            # Create a new list if the file doesn't exist
            concerns = []

        # Send an SMS to the office's phone number
        if office and 'phone' in office:
            sms_message = f"New Concern:\nMatric Number: {matric_number}\nMessage: {message}"
            try:
                commandBuild.set_sms_mode()
            except :
                pass

            if commandBuild.send_sms2(office['phone'], sms_message):
                msg = "SMS sent successfully."
                resp_msg = "success"
                concern_data['sms_sent'] = True  # Update sms_sent to True if SMS is sent
                print(msg, resp_msg)
            else:
                msg = "Failed to send SMS."
                resp_msg = "warning"
                print(msg, resp_msg)
        else:
            msg = "Office phone number not found."
            resp_msg = "info"
            print(msg, resp_msg)

        # Append the new concern with the sms_sent status to the concerns list
        concerns.append(concern_data)

        # Write back the updated concerns to the file
        with open(concerns_file_path, 'w') as file:
            json.dump(concerns, file, indent=4)

        print(msg, resp_msg)
        # Redirect to the success page
        return redirect(url_for('success', msg=msg, resp_msg=resp_msg))

    except Exception as e:
        # Log the error and redirect to the home page
        print(f"Error processing form submission: {e}")
        return redirect(url_for('home') )
 
# Route for the send_msg page
@app.route('/send_msg', methods=['GET', 'POST'])
def send_msg():
    """
    View More page route.
    Renders the send_msg.html template with office data from the query parameter.
    """
    # Retrieve the selected office from the query parameter
    office_data = request.args.get('office')
    #print("Raw office_data:", office_data)

    office = {}

    if office_data:
        try:
            office = json.loads(office_data)
            #print("Parsed office:", office)
            session['selected_office'] = office  # Store in Flask session if needed
        except json.JSONDecodeError as e:
            #print(f"Invalid JSON format for office data: {e}")
            office = session.get('selected_office', {})  # Fall back to session data
    else:
        office = session.get('selected_office', {})

    #print("Final office object:", office)

    if request.method == "POST":
        print(request.form)  # Handle form submission if needed

    return render_template('send_msg.html', office=office)#


@app.route("/success")
def success():
    msg         = request.args.get('msg')
    resp_msg    = request.args.get('resp_msg')
    print(msg, resp_msg)
    return render_template('success.html', msg=msg, resp_msg=resp_msg)

