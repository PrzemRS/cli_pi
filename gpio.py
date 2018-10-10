try:
	import RPi.GPIO as GPIO
	gpio_error = False
except:
	print("Error: Could not import RPi.GPIO. Some functions will not be available.")
	gpio_error = True

def setup(PIOMAP_list):
	if globals()['gpio_error']:
		return 1
	GPIO.setwarnings(False)
	GPIO.cleanup()
	GPIO.setmode(GPIO.BOARD)
	for port in PIOMAP_list:
		try:
			if (port['direction'] == 'input') or (port['direction'] == 'clock') :
				GPIO.setup(port['GPIO'],GPIO.OUT)
			if port['direction'] == 'output':
				GPIO.setup(port['GPIO'],GPIO.IN)
		except:
			print("Error: GPIO pin ", port['GPIO'], " cannot be set.",sep='')
			return 1
	return 0

def set_pin_value(gpio, value):
	if globals()['gpio_error']:
		print("Error: Pin ", gpio, " was not set with value ", value, ".",sep='')
		return 1
	try:
		if value == '0':
			GPIO.output(gpio,GPIO.LOW)
		if value == '1':
			GPIO.output(gpio,GPIO.HIGH)
	except:
		print("Error: Pin ", gpio, " was not set with value ", value, ".",sep='')
		return 1
	return 0

def get_pin_value(gpio):
	if globals()['gpio_error']:
		print("Error: Could not get value of pin ", gpio, ".",sep='')
		return (1, 'X')
	value = 0
	try:
		value = GPIO.input(gpio)
	except:
		print("Error: Could not get value of pin ", gpio, ".",sep='')
		return (1, 'X')
	return (0, value)

def exit():
	if globals()['gpio_error']:
		return 1
	GPIO.cleanup()
	return 0
