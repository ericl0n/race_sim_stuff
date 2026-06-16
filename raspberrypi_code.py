import analogio
import usb_hid
import time
import board
import digitalio

# ADC Pin
ADC_PIN = board.GP26  # Ensure this is correct for your board
led = digitalio.DigitalInOut(board.GP22)
led.direction = digitalio.Direction.OUTPUT
# The HID descriptor for a generic HID device with a single report
HID_REPORT_DESCRIPTOR = bytearray([
    0x05, 0x01,  # Usage Page (Generic Desktop)
    0x09, 0x05,  # Usage (Game Pad)
    0xA1, 0x01,  # Collection (Application)
    0x05, 0x02,  # Usage Page (Simulation Controls)
    0x09, 0x01,  # Usage (Rudder)
    0x15, 0x00,  # Logical Minimum (0)
    0x26, 0xFF, 0x00,  # Logical Maximum (255)
    0x75, 0x08,  # Report Size (8)
    0x95, 0x01,  # Report Count (1)
    0x81, 0x02,  # Input (Data, Var, Abs)
    0xC0  # End Collection
])

# Create a HID device with the specified report descriptor
hid_device = usb_hid.Device(
    usage_page=0x01, usage=0x05, report_ids=[1], 
    in_report_lengths=[1], out_report_lengths=[0], 
    report_descriptor=HID_REPORT_DESCRIPTOR
)

# Add the device to the HID devices list
#usb_hid.enable((hid_device,))

# Initialize the ADC pin
adc = analogio.AnalogIn(ADC_PIN)

# Main loop
while True:
    # Read the ADC value (0-65535) and scale it to 0-255
    adc_value = int((adc.value / 65535.0) * 255)
    print(adc_value)  # This prints to the REPL, helpful for debugging
    # Pack the ADC value into a byte array
    report = bytearray([adc_value])
    # Send the report
    hid_device.send_report(report)
    led.value = True
    time.sleep(0.01)
    led.value = False

