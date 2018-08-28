#!/usr/bin/env python

from __future__ import unicode_literals, print_function
import sys
import os.path
import datetime
import time
import re
import shlex # Library for obtaining arguments from string
from tabulate import tabulate # Library for printing tables
from prompt_toolkit import PromptSession # Library for command prompt
from prompt_toolkit.history import FileHistory
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.lexers import PygmentsLexer
from prompt_toolkit.styles import Style

import wgl_parser
from wgl_parser import *


#####################################################################################################################
#                                                                                                                   #
# Command list and command functions                                                                                #
#   This section contains:                                                                                          #
#     - command related functions; each function takes self dictionary as args[0]                                   #
#     - command list - list of dictionaries that contains command string, command help and function name            #
#     - error message dictionary that contains error messages for all cases                                         #
#                                                                                                                   #
#####################################################################################################################

################################################################
#
# Help fuction
#   Args:   [1] - target command for help; optional argument
#
################################################################
def helpFunction(*args):
	command_dictionary = args[0]
	command_name = command_dictionary["commandName"]

	# Check for parameters
	if len(args) > 2:
		print(error_dict["syntaxError"], command_name)
		return 1

	elif len(args) == 2:
		# Get daictionary fr selected command. If doesn't exist, provide error
		selected_command = []
		for d in command_list:
			if d['commandName'] == args[1]:
				selected_command = d
		if selected_command == []:
			print(error_dict["commandNotFound"])
			return 1
		else:
			print(tabulate([[selected_command["commandName"], selected_command["commandHelp"]]]))
			return 0

	else:
		command_list_for_help = []
		for command in command_list:
			command_list_for_help.append([command["commandName"], command["commandHelp"]])
		print(tabulate(command_list_for_help, headers=["Command name", "Help"]))
		return 0
################################################################

################################################################
#
# PrintVar
#   Args:   [1] - Variable to print; mandatory argument
#
################################################################
def printVarFunction(*args):
	command_dictionary = args[0]
	command_name = command_dictionary["commandName"]

	# Check for parameters
	if len(args) != 2:
		print(error_dict["syntaxError"], command_name)
		return 1
	else:
		print(args[1])
		return 0
################################################################

################################################################
#
# Read patterns
#   Args:   [1] - path to wgl pattern; mandatory argument
#
################################################################
def readPatternFunction(*args):
	command_dictionary = args[0]
	command_name = command_dictionary["commandName"]
	# Check for parameters
	if len(args) != 2:
		print(error_dict["syntaxError"], command_name)
		return 1
	else:
		# Read pattern here
		if os.path.isfile(args[1]):
			globals()['PIOMAP_list'],globals()['VECTOR_list']=wgl_parser.parse_wgl(args[1])
			return 0
		else:
			print('File ',args[1], 'not found')
			return 1
################################################################

################################################################
#
# Read PIOMAP
#   Args:   [1] - path to wgl pattern with PIOMAP; mandatory argument
#
################################################################
def readPIOMAPFunction(*args):
	command_dictionary = args[0]
	command_name = command_dictionary["commandName"]
	# Check for parameters
	if len(args) != 2:
		print(error_dict["syntaxError"], command_name)
		return 1
	else:
		# Read pattern here
		if os.path.isfile(args[1]):
			globals()['PIOMAP_list']=wgl_parser.parse_wgl_piomap(args[1])
			return 0
		else:
			print('File ',args[1], 'not found')
			return 1
################################################################

################################################################
#
# Execute patterns
#   Args:   [1] - mandatory argument; -vector OR -all
#           [2] - optional argument; range if 1st argument was -vector
#
################################################################
def executePatternFunction(*args):
	command_dictionary = args[0]
	command_name = command_dictionary["commandName"]
	# Check for parameters
	if globals()['VECTOR_list']=='':
		print(error_dict["noPattern"])
		return 1
	if len(args) == 4 and str(args[1]) == "-vector":
		wgl_parser.execute_pattern(globals()['PIOMAP_list'],globals()['VECTOR_list'],args[2],args[3])
		return 0
	elif len(args) == 2 and args[1] == "-all":
		# Execute all pattern vectors
		wgl_parser.execute_pattern(globals()['PIOMAP_list'],globals()['VECTOR_list'],0,len(globals()['VECTOR_list']))
		return 0

	else:
		print(error_dict["syntaxError"], command_name)
		return 1
