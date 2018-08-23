# import RPi.GPIO as GPIO

def setup(PIOMAP_list):
	# GPIO.setwarnings(False)
	# GPIO.cleanup()
	# GPIO.setmode(GPIO.BOARD)
	for port in PIOMAP_list:
		if port['direction'] == 'input':
			print('GPIO setup ', port['GPIO'], ' OUT')
			# GPIO.setup(port['GPIO'],GPIO.OUT)
		if port['direction'] == 'output':
			print('GPIO setup ', port['GPIO'], ' IN')
			# GPIO.setup(port['GPIO'],GPIO.IN)
	return 0

def set_pin_value(gpio, value):
	gpio_value = 0
	# gpio_value = GPIO.LOW
	if value == '0':
		gpio_value = 0
		# gpio_value = GPIO.LOW
	if value == '1':
		gpio_value = 1
		# gpio_value = GPIO.HIGH
	try:
		print('GPIO output', gpio, ' ', gpio_value)
		# GPIO.output(gpio,gpio_value)
	except:
		return 1
	return 0

def get_pin_value(gpio):
	value = 0
	try:
		print('GPIO input')
		# value = GPIO.input(gpio)
	except:
		return None
	return value

def exit():
	# GPIO.cleanup()
	return
