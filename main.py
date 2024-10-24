# This script starts the convyer belt system

# You can automate this by adding it in cronjobs

# For cronjobs use the following command (just copy paste it) 

# " @reboot /usr/bin/python3 /path/to/your/main.py "


import serial
import time
import logging

# Configure logging
logging.basicConfig(filename="system_log.txt", level=logging.INFO,
                    format="%(asctime)s - %(message)s")

# Initialize Serial communication
try:
    arduino = serial.Serial(port='/dev/ttyUSB0', baudrate=9600, timeout=1)  # Adjust port as needed
    time.sleep(2)  # Wait for connection to establish
    logging.info("Connected to Arduino.")
except Exception as e:
    logging.error(f"Error connecting to Arduino: {e}")
    exit()

def start_conveyor():
    try:
        # Send command to start the conveyor system
        arduino.write(b'START\n')  # Assuming 'START' is the command used in your .ino file
        logging.info("Conveyor belt started.")
        
        # Wait for Arduino to process and send back responses
        while True:
            response = arduino.readline().decode().strip()
            if response:
                logging.info(f"Arduino response: {response}")
            if "STOP" in response:  # Example to stop, adjust condition based on system requirements
                logging.info("Conveyor belt stopped.")
                break

    except Exception as e:
        logging.error(f"Error during conveyor operation: {e}")
    finally:
        arduino.close()
        logging.info("Closed connection to Arduino.")

if __name__ == "__main__":
    start_conveyor()