################################################################

################################################################
#
# Report pinmap
#
################################################################
def reportPinmapFunction(*args):
	command_dictionary = args[0]
	command_name = command_dictionary["commandName"]
	if globals()['PIOMAP_list']=='':
		print(error_dict["noPinmap"])
		return 1
	# Check for parameters
	if len(args) > 1:
		print(error_dict["syntaxError"], command_name)
		return 1
	else:
		wgl_parser.Show_Mapping(globals()['PIOMAP_list'])
		return 0
################################################################

################################################################
#
# Report pattern
#
################################################################
def reportPatternFunction(*args):
	command_dictionary = args[0]
	command_name = command_dictionary["commandName"]
	# Check for parameters
	if globals()['VECTOR_list']=='':
		print(error_dict["noPattern"])
		return 1
	if len(args) > 1:
		print(error_dict["syntaxError"], command_name)
		return 1
	else:
		print('Pattern in memory has',len(globals()['VECTOR_list']),'vectors')
		return 0
################################################################

################################################################
#
# Report vector
#   Args:   [1] - vector; mandatory argument
#
################################################################
def reportVectorFunction(*args):
	command_dictionary = args[0]
	command_name = command_dictionary["commandName"]
	# Check for parameters
	if globals()['VECTOR_list']=='':
		print(error_dict["noPattern"])
		return 1
	if len(args) != 2:
		print(error_dict["syntaxError"], command_name)
		return 1
	else:
		print('Vector', args[1], ':')
		try:
			report_vector(globals()['VECTOR_list'][int(args[1])],globals()['PIOMAP_list'])
		except:
			print(error_dict["indexOutOfRange"])
			return 1
		return 0
################################################################

################################################################
#
# Apply shift
#   Args:   [1] - values to shift; mandatory argument
#           [2] - response, x when don't care; mandatory argument
#
################################################################
def applyShiftFunction(*args):
	command_dictionary = args[0]
	command_name = command_dictionary["commandName"]
	# Check for parameters
	if len(args) != 3:
		print(error_dict["syntaxError"], command_name)
		return 1
	else:
		# Apply shift and check response
		print("Hello from function applyShiftFunction")
		print("I was called with", len(args), "arguments:", args)
		print("Implement me here :)")
		return 0
################################################################

################################################################
#
# Apply capture
#
################################################################
def applyCaptureFunction(*args):
	command_dictionary = args[0]
	command_name = command_dictionary["commandName"]
	# Check for parameters
	if len(args) != 1:
		print(error_dict["syntaxError"], command_name)
		return 1
	else:
		# Apply capture
		print("Hello from function applyCaptureFunction")
		print("I was called with", len(args), "arguments:", args)
		print("Implement me here :)")
		return 0
################################################################

################################################################
#
# Apply unload
#   Args:   [1] - values to shift, x when don't care; mandatory argument
#           [2] - expected response; mandatory argument
#
################################################################
def applyUnloadFunction(*args):
	command_dictionary = args[0]
	command_name = command_dictionary["commandName"]
	# Check for parameters
	if len(args) != 3:
		print(error_dict["syntaxError"], command_name)
		return 1
	else:
		# Apply unload and check response
		print("Hello from function applyUnloadFunction")
		print("I was called with", len(args), "arguments:", args)
		print("Implement me here :)")
		return 0
################################################################

