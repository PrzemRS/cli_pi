import re
import time
import sys
from tabulate import tabulate
import gpio

def parse_wgl_header(file):
	PIOMAP_list=[]
	line = file.readline()
	#GPIO_list=['GPIO0', 'GPIO1', 'GPIO2', 'GPIO3', 'GPIO4', 'GPIO5', 'GPIO6', 'GPIO7', 'GPIO8', 'GPIO9', 'GPIO10']
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
				print('Too many ports in pattern file: ',filepath)
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
	#Drive Inputs
	for idx,in_port in enumerate(vector['inputs']):
			GPIO=get_GPIO_from_port_name(in_port['port'], PIOMAP_list)
			print('Driving', in_port['port'], GPIO, in_port['value'])
			gpio.set_pin_value(GPIO, in_port['value'])
	#Capture Outputs
	for idx,out_port in enumerate(vector['outputs']):
		if out_port['value'] != 'X':
			GPIO=get_GPIO_from_port_name(out_port['port'],PIOMAP_list)
			print('Capturing', out_port['port'], GPIO, out_port['value'])
	#Pulse Clocks Posedge
	for idx,clock_port in enumerate(vector['clocks']):
			GPIO=get_GPIO_from_port_name(clock_port['port'],PIOMAP_list)
			print('Rising Edge', clock_port['port'], GPIO, clock_port['value'])
	#Pulse Clocks Negedge
	for idx,clock_port in enumerate(vector['clocks']):
			GPIO=get_GPIO_from_port_name(clock_port['port'],PIOMAP_list)
			print('Falling Edge', clock_port['port'], GPIO,'0')

def execute_pattern(PIOMAP_list,VECTOR_list,from_idx,to_idx):
	for idx in range(int(from_idx),int(to_idx)+1):
		print('Vector : ', idx)
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


def force_Pi(PIOMAP_list,input_vector):
	inputs=[]
	force_PI_data=[]
	for port in PIOMAP_list:
		if port['direction']=='input':
			inputs.append({'port_name' : port['port_name'], 'GPIO': port['GPIO']})
	if len(inputs)==len(input_vector):
		for idx,in_port in enumerate(inputs):
			force_PI_data.append([in_port['port_name'], in_port['GPIO'], input_vector[idx]])
	else:
		print('The arugment must have the same width as numer of input ports (',len(inputs),'). Argument length is (', len(input_vector), ')')
		return 1
	print('Driving input ports:')
	print(tabulate(force_PI_data,headers=['Port\nName', 'GPIO', 'Value'],tablefmt='orgtbl'))
	return 0

def measure_po(PIOMAP_list):
	captures=[]
	measure_po_data=[]
	for port in PIOMAP_list:
		if port['direction']=='output':
			captured_value='X'
			captures.append([port['port_name'], port['GPIO'], captured_value])
	print('Capturing output ports:')
	print(tabulate(captures,headers=['Port\nName', 'GPIO', 'Value'],tablefmt='orgtbl'))
	return 0

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
		result = 0
		for result, expected in zip(result_list, expected_list):
			if result != expected and expected != 'X' and expected != 'x':
				print('Error: Miscompare at ',expected_list.index(expected) ,' pin.')
				print('       Expected value: ', expected, ' result value: ', result)
				result = 1
		return result

#if __name__ == '__main__':

#   PIOMAP_list,VECTOR_list=parse_wgl('pattern.wgl')
#   Show_Mapping(PIOMAP_list)

	#execute_pattern(VECTOR_list,0,len(VECTOR_list))
#   execute_pattern(VECTOR_list,0,3)
	#for Vector in VECTOR_list:
	#   print(Vector)
	##Show_Mapping(Pattern_dict,PIOMAP_list)
	#input("Press Enter to continue...")
	#Pattern=[]
	#Pattern_transcript=[]
	#parse_SVF_pattern(filepath,Pattern_dict,PIOMAP_list,Pattern,Pattern_transcript)
	#execute_pattern(Pattern_dict,PIOMAP_list,Pattern,0)


	#print(Pattern)
#
#   #print(Pattern[0][0])
	#print(Pattern[0][1])
	#for transcript_line in Pattern_transcript:
	#   print(transcript_line, end='')
