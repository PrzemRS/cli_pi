import re
import time
import sys
from tabulate import tabulate
import gpio
import time

def parse_wgl_header(file):
	PIOMAP_list=[]
	line = file.readline()
	GPIO_list=[40, 38, 37, 36, 35, 33, 32 ,31, 29, 28]
	GPIO_idx=0
	while line:
		signal_line = re.search('^\s+"(\w+)" : (input|output)(?: initialp\[(\w+)\])?;', line)
		if signal_line:
			signal_name=signal_line.group(1)
			signal_direction=signal_line.group(2)
			if signal_direction == 'input':
				if signal_line.group(3) == 'N':
					signal_init_val='0'
			else:
				signal_init_val='X'

			#PIOMAP_list.append({'port_name' : signal_name, 'direction' : signal_direction, 'GPIO' : GPIO_list[GPIO_idx], 'init_val' : signal_init_val, 'timeplate' : ''})
			PIOMAP_list.append({'port_name' : signal_name, 'direction' : signal_direction, 'GPIO' : GPIO_list[GPIO_idx], 'init_val' : signal_init_val})
			GPIO_idx = GPIO_idx + 1
			if  GPIO_idx >= len(GPIO_list):
				print('Error: Too many ports in pattern file: ',filepath)
				return 1

		timeplate_line = re.search('^\s+"(\w+)" := (input|output)\[(.*)\];', line)
		if timeplate_line:
			signal_name=timeplate_line.group(1)
			signal_direction=timeplate_line.group(2)
			signal_timeplate=timeplate_line.group(3)
			for idx,port in enumerate(PIOMAP_list):
				if port['port_name']==signal_name:
					#PIOMAP_list[idx]['timeplate']=signal_timeplate
					clock_timeplate = re.search('\d+\w+:D, \d+\w+:S, \d+\w+:D', signal_timeplate)
					if clock_timeplate:
						PIOMAP_list[idx]['direction']='clock'


		break_line = re.search('pattern Chain_Scan_test\(',line)
		if break_line:
			gpio.setup(PIOMAP_list)
			return PIOMAP_list

		line = file.readline()

def parse_wgl_pattern(file,PIOMAP_list):
	line = file.readline()
	VECTOR_list=[]
	while line:
		vector_line = re.search('vector.* := \[ ([ \w]+) \];', line)
		if vector_line:
			Vector=list(vector_line.group(1).split())
			Vector_clocks=[]
			Vector_inputs=[]
			Vector_outputs=[]
			for index,port in enumerate(PIOMAP_list):
				if port['direction'] == 'clock':
					Vector_clocks.append({'port' : port['port_name'], 'value' : Vector[index]})
				elif port['direction'] == 'input':
					Vector_inputs.append({'port' : port['port_name'], 'value' : Vector[index]})
				elif port['direction'] == 'output':
					Vector_outputs.append({'port' : port['port_name'], 'value' : Vector[index]})
			VECTOR_list.append({'clocks': Vector_clocks,'inputs' : Vector_inputs, 'outputs' : Vector_outputs})
		line = file.readline()
	return VECTOR_list

def get_GPIO_from_port_name(port_name,PIOMAP_list):
	for port in PIOMAP_list:
		if port['port_name']==port_name:
			return port['GPIO']
	return 1

def get_direction_from_port_name(port_name,PIOMAP_list):
	for port in PIOMAP_list:
		if port['port_name']==port_name:
			return port['direction']
	return 1

def execute_vector(vector,PIOMAP_list):
	value_list = [port['value'] for port in vector['inputs']]
	#print("[DEBUG] pattern inputs ", value_list)
	force_pi(PIOMAP_list, value_list, True)
	time.sleep(0.024)
	outputs = measure_po(PIOMAP_list, True)
	#print("[DEBUG] GPIO output values ", outputs)
	time.sleep(0.001)
	expected_outputs = [port['value'] for port in vector['outputs']]
	#print("[DEBUG] expected outputs ", expected_outputs)
	compare_vectors(outputs, expected_outputs)
	pulse_clocks(vector,PIOMAP_list)
	return 0

