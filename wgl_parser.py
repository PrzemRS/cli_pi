import re
import time
import sys
from tabulate import tabulate
import gpio
import time

def parse_wgl_header(file):
	PIOMAP_list=[]
	line = file.readline()
	# GROUND - 39, 34, 30, 25, 20, 14, 09, 06
	# DC POWER - 17, 04, 02, 01
	GPIO_list=[40, 38, 37, 36, 35, 33, 32 ,31, 29, 28, 27, 26, 24, 23, 22, 21, 19, 18, 16, 15, 13, 12, 11, 10, 8, 7, 5, 3]
	GPIO_idx=0
	while line:
		timeplate_line = re.search('^\s+"(\w+)"(\[\d+\])? := (input|output)\[(.*)\];', line)
		if timeplate_line:
			signal_name=timeplate_line.group(1)
			bus_idx=timeplate_line.group(2)
			signal_direction=timeplate_line.group(3)
			signal_timeplate=timeplate_line.group(4)
			if bus_idx is not None:
				signal_name=signal_name+bus_idx
			clock_timeplate = re.search('\d+\w+:D, \d+\w+:S, \d+\w+:D', signal_timeplate)
			if clock_timeplate:
				signal_direction='clock'
			if  GPIO_idx >= len(GPIO_list):
				print('Error: Too many ports in pattern file:', file.name)
				return (1, [])
			# TODO: check if port already saved
			PIOMAP_list.append({'port_name' : signal_name, 'direction' : signal_direction, 'GPIO' : GPIO_list[GPIO_idx]})
			GPIO_idx = GPIO_idx + 1

		break_line = re.search('pattern Chain_Scan_test\(',line)
		if break_line:
			gpio_status = gpio.setup(PIOMAP_list)
			return (gpio_status, PIOMAP_list)
		line = file.readline()

def parse_wgl_pattern(file,PIOMAP_list):
	line = file.readline()
	VECTOR_list=[]
	vector_done = False
	vector_multiline = False
	while line:
		vector_single_line = re.search('^\s*vector.* := \[ ([ 0|1|X|x|\-]+) \];\s*$', line)
		vector_done = False
		if vector_single_line:
			vector_done = True
			vector_line = vector_single_line.group(1)
		if vector_multiline:
			vector_multiple_line2 = re.search('^\s*([ 0|1|X|x|\-]+)\s*$', line)
			vector_multiple_line3 = re.search('^\s*([ 0|1|X|x|\-]+) \];\s*$', line)
			if vector_multiple_line2:
				vector_line = vector_line + " " + vector_multiple_line2.group(1)
			elif vector_multiple_line3:
				vector_line = vector_line + " " + vector_multiple_line3.group(1)
				vector_multiline = False
				vector_done = True
			else:
				vector_line = ""
				vector_multiline = False
				vector_done = False
		vector_multiple_line1 = re.search('^\s*vector.* := \[ ([ 0|1|X|x|\-]+)\s*$', line)
		if vector_multiple_line1:
			vector_line = vector_multiple_line1.group(1)
			vector_multiline = True
		if vector_done:
			Vector=list(vector_line.split())
			Vector_clocks=[]
			Vector_inputs=[]
			Vector_outputs=[]
			if len(Vector) == len(PIOMAP_list):
				for index,port in enumerate(PIOMAP_list):
					if port['direction'] == 'clock':
						Vector_clocks.append({'port' : port['port_name'], 'value' : Vector[index]})
					elif port['direction'] == 'input':
						Vector_inputs.append({'port' : port['port_name'], 'value' : Vector[index]})
					elif port['direction'] == 'output':
						Vector_outputs.append({'port' : port['port_name'], 'value' : Vector[index]})
				VECTOR_list.append({'clocks': Vector_clocks,'inputs' : Vector_inputs, 'outputs' : Vector_outputs})
		line = file.readline()
	return (0, VECTOR_list)

def get_GPIO_from_port_name(port_name,PIOMAP_list):
	for port in PIOMAP_list:
		if port['port_name']==port_name:
			return port['GPIO']
	return ""

