import temp_sensor, time
from gpiozero import LED

# Global constants
STATUS_LED_PIN = 17 # GPIO pin for status led
READ_INTERVAL = 10 # Seconds between data readings.
FILENAME = 'temperature_data.txt'
FAHRENHEIT = True # Set to False for Celsius readings.
PRINT_DATA = False # Whether to print data to screen.  Set to True for testing.

def get_reading():
    temperature = temp_sensor.read_temp()['1']
    # Temperature is C by default.  Change to F if indicated by FAHRENHEIT flag:
    if FAHRENHEIT:
        temperature = temperature * 9 / 5 + 32
    return temperature

def write_data(temperature):
    with open(FILENAME, 'a') as data_file:
        timestamp = time.ctime()
        data = timestamp + ', ' + str(temperature) 
        if PRINT_DATA:
            print(data)
        # Don't forget '\n' to add a newline after each entry:
        data_file.write(data+ '\n')
        # Close the file until next cycle to avoid losing data in case of power loss.
        data_file.close()
    return

def initialize_file(name):
    """ Create blank data file and write headers. """
    data_file = open(FILENAME, 'w')
    if FAHRENHEIT:
        t_unit = 'F'
    else:
        t_unit = 'C'
    data_file.write('Time, Temp (*' + t_unit + ')\n')
    data_file.close()
    return

def end_data_collection():
    """ Set logging to False to end data collection. """
    print("Data collection halted.  Wrapping up...")
    global logging
    logging = False
    return

# Main code

# Create Button and LED objects
status_led = LED(STATUS_LED_PIN)

# Create blank data file and write headers.
initialize_file(FILENAME)

# Collect data at intervals
logging = True 
while logging:
    status_led.on()
    temperature = get_reading()
    write_data(temperature)
    status_led.off()
    time.sleep(READ_INTERVAL)

