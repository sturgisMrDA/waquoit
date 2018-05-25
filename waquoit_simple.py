import temp_sensor, time
from gpiozero import LED

# Global constants
FILENAME = 'temperature.txt'
READ_INTERVAL = 10 # Interval in seconds

def get_reading():
    temperature = temp_sensor.read_temp()['1']
    temperature = temperature * 1.8 + 32.0
    return temperature

def write_data(temperature):
    with open(FILENAME, 'a') as data_file:
        timestamp = time.ctime()
        data = timestamp + ', ' + str(temperature) 
        # Don't forget '\n' to add a newline after each entry:
        data_file.write(data+ '\n')
        # Close the file until next cycle to avoid losing data in case of power loss.
        data_file.close()
    return

def initialize_file():
    """ Create blank data file and write headers. """
    data_file = open(FILENAME, 'w')
    data_file.write('Time, Temp\n')
    data_file.close()
    return

# Main code

# Create Button and LED objects
status_led = LED(17)

# Create blank data file and write headers.
initialize_file()

# Collect data at intervals

while True:
    status_led.on()
    temperature = get_reading()
    write_data(temperature)
    status_led.off()
    time.sleep(READ_INTERVAL)