################################################################
#
# Force primary inputs
#   Args:   [1] - pi values, x when don't care; mandatory argument
#
################################################################
def forcePiFunction(*args):
	command_dictionary = args[0]
	command_name = command_dictionary["commandName"]
	if globals()['PIOMAP_list']=='':
		print(error_dict["noPinmap"])
		return 1
	# Check for parameters
	if len(args) != 2:
		print(error_dict["syntaxError"], command_name)
		return 1
	else:
		# Force PI
		wgl_parser.force_pi(globals()['PIOMAP_list'],args[1])
		return 0
################################################################

################################################################
#
# Measure primary outputs
#
################################################################
def measurePoFunction(*args):
	command_dictionary = args[0]
	command_name = command_dictionary["commandName"]
	if globals()['PIOMAP_list']=='':
		print(error_dict["noPinmap"])
		return 1
	# Check for parameters
	if len(args) != 1:
		print(error_dict["syntaxError"], command_name)
		return 1
	else:
		# Measure PO
		wgl_parser.measure_po(globals()['PIOMAP_list'])
		return 0
################################################################

################################################################
#
# iJTAG shift
#   Args:   [1] - values to shift; mandatory argument
#           [2] - response, x when don't care; mandatory argument
#
################################################################
def ijtagShiftFunction(*args):
	command_dictionary = args[0]
	command_name = command_dictionary["commandName"]

	# Regex for input string
	pattern = r'[^\.a-z0-9]'

	# Check for parameters
	if globals()['PIOMAP_list']=='':
		print(error_dict["noPinmap"])
		return 1
	if len(args) != 3 or re.search(pattern, str(args[1])) or re.search(pattern, str(args[2])):
		print(error_dict["syntaxError"], command_name)
		return 1
	else:
		# Apply iJTAG shift and check response
		values = args[1]
		expected_response = args[2]
		if len(values) != len(expected_response):
			print(error_dict["differentLengthValuesError"])
			return 1
		wgl_parser.force_single_pin(globals()['PIOMAP_list'], 'ijtag_sel', '1')
		tck_pulse()
		response = shift(values)
		update()
		capture()
		wgl_parser.force_single_pin(globals()['PIOMAP_list'], 'ijtag_sel', '0')
		status = wgl_parser.compare_vectors(response, expected_response)
		return status
################################################################
def tck_pulse():
	wgl_parser.force_single_pin(globals()['PIOMAP_list'], 'ijtag_tck', '1')
	time.sleep(0.050)
	wgl_parser.force_single_pin(globals()['PIOMAP_list'], 'ijtag_tck', '0')
	time.sleep(0.005)

def shift(values):
	response = ""
	wgl_parser.force_single_pin(globals()['PIOMAP_list'], 'ijtag_se', '1')
	for value in values:
		print("[DEBUG] Shift value: ", value)
		#if value not in ["x", "X"]:
			#wgl_parser.force_single_pin(globals()['PIOMAP_list'], 'ijtag_si', value)
		response += '0'
		 #wgl_parser.measure_single_pin(globals()['PIOMAP_list'], 'ijtag_so')
		print("[DEBUG] Captured values: ", response, "\n[DEBUG] Pulse tck")
		tck_pulse()
	wgl_parser.force_single_pin(globals()['PIOMAP_list'], 'ijtag_se', '0')
	return response

def update():
	wgl_parser.force_single_pin(globals()['PIOMAP_list'], 'ijtag_ue', '1')
	tck_pulse()
	wgl_parser.force_single_pin(globals()['PIOMAP_list'], 'ijtag_ue', '0')

def capture():
	wgl_parser.force_single_pin(globals()['PIOMAP_list'], 'ijtag_ce', '1')
	tck_pulse()
	wgl_parser.force_single_pin(globals()['PIOMAP_list'], 'ijtag_ce', '0')

################################################################
#
# iJTAG select
#   Args:   [1] - 1 - on OR 0 - off; mandatory argument
#
################################################################
def ijtagSelectFunction(*args):
	command_dictionary = args[0]
	command_name = command_dictionary["commandName"]
	# Check for parameters
	if globals()['PIOMAP_list']=='':
		print(error_dict["noPinmap"])
		return 1
	if len(args) != 2 or str(args[1]) not in ["0", "1"]:
		print(error_dict["syntaxError"], command_name)
		return 1
	else:
		# Apply iJTAG select value
		wgl_parser.force_single_pin(globals()['PIOMAP_list'], 'ijtag_sel', str(args[1]))
		return 0
