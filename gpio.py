# import RPi.GPIO as GPIO

def setup(PIOMAP_list):
	# GPIO.setwarnings(False)
	# GPIO.cleanup()
	# GPIO.setmode(GPIO.BOARD)
	for port in PIOMAP_list:
		if (port['direction'] == 'input') or (port['direction'] == 'clock') :
			print('GPIO setup ', port['GPIO'], ' OUT')
			# GPIO.setup(port['GPIO'],GPIO.OUT)
		if port['direction'] == 'output':
			print('GPIO setup ', port['GPIO'], ' IN')
			# GPIO.setup(port['GPIO'],GPIO.IN)
	return 0

def set_pin_value(gpio, value):
	try:
		if value == '0':
			print('GPIO output', gpio, ' 0')
			# GPIO.output(gpio,GPIO.LOW)
		if value == '1':
			print('GPIO output', gpio, ' 1')
			# GPIO.output(gpio,GPIO.HIGH)
	except:
		print("Warning: Pin ", gpio, " was not set with value ", gpio_value)
		return 1
	return 0

def get_pin_value(gpio):
	value = 0
	try:
		print('GPIO input ', gpio)
		# value = GPIO.input(gpio)
	except:
		print("Error: Could not get value of pin ", gpio)
		return None
	return value

def exit():
	# GPIO.cleanup()
	return
