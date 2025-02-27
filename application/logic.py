import subprocess, getpass,  os, json, random, time, logging
import num2word
import serial
from datetime import datetime, timedelta

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


class portIDAllocation(object):
    def __init__(self, *args):
        super(portIDAllocation, self).__init__(*args)
        
    def NumberOfPorts(self):
        NumberOfPorts = len(list(filter(None, " ".join(list(subprocess.check_output(['lsusb', '-s', ':1']).decode())).split("\n"))))
        return NumberOfPorts
     
    def liveUSBPorts(self):
        matchingPortList 	= []
        portIDList		    = []
        NumUSBPort = self.NumberOfPorts()
        print(NumUSBPort)
        current_os_user = getpass.getuser()
        #print("NumUSBPort: ", NumUSBPort, "current_os_user: ", current_os_user)
        constant_path = "/dev/ttyUSB"
        counter = 0
        try:
            USBport = constant_path + str(counter)
            portID  = "Zero"
            if os.path.exists(str(USBport)) == True :
                print("USBport: ", USBport)
                matchingPortList.append(USBport)
                portIDList.append(portID)
        except :
            pass
        counter     = counter + 1
        while (counter < NumUSBPort ):
            variable_path = str(counter)
            USBport = constant_path + variable_path
            print("USBport: ", USBport)
            if os.path.exists(str(USBport)) == True :
                print("USBport: ", USBport, "portID: ", portID)
                portID  = num2word.word(counter)
                matchingPortList.append(USBport)
                portIDList.append(portID)

            counter += 1
        print(portIDList, matchingPortList)
        portAssignment = dict(zip(portIDList, matchingPortList))
        return portAssignment

class serialportSetup(object):
    def __init__(self, serialport, *args):
        self.serialport     = serialport
        super(serialportSetup, self).__init__(*args)

    def serialSetup(self):
        serialport      = self.serialport
        ser             = serial.Serial(serialport, 9600, timeout=1)
        '''with serial.Serial(serialport, 9600, timeout=1) as ser:
            print("Inside Own logic",ser, type(ser))
            return ser
            '''
        return ser