################################################################

################################################################
#
# iJTAG se
#   Args:   [1] - 1 - on OR 0 - off; mandatory argument
#
################################################################
def ijtagSeFunction(*args):
	command_dictionary = args[0]
	command_name = command_dictionary["commandName"]
	# Check for parameters
	if globals()['PIOMAP_list']=='':
		print(error_dict["noPinmap"])
		return 1
	if len(args) != 2 or str(args[1]) not in ["0", "1"]:
		print(error_dict["syntaxError"], command_name)
		return 1
	else:
		# Apply iJTAG se value
		wgl_parser.force_single_pin(globals()['PIOMAP_list'], 'ijtag_se', str(args[1]))
		return 0
################################################################

################################################################
#
# iJTAG ce
#   Args:   [1] - 1 - on OR 0 - off; mandatory argument
#
################################################################
def ijtagCeFunction(*args):
	command_dictionary = args[0]
	command_name = command_dictionary["commandName"]
	# Check for parameters
	if globals()['PIOMAP_list']=='':
		print(error_dict["noPinmap"])
		return 1
	if len(args) != 2 or str(args[1]) not in ["0", "1"]:
		print(error_dict["syntaxError"], command_name)
		return 1
	else:
		# Apply iJTAG ce value
		wgl_parser.force_single_pin(globals()['PIOMAP_list'], 'ijtag_ce', str(args[1]))
		return 0
################################################################

################################################################
#
# Pulse tck
#
################################################################
def pulseTckFunction(*args):
	command_dictionary = args[0]
	command_name = command_dictionary["commandName"]
	# Check for pinmap availability
	if globals()['PIOMAP_list']=='':
		print(error_dict["noPinmap"])
		return 1
	# Check for parameters
	if len(args) > 1:
		print(error_dict["syntaxError"], command_name)
		return 1
	else:
		# Apply pulse tck
		tck_pulse()
		return 0
################################################################

################################################################
#
# dofile
#   Args:   [1] - dofile file path; mandatory argument
#
################################################################
def dofileFunction(*args):
	global print
	command_dictionary = args[0]
	command_name = command_dictionary["commandName"]
	global dofile_mode
	# Check for parameters
	if len(args) != 2:
		print(error_dict["syntaxError"], command_name)
		return 1
	else:
		file_path = args[1]
		# Check if dofile file exists, if no print an error
		if not os.path.isfile(file_path):
			print(error_dict["fileNotExists"], file_path)
			return 1
		else:
			# Open dofile and check if it is in read mode, then execute each command from it.
			dofile = open(file_path, "r")
			if dofile.mode == 'r':
				dofile_content = dofile.readlines()
				dofile.close()
				dofile_mode = True
				# Override print function to print // at the begining of the line
				old_print = print
				def my_decorator(func):
					def wrapped_func(*args,**kwargs):
						# Replace new line char to new line and //
						new_args = []
						[new_args.append(str(arg).replace("\n", "\n// ")) for arg in args]
						return func("//",*new_args,**kwargs)
					return wrapped_func

				print = my_decorator(print)
				# Execute each command from dofile
				for command in dofile_content:
					# If line contains command starting from // don't print command - it is not printable comment
					if command[:2] == "//" or command in ['\n', '\r\n']:
						continue
					else:
						print("command:", str(command).rstrip())
						# If line contains command starting from # just print line as a commend, do not execute it
						if command[0] != "#":
							result = commandValidator(command_list, command)
							if result != 0:
								# restore default print function and return with exit code
								print = old_print
								return result
		dofile_mode = False
		# restore default print function
		print = old_print
		return 0
################################################################