def get_direction_from_port_name(port_name,PIOMAP_list):
	for port in PIOMAP_list:
		if port['port_name']==port_name:
			return port['direction']
	return ""

def execute_vector(vector,PIOMAP_list,vector_id):
	value_list = [port['value'] for port in vector['inputs']]
	status_pi = force_pi(PIOMAP_list, value_list, True)
	time.sleep(0.024)
	(status_po, outputs) = measure_po(PIOMAP_list, True)
	time.sleep(0.001)
	expected_outputs = [port['value'] for port in vector['outputs']]
	status_cmp = compare_vectors(outputs, expected_outputs)
	status_clk = pulse_clocks(vector,PIOMAP_list)
	status = status_pi or status_po or status_cmp or status_clk
	if status:
		print("Error: Vector", vector_id, "executed with errors.")
	return

def pulse_clocks(vector,PIOMAP_list):
	clock_list = [port['GPIO'] for port in PIOMAP_list if port['direction'] == 'clock']
	value_list = [port['value'] for port in vector['clocks']]
	gpio_status = 0
	if len(value_list) != len(clock_list):
		print('Error: value list length (', len(value_list), ') is different than number of clocks (', len(clock_list), ').')
		return 1
	else:
		clock_tuple = zip(clock_list, value_list)
		for clock, value in clock_tuple:
			gpio_status = gpio.set_pin_value(clock, value)
		time.sleep(0.050)
		for clock, value in clock_tuple:
			gpio_status = gpio.set_pin_value(clock, '0')
		time.sleep(0.005)
	return gpio_status

def execute_pattern(PIOMAP_list,VECTOR_list,from_idx,to_idx):
	execute_status = 0
	for idx in range(int(from_idx),int(to_idx)+1):
		print('Note: Executing vector:', idx)
		status = execute_vector(VECTOR_list[idx],PIOMAP_list,idx)
		execute_status = execute_status or status
	return execute_status

def report_vector(vector,PIOMAP_list):
	vector_data=[]
	#Inputs
	for idx,in_port in enumerate(vector['inputs']):
			GPIO=get_GPIO_from_port_name(in_port['port'], PIOMAP_list)
			direction=get_direction_from_port_name(in_port['port'], PIOMAP_list)
			vector_data.append([in_port['port'],  direction, GPIO, in_port['value']])
	#Outputs
	for idx,out_port in enumerate(vector['outputs']):
			GPIO=get_GPIO_from_port_name(out_port['port'],PIOMAP_list)
			direction=get_direction_from_port_name(out_port['port'], PIOMAP_list)
			vector_data.append([out_port['port'],  direction, GPIO, out_port['value']])
	#Clocks
	for idx,clock_port in enumerate(vector['clocks']):
			GPIO=get_GPIO_from_port_name(clock_port['port'],PIOMAP_list)
			direction=get_direction_from_port_name(clock_port['port'], PIOMAP_list)
			vector_data.append([clock_port['port'],  direction, GPIO, clock_port['value']])

	print(tabulate(vector_data,headers=['Port\nName', 'Type', 'GPIO', 'Value'],tablefmt='orgtbl'))
	return 0


def force_pi(PIOMAP_list,input_vector, show_report=True):
	inputs=[]
	force_PI_data=[]
	gpio_status = 0
	for port in PIOMAP_list:
		if port['direction']=='input':
			inputs.append({'port_name' : port['port_name'], 'GPIO': port['GPIO']})
	if len(inputs)==len(input_vector):
		for idx,in_port in enumerate(inputs):
			pin = in_port['GPIO']
			value = input_vector[idx]
			if value != '0' and value != '1':
				value = 'X'
			force_PI_data.append([in_port['port_name'], pin, value])
			gpio_status = gpio.set_pin_value(pin, value)
	else:
		print('Error: The arugment must have the same width as numer of input ports (',len(inputs),'). Argument length is (', len(input_vector), ').', sep='')
		return 1
	if show_report == True:
		print('Driving input ports:')
		print(tabulate(force_PI_data,headers=['Port\nName', 'GPIO', 'Value'],tablefmt='orgtbl'))
	return gpio_status