class ATCommands(object):
    def __init__(self, ser, *args):
        self.ser        = ser
        super(ATCommands, self).__init__(*args)
    
    def connect(self):
        try:
            self.serial = serial.Serial(self.port, self.baudrate, timeout=self.timeout)
            time.sleep(1)  # Allow initialization
            logging.info(f"Connected to SIM800C module on port {self.port}.")
            return True
        except Exception as e:
            logging.error(f"Failed to connect to SIM800C on port {self.port}: {e}")
            return False

    def is_module_detected(self):
        """Check if SIM800C responds to AT command"""
        try:
            response = self.send_at_command("AT", "OK")
            return "OK" in response
        except Exception as e:
            logging.error(f"Error checking module detection: {e}")
            return False

    def is_sim_inserted(self):
        """ Check if a SIM card is inserted """
        try:
            response = self.send_at_command("AT+CPIN?")
            time.sleep(1)
            print("response: ", response, "is_sim_inserted: ", "+CPIN: READY" in response)
            time.sleep(3)
            print("is_sim_inserted: ", "+CPIN: READY" in response)
            return "+CPIN: READY" in response
        except Exception as e:
            print("is_sim_inserted: ", f"Error checking SIM card: {e}")
            return False
    
    def is_sim_inserted2(self):
        """Check if a SIM card is inserted and ready."""
        try:
            # Send the AT+CPIN? command
            response = self.send_at_command("AT+CPIN?", "+CPIN:")
            time.sleep(1)  # Wait for the response
            print("Response:", response)

            # Check if the SIM is ready
            if "+CPIN: READY" in response:
                print("SIM card is inserted and ready.")
                return True
            elif "ERROR" in response:
                print("SIM card is not inserted, not recognized, or there is an issue with the modem.")
                return False
            else:
                print("Unexpected response from modem.")
                return False
        except Exception as e:
            print(f"Error checking SIM card: {e}")
            return False

    def send_at_command2(self, command, expected_response):
        """Simulate sending an AT command and receiving a response."""
        # Replace this with actual modem communication logic
        # For testing purposes, simulate different responses
        if command == "AT+CPIN?":
            # Simulate an error response
            return "ERROR"
            # Uncomment the line below to simulate a successful response
            # return "+CPIN: READY"
        return ""
    
    def get_signal_strength_old(self):
        """Returns signal strength in dBm (Converted from CSQ value)"""
        response = self.send_at_command("AT+CSQ") #, "+CSQ:")
        if response:
            try:
                csq_value = int(response.split(":")[1].split(",")[0].strip())
                print("csq_value: ", csq_value)
                if csq_value == 99:
                    return -120  # No signal
                return (2 * csq_value) - 113  # Convert to dBm
            except ValueError:
                logging.error("Failed to parse signal strength.")
                return None
        return None

    def get_signal_strength(self):
        """Retrieve signal strength from SIM800C module."""
        response = self.send_at_command("AT+CSQ") #, expected_response="+CSQ:")
        
        if response:
            try:
                # Extract values from response
                parts = response.split(":")[1].strip().split(",")
                rssi = int(parts[0])
                
                # Convert to dBm
                signal_dbm = -113 + (rssi * 2) if rssi != 99 else "Unknown"
                
                return {
                    "raw_rssi": rssi,
                    "signal_strength_dbm": signal_dbm,
                    "status": "Good" if rssi >= 15 else "Weak" if rssi > 5 else "Very Weak"
                }
            except Exception as e:
                print(f"Error parsing signal strength: {e}")
        
        return {"error": "Failed to retrieve signal strength"}

    def get_module_info(self):
        return self.send_at_command( 'ATI')

    def get_sim_info(self):
        return self.send_at_command( 'AT+CCID')

    def get_operator_info(self):
        operator_name = "N/A"
        response = self.send_at_command('AT+COPS?')
        print("get_operator_response: ", response)
        operator_index = response.find('+COPS:')
        print("operator_index: ", operator_index); #time.sleep(300)
        if operator_index != -1:
            parts = response[operator_index:].split(',')
            print("parts: ", parts)
            if len(parts) >= 3:
                try:
                    operator_name = parts[2].split('"')
                except:
                    pass
                print("operator_name: ", operator_name)
                try:
                    operator_name = operator_name[1].strip(',')
                    print("operator_name: ", operator_name)
                except:
                    pass
                return operator_name
        return None

    def get_signal_info(self):
        response = self.send_at_command('AT+CSQ')
        print("signal_level_response: ", response)
        signal_level = response.split(',')[0].strip('+CSQ: ')
        print("signal_level: ", signal_level)
        return signal_level

    def get_network_info(self):
        #response = self.send_at_command('AT+CIPRXGET?')
        #response = self.send_at_command('AT+CPSI?')
        # Enable engineering mode
        self.send_at_command('AT+CENG=3')
        time.sleep(1)  # Wait for response

        # Query detailed cell information
        response = self.send_at_command('AT+CENG?')
        return response 
    
    def get_network_time(self):
        response = self.send_at_command('AT+CCLK?')
        return response 
    
    def get_network_location_info(self):
        response = self.send_at_command('AT+CIPGSMLOC=1,1')
        return response 
    
    def is_sim_attached(self):
        response = self.send_at_command( 'AT+CPIN?')
        return '+CPIN: READY' in response

    def is_network_available(self):
        response = self.send_at_command('AT+CREG?')
        return '+CREG: 0,1' in response or '+CREG: 0,5' in response

    def get_network_operator(self):
        response = self.send_at_command('AT+COPS?')
        operator_index = response.find('+COPS:')
        if operator_index != -1:
            parts = response[operator_index:].split(',')
            if len(parts) >= 3:
                operator_name = parts[2].strip('"')
                return operator_name
        return None

    def get_network_operators_details(self):
        response = self.send_at_command('AT+COPS=?')
        operator_index = response.find('+COPS:')
        
    def truncate_message(message, max_length=160):
        return message[:max_length]
    
    def set_sms_mode(self):
        self.send_at_command('AT+CMGF=1')  # Set SMS mode to text mode
        time.sleep(3)

    def send_sms(self, phone, sms_message):
        
        """
        Send an SMS message using SIM800C module
        
        Args:
            phone (str): Phone number to send SMS to
            sms_message (str): Message text to send
        
        Returns:
            bool: True if SMS sent successfully, False otherwise
        """
        try:
            # Set SMS mode to text mode
            self.set_sms_mode()
            
            # Truncate message to 160 characters if needed
            truncated_message = self.truncate_message(sms_message)
            
            # Send SMS command sequence
            # 1. Specify the phone number
            response1 = self.send_at_command(f'AT+CMGS="{phone}"')
            
            # Check if phone number was accepted
            if 'ERROR' in response1:
                print(f"Error setting recipient number: {response1}")
                return False
            
            # 2. Send the message text followed by Ctrl+Z (ASCII 26)
            message_with_end = truncated_message + chr(26)
            response2 = self.send_at_command(message_with_end, timeout=10)
            
            # Check if message was sent successfully
            if '+CMGS:' in response2:
                print(f"SMS sent successfully to {phone}")
                return True
            else:
                print(f"Failed to send SMS. Response: {response2}")
                return False
        
        except Exception as e:
            print(f"Exception in send_sms: {e}")
            return False
        
    def list_sms_messages(self):
        messages = []
        response = self.send_at_command( 'AT+CMGL="ALL"')
        time.sleep(3)
        """buffereing_bytes = ser.read(ser.inWaiting())
        print("response: ", response)
        request = buffereing_bytes.decode('utf-8')
        print("request: ", request)"""
        lines = response.strip().split('\r\n')
        #print("lines: ", lines)
        print(len(lines), type(lines))
        #for i in range(0, len(lines)):
        for line in lines:
            if line.startswith('+CMGL'):
                messages.append({
                    'index': int(line.split(',')[0].split(':')[1].strip())})
                #messages.append(line)
            #print(lines[i], "\n\n")
            #if lines[i].start
            #messages.append({'message': lines[i]})
        """try:
            for i in range(0, len(lines), 2):
                print(lines[i], len(lines))
                messages.append({
                    'index': int(lines[i].split(',')[0].split(':')[1].strip()),
                    'sender': lines[i].split(',')[1].strip(),
                    'date': lines[i].split(',')[3].strip(),
                    'message': lines[i+1].strip()
                })
                print(lines[i+1].strip())
        except:
            pass"""
        print(messages)
        return messages
    
    def check_call_status(self):
        response = self.send_at_command( 'AT+CPAS')
        return '+CPAS: 0' in response  # Call active
    
    def send_at_command(self, command, timeout=1):
        ser     = self.ser
        ser.write((command + "\r\n").encode('utf-8'))
        time.sleep(1)
        return ser.read_all().decode('utf-8')

    def send_sms2(self, phone, sms_message):
        """
        Send an SMS message using SIM800C module
        
        Args:
            phone (str): Phone number to send SMS to
            sms_message (str): Message text to send
        
        Returns:
            bool: True if SMS sent successfully, False otherwise
        """
        try:
            # Validate inputs
            if not phone or not sms_message:
                print("Phone number or message is empty")
                return False
            
            # Set SMS mode to text mode
            self.send_at_command('AT+CMGF=1')
            time.sleep(1)
            
            # Truncate message to 160 characters if needed
            truncated_message = sms_message[:160]
            
            # Prepare SMS send command
            send_cmd = f'AT+CMGS="{phone}"\r'
            self.ser.write(send_cmd.encode('utf-8'))
            time.sleep(1)
            
            # Send message with Ctrl+Z
            full_message = truncated_message + chr(26)
            self.ser.write(full_message.encode('utf-8'))
            
            # Wait for response
            time.sleep(2)
            response = self.ser.read_all().decode('utf-8', errors='ignore')
            
            # Check for successful send
            if '+CMGS:' in response:
                print(f"SMS sent successfully to {phone}")
                return True
            else:
                print(f"Failed to send SMS. Response: {response}")
                return False
        
        except Exception as e:
            print(f"Exception in send_sms: {e}")
            return False
        
    def send_at_sms_command(self, command, timeout=1):
        """
        Send an AT command to the serial device and read the response
        """
        try:
            # Ensure serial connection exists and is open
            if not self.ser or not self.ser.is_open:
                print("Serial port is not open")
                return ""
            
            # Clear any existing input buffer
            self.ser.reset_input_buffer()
            
            # Send command
            full_command = command + "\r\n"
            self.ser.write(full_command.encode('utf-8'))
            
            # Wait for response
            time.sleep(timeout)
            
            # Read all available data
            if self.ser.in_waiting > 0:
                response = self.ser.read_all().decode('utf-8', errors='ignore')
                return response.strip()
            
            return ""
        
        except serial.SerialException as e:
            print(f"Serial communication error: {e}")
            return ""
        except Exception as e:
            print(f"Unexpected error in send_at_command: {e}")
            return ""