#def drive_inputs(value_list,PIOMAP_list):
#	gpio_list = [port['GPIO'] for port in PIOMAP_list if port['direction'] == 'input']
#	#print("[DEBUG] GPIO inputs ", gpio_list)
#	if len(value_list) != len(gpio_list):
#		print('Error: value list length (', len(value_list), ') is different than number of inputs (', len(gpio_list), ').')
#		return 1
#	else:
#		for pin, value in zip(gpio_list, value_list):
#			gpio.set_pin_value(pin, value)
#	return 0


#def capture_outputs(PIOMAP_list):
#	outputs = []
#	gpio_list = [port['GPIO'] for port in PIOMAP_list if port['direction'] == 'output']
#	#print("[DEBUG] GPIO outputs ", gpio_list)
#	for pin in gpio_list:
#		outputs.append(gpio.get_pin_value(pin))
#	print(outputs)
#	return outputs

def pulse_clocks(vector,PIOMAP_list):
	clock_list = [port['GPIO'] for port in PIOMAP_list if port['direction'] == 'clock']
	value_list = [port['value'] for port in vector['clocks']]
	print("[DEBUG] GPIO clocks ", clock_list)
	print("[DEBUG] GPIO clocks value ", value_list)
	if len(value_list) != len(clock_list):
		print('Error: value list length (', len(value_list), ') is different than number of clocks (', len(clock_list), ').')
		return 1
	else:
		clock_tuple = zip(clock_list, value_list)
		for clock, value in clock_tuple:
			#print("[DEBUG] Rising edge")
			gpio.set_pin_value(clock, value)
		time.sleep(0.050)
		for clock, value in clock_tuple:
			#print("[DEBUG] Falling edge")
			gpio.set_pin_value(clock, '0')
		time.sleep(0.005)
	return 0

def execute_pattern(PIOMAP_list,VECTOR_list,from_idx,to_idx):
	for idx in range(int(from_idx),int(to_idx)+1):
		print('Note: Executing vector:', idx)
		execute_vector(VECTOR_list[idx],PIOMAP_list)


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


def force_pi(PIOMAP_list,input_vector, show_report=True):
	inputs=[]
	force_PI_data=[]
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
			gpio.set_pin_value(pin, value)
	else:
		print('Error: The arugment must have the same width as numer of input ports (',len(inputs),'). Argument length is (', len(input_vector), ').', sep='')
		return 1
	if show_report == True:
		print('Driving input ports:')
		print(tabulate(force_PI_data,headers=['Port\nName', 'GPIO', 'Value'],tablefmt='orgtbl'))
	return 0

def measure_po(PIOMAP_list, show_report=True):
	captures=[]
	captured_values=[]
	measure_po_data=[]
	for port in PIOMAP_list:
		if port['direction']=='output':
			captured_value=str(gpio.get_pin_value(port['GPIO']))
			captured_values.append(captured_value)
			captures.append([port['port_name'], port['GPIO'], captured_value])
	if show_report == True:
		print('Capturing output ports:')
		print(tabulate(captures,headers=['Port\nName', 'GPIO', 'Value'],tablefmt='orgtbl'))
	return captured_values

def Show_Mapping(PIOMAP_list):
	print(tabulate(PIOMAP_list,headers={'port_name' : 'Port\nName', 'direction' : 'Type', 'GPIO' : 'GPIO', 'init_val' : 'Init\nVal'},tablefmt='orgtbl'))
	return

def parse_wgl(filepath):
	file=open(filepath, 'r')
	PIOMAP_list=parse_wgl_header(file)
	VECTOR_list=parse_wgl_pattern(file, PIOMAP_list)
	return PIOMAP_list,VECTOR_list

def parse_wgl_piomap(filepath):
	file=open(filepath, 'r')
	PIOMAP_list=parse_wgl_header(file)
	return PIOMAP_list

def compare_vectors(result_list, expected_list):
	if len(result_list) != len(expected_list):
		print('Error: result list length (', len(result_list), ') is different than expected list length(', len(expected_list), ').')
		return 1
	else:
		status = 0
		for result, expected in zip(result_list, expected_list):
			if result != expected and expected != 'X' and expected != 'x':
				print('Error: Miscompare at pin ',expected_list.index(expected) ,'.', sep='')
				print('       Expected value: ', expected, '. Result value: ', result, sep='')
				result = 1
		if status == 0:
			print('Note: No miscompares between results and expected values.')
		return status
		