def measure_po(PIOMAP_list, show_report=True):
	captures=[]
	captured_values=[]
	measure_po_data=[]
	capture_status = 0
	for port in PIOMAP_list:
		if port['direction']=='output':
			(capture_status, captured_value)=gpio.get_pin_value(port['GPIO'])
			captured_value = str(captured_value)
			captured_values.append(captured_value)
			captures.append([port['port_name'], port['GPIO'], captured_value])
	if show_report == True:
		print('Capturing output ports:')
		print(tabulate(captures,headers=['Port\nName', 'GPIO', 'Value'],tablefmt='orgtbl'))
	return (capture_status, captured_value)

def Show_Mapping(PIOMAP_list):
	print(tabulate(PIOMAP_list,headers={'port_name' : 'Port\nName', 'direction' : 'Type', 'GPIO' : 'GPIO', 'init_val' : 'Init\nVal'},tablefmt='orgtbl'))
	return 0

def parse_wgl(filepath):
	file=open(filepath, 'r')
	(header_status, PIOMAP_list)=parse_wgl_header(file)
	(pattern_status, VECTOR_list)=parse_wgl_pattern(file, PIOMAP_list)
	parse_status = header_status or pattern_status
	return (parse_status, PIOMAP_list, VECTOR_list)

def parse_wgl_piomap(filepath):
	file=open(filepath, 'r')
	(parse_status, PIOMAP_list)=parse_wgl_header(file)
	return (parse_status, PIOMAP_list)

def compare_vectors(result_list, expected_list):
	if len(result_list) != len(expected_list):
		print('Error: result list length (', len(result_list), ') is different than expected list length (', len(expected_list), ').', sep='')
		return 1
	else:
		status = 0
		for result, expected in zip(result_list, expected_list):
			if result != expected and expected != 'X' and expected != 'x':
				print('Error: Miscompare at pin ',expected_list.index(expected) ,'.', sep='')
				print('       Expected value: ', expected, '. Result value: ', result, sep='')
				status = 1
		if status == 0:
			print('Note: No miscompares between results and expected values.')
		return status

def force_single_pin(PIOMAP_list, pin_name, value, show_report=True):
	pin_exists = False
	for pin in PIOMAP_list:
		if pin['port_name'] == pin_name:
			#print('[DEBUG] pin exist', pin_name)
			pin_exists = True
			pin_gpio = pin['GPIO']
			if pin['direction'] == 'output':
				print('Error: Pin', pin_name, 'is defined as output')
				return 1

	if pin_exists:
		gpio_status = gpio.set_pin_value(pin_gpio, value)
	else:
		print('Error: Pin', pin_name, 'does not exist.')
		return 1
	if show_report == True:
		print('Driving port:')
		print(tabulate([[pin_name, pin_gpio, value]],headers=['Port\nName', 'GPIO', 'Value'],tablefmt='orgtbl'))
	return gpio_status

def measure_single_pin(PIOMAP_list, pin_name, show_report=True):
	pin_exists = False
	for pin in PIOMAP_list:
		if pin['port_name'] == pin_name:
			#print('[DEBUG] pin exist', pin_name)
			pin_exists = True
			pin_gpio = pin['GPIO']
			if pin['direction'] == 'input' or pin['direction'] == 'clock':
				print('Error: Pin', pin_name, 'is defined as ', pin['direction'])
				return (1, 'X')

	if pin_exists:
		(gpio_status, value) = gpio.get_pin_value(pin_gpio)
	else:
		print('Error: Pin', pin_name, 'does not exist.')
		return (1, 'X')
	if show_report == True:
		print('Measuring port:')
		print(tabulate([[pin_name, pin_gpio, value]],headers=['Port\nName', 'GPIO', 'Value'],tablefmt='orgtbl'))
	return (gpio_status, value)