################################################################
#
# Exit
#
################################################################
def exitFunction(*args):
	command_dictionary = args[0]
	command_name = command_dictionary["commandName"]
	# Check for parameters
	if len(args) != 1:
		print(error_dict["syntaxError"], command_name)
		return 1
	else:
		print(info_dict["exit"])
		wgl_parser.gpio.exit()
		exit()
		return 0
################################################################

command_list = [
	{"commandName": "help",             "commandHelp": "This comand prints help and command list or help for provided command\n  Syntax: help [command_name]",                                                                      "commandFunction": helpFunction             },
	{"commandName": "printVar",         "commandHelp": "Use this command to print Variable.\n  Syntax printVar <variable>",                                                                                                         "commandFunction": printVarFunction         },
	{"commandName": "read_pattern",     "commandHelp": "Use this command to read wgl pattern.\n  Syntax read_pattern <pattern_path>",                                                                                               "commandFunction": readPatternFunction      },
	{"commandName": "read_pinmap",      "commandHelp": "Use this command to read wgl header with PIOMAP.\n  Syntax read_pinmap <pattern_path>",                                                                                     "commandFunction": readPIOMAPFunction       },
	{"commandName": "execute_pattern",  "commandHelp": "Use This command to execute pattern. Available options - run all patterns or vector range.\n  Syntax: execute_pattern -vector <range start> <range stop> | -all",           "commandFunction": executePatternFunction   },
	{"commandName": "report_pinmap",    "commandHelp": "Use this command to report pinmap\n  Syntax: report_pinmap",                                                                                                                "commandFunction": reportPinmapFunction     },
	{"commandName": "report_pattern",   "commandHelp": "Use this command to report pattern details\n  Syntax: report_pattern",                                                                                                      "commandFunction": reportPatternFunction    },
	{"commandName": "report_vector",    "commandHelp": "Use this command to report pattern vector details\n  Syntax: report_vector <vector>",                                                                                       "commandFunction": reportVectorFunction     },
	{"commandName": "apply_shift",      "commandHelp": "Use this command to apply shift procedure though flip flops\n  Syntax: apply_shift <value> <response>\n  Note: If some bits in response are don't care, mark it as x",      "commandFunction": applyShiftFunction       },
	{"commandName": "apply_capture",    "commandHelp": "Use this command to apply capture procedure from flip flops\n  Syntax: apply_capture",                                                                                      "commandFunction": applyCaptureFunction     },
	{"commandName": "apply_unload",     "commandHelp": "Use this command to apply unload procedure though flip flops\n  Syntax: unload <value> <response>\n  Note: If some bits in value are don't care, mark it as x",             "commandFunction": applyUnloadFunction      },
	{"commandName": "force_pi",         "commandHelp": "Use this command to force primary inputs. Provide values acording to pinmap.\n  Syntax: force_pi <value>\n  Example: force_pi 01x0X1",                                      "commandFunction": forcePiFunction          },
	{"commandName": "measure_po",       "commandHelp": "Use this command to measure primary output values\n  Syntax: measure_po",                                                                                                   "commandFunction": measurePoFunction        },
	{"commandName": "ijtag_shift",      "commandHelp": "Use this command to apply iJTAG shift procedure though TDR\n  Syntax: ijtag_shift <value> <response>\n  Note: If some bits in response are don't care, mark it as x",       "commandFunction": ijtagShiftFunction       },
	{"commandName": "ijtag_sel",        "commandHelp": "Use this command to force 0 or 1 value in ijtag_sel pin\n  Syntax: ijtag_sel 0 | 1",                                                                                     	"commandFunction": ijtagSelectFunction      },
	{"commandName": "ijtag_se",         "commandHelp": "Use this command to force 0 or 1 value in ijtag_se pin\n  Syntax: ijtag_se 0 | 1",                                                                                          "commandFunction": ijtagSeFunction          },
	{"commandName": "ijtag_ce",         "commandHelp": "Use this command to force 0 or 1 value in ijtag_ce pin\n  Syntax: ijtag_ce 0 | 1",                                                                                          "commandFunction": ijtagCeFunction          },
	{"commandName": "pulse_tck",        "commandHelp": "Use this command to pulse ijtag_tck clock once\n  Syntax: pulse_tck",                                                                                                       "commandFunction": pulseTckFunction         },
	{"commandName": "dofile",           "commandHelp": "Use this command to execute dofile\n  Syntax: dofile <dofile_file>",                                                                                                        "commandFunction": dofileFunction           },
	{"commandName": "exit",             "commandHelp": "Use this command to exit the tool\n  Syntax: exit",                                                                                                                         "commandFunction": exitFunction             },
]

error_dict = {
	"commandNotFound":  			"Error: Command not found. To check available commands type help",
	"validatorIssue":   			"Error: Something goes wrong with command parsing :(",
	"syntaxError":      			"Error: Syntax error. Check syntax using help",
	"dofileError":      			"Error: Dofile execution error. Dofile execution has been aborted.\n       Last command exit status:",
	"fileNotExists":    			"Error: Provided file doesn't exists. Check path for the file:\n      ",
	"indexOutOfRange":  			"Error: Vector of that range doesn't exist.",
	"noPattern":        			"Error: Use read_pattern to read wgl pattern first.",
	"noPinmap":         			"Error: Use read_pinmap or read_pattern to set pinout.",
	"differentLengthValuesError":	"Error: Shift value and expected response have to have the same length."
}

info_dict = {
	"exit":             "GoodBye!\nThank you for using Mentor tools.",
	"ctrlC":            "Press Ctrl-D or type exit to close the tool.",
}

#####################################################################################################################
#                                                                                                                   #
# Command validator                                                                                                 #
#   This function is used to validate user input, run command related function and pass all command args to it      #
#                                                                                                                   #
#####################################################################################################################
def commandValidator(command_list, input_string):
	# Collect all available commands
	available_commands = []
	for command in command_list:
		available_commands.append(command["commandName"])

	# Split input string to command and arguments, and remove command from the list
	all_arguments = shlex.split(input_string)
	command_name_string = all_arguments[0]
	all_arguments.remove(command_name_string)

	# Obtain command function
	if command_name_string not in available_commands:
		print(error_dict["commandNotFound"])
		return 1
	else:
		for commandDictionary in command_list:
			if commandDictionary['commandName'] == command_name_string:
				function = commandDictionary["commandFunction"]
				# Call command function with all arguments passed by user
				execution_result = function(commandDictionary, *all_arguments)
				return execution_result

		print(error_dict["validatorIssue"])
		return 1

#####################################################################################################################
#                                                                                                                   #
# Command prompt                                                                                                    #
#                                                                                                                   #
#####################################################################################################################

# Obtain all available commands and assign it into word completer
word_completer_list = []
for command in command_list:
	word_completer_list.append(command["commandName"])

command_completer = WordCompleter(word_completer_list, ignore_case=True)

# Disable dofile mode - this mode is used during execution commands from file
dofile_mode = False

def print_banner():
	now = datetime.datetime.now()
	print("//  Tessent ATEInsight  2018.4  ", now.strftime("%a %b %d %X %Y"))
	print("//                Copyright 2011-2018 Mentor Graphics Corporation")
	print("//")
	print("//                           All Rights Reserved.")
	return 0

# Command propmt main task
def main():
	print_banner()
	global dofile_mode
	global VECTOR_list
	global PIOMAP_list
	VECTOR_list=''
	PIOMAP_list=''
	session = PromptSession(completer=command_completer, complete_while_typing=True, history=FileHistory('.myhistory'), message='ATE> ')
	while True:
		try:
			text = session.prompt()
			if text is not "":
				result = commandValidator(command_list, text)
				if dofile_mode == True and result != 0:
					dofile_mode = False
					print(error_dict["dofileError"], result)
		except KeyboardInterrupt:
			print(info_dict["ctrlC"])
			continue  # Ctrl-C pressed. Try again.
		except EOFError:
			break  # Ctrl-D pressed.

	print(info_dict["exit"])

if __name__ == '__main__':
	main()
