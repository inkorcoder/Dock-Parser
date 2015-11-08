#!/usr/bin/env python
#-*- coding: utf-8 -*-

################################################################
#                    JSON PARSER
#
# --------------------------------------------------------------
# 				author: 	Inkor
# 				year: 		2015
# --------------------------------------------------------------
#
# This script can generate documentation from your project.
# There are all directives, wich this script can parse:
# 	-i, --input_folder - [relative path to folder] Input
# 	-o, --output_file  - [ralative path to file] Output
# 	-e, --exeptions    - [string] Exeptions
# 	-q, --quiet_mode   - [flag] Quiet mode
# 	-c, --cut_symbols  - [string] Cute symbols
#
# And here it is a better information:
# --------------------------------------------------------------
# NAME         | CAPTION                                       |
# --------------------------------------------------------------
# Input folder | Your project folder. All files in this folder |
#              | will be scaned. Path to this folder must be   |
#              | relative, for eample: [../back_to/this_foldr] |
# --------------------------------------------------------------
# Output file  | Relative path, where you need to creeate your |
#              | output file, for eample: [../up/myfile.json]  |
# --------------------------------------------------------------
# Exeptions    | This folders will be ignored. Just words      |
#              | with spaces, for example: [dist img myfoldr2] |
# --------------------------------------------------------------
# Quiet mode   | If enabled, results will not be written in    |
#              | console.                                      |
# --------------------------------------------------------------
# Cut symbols  | Symbols will be ignored. Each symbol must be  |
#              | escaped with '\' [\\n \\t \\r \#], NOT [\n \t]|
# --------------------------------------------------------------
#
# And here is an example:
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# python test.py -i ../apertura -o list.json -e dist .git -q -c \\n \\t \\r \#
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#
# [input] 				-i ../apertura
# [output] 				-o list.json
# [exeptions] 		-e dist .git
# [quiet mode]		-q
# [cuted symbols] -c \\n \\t \\r \#
#
################################################################

# Modules import
import sys, argparse, os, time, re



###############################################################
# Colors class
###############################################################

class color:
	HEADER 	= '\033[95m'
	OKBLUE 	= '\033[94m'
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL 		= '\033[91m'
	ENDC 		= '\033[0m'
	GREY 	= '\033[1;30m'

	def disable(self):
		self.HEADER = ''
		self.OKBLUE = ''
		self.OKGREEN = ''
		self.WARNING = ''
		self.FAIL = ''
		self.ENDC = ''



###############################################################
# Arguments parsing
###############################################################

# Include argparser. We can parse the keys in command line.
parser = argparse.ArgumentParser(add_help=True)

# This arguments will be used
# [INPUT]
parser.add_argument(
	"-i", "--input_folder",
	help 		= "Input folder",
	default = False
)
# [OUTPUT]
parser.add_argument(
	"-o", "--output_file",
	help 		= "Output JSON file",
	default = False
)
# [EXEPTIONS]
parser.add_argument(
	"-e", "--exeptions",
	help 		= "Add files or folders, which not to be documented.",
	nargs 	= "+",
	default = False
)
# [QUIET MODE]
parser.add_argument(
	"-q", "--quiet_mode",
	help 		= "Disable not used files log.",
	nargs 	= "?",
	default = False
)
# [SYMBOLS]
parser.add_argument(
	"-c", "--cut_symbols",
	help 		= "These characters will be stripped from names, captions and other. !!!IMPORTANT!!! - you must shield some characters (for example: \# - good, # - error. \\\\n - good, \\n - error).",
	nargs 	= "+",
	default = False
)

# Init argparse
args 					= parser.parse_args()

# Sum of all modules,
# [0] - by default
total_modules = 0




#################################################################
# Functions for parsing.                                        #
#################################################################

# [MODULE]
def get_module(inp):
	title 	= re.findall(r'@module.*?title:(.*?)\*n', inp, re.MULTILINE|re.DOTALL)
	typ 		= re.findall(r'@module.*?type:(.*?)\*n', inp, re.MULTILINE|re.DOTALL)
	caption = re.findall(r'@module.*?caption:(.*?)\*n', inp, re.MULTILINE|re.DOTALL)
	return [title,caption,typ]

# [PROPERTY]
def get_module_properties(inp):
	name 		= re.findall(r'@property.*?name:(.*?)\*n', inp, re.MULTILINE|re.DOTALL)
	caption = re.findall(r'@property.*?caption:(.*?)\*n', inp, re.MULTILINE|re.DOTALL)
	return [name,caption]

# [METHOD]
def get_module_methods(inp):
	name 				= re.findall(r'@method.*?name:(.*?)\*n', inp, re.MULTILINE|re.DOTALL)
	caption 		= re.findall(r'@method.*?caption:(.*?)\*n', inp, re.MULTILINE|re.DOTALL)
	arguments 	= re.findall(r'@method.*?arguments:(.*?)\*n', inp, re.MULTILINE|re.DOTALL)
	returns 		= re.findall(r'@method.*?return:(.*?)\*n', inp, re.MULTILINE|re.DOTALL)
	return [name,caption,arguments,returns]

# [MIXIN]
def get_module_mixins(inp):
	name 				= re.findall(r'@mixin.*?name:(.*?)\*n', inp, re.MULTILINE|re.DOTALL)
	caption 		= re.findall(r'@mixin.*?caption:(.*?)\*n', inp, re.MULTILINE|re.DOTALL)
	arguments 	= re.findall(r'@mixin.*?arguments:(.*?)\*n', inp, re.MULTILINE|re.DOTALL)
	returns 		= re.findall(r'@mixin.*?return:(.*?)\*n', inp, re.MULTILINE|re.DOTALL)
	return [name,caption,arguments,returns]

# [PLUGIN]
def get_module_plugins(inp):
	name 		= re.findall(r'@plugin.*?name:(.*?)\*n', inp, re.MULTILINE|re.DOTALL)
	caption = re.findall(r'@plugin.*?caption:(.*?)\*n', inp, re.MULTILINE|re.DOTALL)
	return [name,caption]



#################################################################
# Parse keys function                                           #
#################################################################
def parse_keys(_file, _output, _status, _quiet, _file_name, _path):

	# Open input file and read it
	_input_file = open(_file)
	input_file 	= _input_file.read()

	# Find out, has it a '@module' directive
	match = re.search('@module', input_file)

	# If it has a '@module' directive
	if match:

		# Get total modules counter and write log with other color
		global total_modules
		total_modules += 1

		print("> "+color.OKBLUE+_file+color.ENDC+" : "+color.GREY+str(len(input_file))+color.ENDC)
		time.sleep(0.3)

		# Head of the module, we are getting it from file info
		_output.write("\n\r\n\r\t{")
		_output.write("\n\r\t\t\"filename\": \""+str(_file_name)+"\",\n\r")
		_output.write("\t\t\"path\":     \""+str(_path)+"\",\n\r")
		_output.write("\t\t\"file\":     \""+str(_file)+"\",\n\r")
		_output.write("\t\t\"size\":     \""+str(os.path.getsize(_file))+"\",\n\r")
		_output.write("\t\t\"length\":   \""+str(len(input_file))+"\"")

		# If we must cut some symbols, we need to create pattern
		global args
		if args.cut_symbols != False:
			regexp = "|"
			for c in args.cut_symbols:
				regexp += c+"|"
			input_ = re.sub("^\s+"+regexp+"\s+$", '', str(input_file))
		# Or, leave it as string
		else:
			input_ = str(input_file)

		module_properties = get_module_properties(input_)
		module_methods 		= get_module_methods(input_)
		module_mixins 		= get_module_mixins(input_)
		module_plugins 		= get_module_plugins(input_)


		# -----------------------------------------------------------
		# Parse module. We are getting info from function
		# -----------------------------------------------------------
		module = get_module(input_)
		module_names = ['title','caption','type']
		i = 0
		for g in module:
			_output.write(",\n\r\t\t\""+module_names[i]+"\":     \""+g[0]+"\"")
			i += 1

		# -----------------------------------------------------------
		# Parse properties. We are getting info from function
		# -----------------------------------------------------------
		if len(module_properties[0]) > 0:
			_output.write(",\n\r\n\r\t\t\"properties\": [\n\r")
			i = 0
			# Write each property information
			while (i < len(module_properties[0])):
				_output.write("\n\r\t\t\t{\"name\": \""+module_properties[0][i]+"\", \"caption\": \""+module_properties[1][i]+"\"}")
				if (i+1) < len(module_properties[0]):
					_output.write(',')
				i += 1
			_output.write("\n\r\t\t]")

		# -----------------------------------------------------------
		# Parse methods. We are getting info from function
		# -----------------------------------------------------------
		if len(module_methods[0]) > 0:
			_output.write(",\n\r\n\r\t\t\"methods\": [\n\r")
			i = 0
			# Write each property information
			while (i < len(module_methods[0])):
				_output.write("\n\r\t\t\t{\n\r\t\t\t\t\"name\":      \""+module_methods[0][i]+"\",\n\r\t\t\t\t\"caption\":   \""+module_methods[1][i]+"\",\n\r\t\t\t\t\"arguments\": \""+module_methods[2][i]+"\",\n\r\t\t\t\t\"returns\":   \""+module_methods[3][i]+"\"\n\r\t\t\t}")
				if (i+1) < len(module_methods[0]):
					_output.write(',')
				i += 1
			_output.write("\n\r\t\t]")

		# -----------------------------------------------------------
		# Parse mixins. We are getting info from function
		# -----------------------------------------------------------
		if len(module_mixins[0]) > 0:
			_output.write(",\n\r\n\r\t\t\"mixins\": [\n\r")
			i = 0
			# Write each property information
			while (i < len(module_mixins[0])):
				_output.write("\n\r\t\t\t{\"name\":      \""+module_mixins[0][i]+"\",\n\r\t\t\t\t\"caption\":   \""+module_mixins[1][i]+"\",\n\r\t\t\t\t\"arguments\": \""+module_mixins[2][i]+"\",\n\r\t\t\t\t\"returns\":   \""+module_mixins[3][i]+"\"\n\r\t\t\t}")
				if (i+1) < len(module_mixins[0]):
					_output.write(',')
				i += 1
			_output.write("\n\r\t\t]")

		# -----------------------------------------------------------
		# Parse plugins. We are getting info from function
		# -----------------------------------------------------------
		if len(module_plugins[0]) > 0:
			_output.write(",\n\r\n\r\t\t\"plugins\": [\n\r")
			i = 0
			# Write each property information
			while (i < len(module_plugins[0])):
				_output.write("\n\r\t\t\t{\"name\": \""+module_plugins[0][i]+"\", \"caption\": \""+module_plugins[1][i]+"\"}")
				if (i+1) < len(module_plugins[0]):
					_output.write(',')
				i += 1
			_output.write("\n\r\t\t]")


		# end
		if _status == False:
			_output.write("\n\r\t},")
		else:
			_output.write("\n\r\t}")

	# If it hasn't a '@module' directive, we are writing
	# file path into log
	else:
		if args.quiet_mode == False:
			print("   "+_file)
			time.sleep(0.05)




#################################################################
# Main function                                                 #
#################################################################
total_modules_all = 0
total_modules 		= 0
def create_output(inp, outp, quiet):

	# Some vars
	filesCount 				= 0
	dirsCount 				= 0
	removedFilesCount = 0
	removedDirsCount 	= 0

	# Begining of output
	output = open(outp, 'w')
	output.write("[")

	# -------------------------------------------------------------
	# First, we need to count all modules
	# -------------------------------------------------------------
	global total_modules_all
	for dirname, dirnames, filenames in os.walk(inp):
		# Open input file and read it
		for filename in filenames:
			_input_file = open(os.path.join(dirname, filename))
			input_file 	= _input_file.read()
			# Find out, has it a '@module' directive
			match = re.search('@module', input_file)
			# If it has a '@module' directive
			if match:
				total_modules_all += 1
		# If we have exeptions, we need to delete exeptions from folders list
		if args.exeptions:
			for exep in args.exeptions:
				# If it is dir
				if exep in dirnames:
					removedDirsCount += 1
					dirnames.remove(exep)
				# And if it's file
				if exep in filenames:
					removedFilesCount += 1
					filenames.remove(exep)
	# -------------------------------------------------------------


	# Check all dirs and files in input folder
	for dirname, dirnames, filenames in os.walk(inp):

		# If it is dir
		for subdirname in dirnames:
			dirsCount += 1

		# If it is file
		for filename in filenames:
			filesCount += 1
			# Check, is it the last file and go to parsing
			parse_keys(os.path.join(dirname, filename), output, (False if total_modules < total_modules_all-1 else True), quiet, filename, dirname)

		# If we have exeptions, we need to delete exeptions from folders list
		if args.exeptions:
			for exep in args.exeptions:
				# If it is dir
				if exep in dirnames:
					removedDirsCount += 1
					dirnames.remove(exep)
				# And if it's file
				if exep in filenames:
					removedFilesCount += 1
					filenames.remove(exep)

	# End of output
	output.write("\n\r]")

	# If we have some modules
	if total_modules_all > 0:
		print("\n\rModules created: "+str(total_modules_all))
	# Oh, no... :((
	else:
		print("\n\rIt's no gived modules.")

	# And, full information
	print(
		"File(s): "+str(filesCount)+"   Dir(s): "+str(dirsCount)+"   "+
		"Exeptions: "+str(removedFilesCount)+"file(s), "+
		str(removedDirsCount)+"dir(s)\n\r")

	return inp+outp



###############################################################
# Main checking
###############################################################

# If we have input folder
if args.input_folder:

	# Print input folder
	print("\n\r <-- "+color.HEADER+args.input_folder+color.ENDC)

	# If we have output file path
	if args.output_file:

		# Print output file path
		print(" --> "+color.OKGREEN+args.output_file+color.ENDC+"\n\r")
		# And start parsing
		create_output(args.input_folder, args.output_file, args.quiet_mode)

	# So, we need output file path
	else:
		print("\n\r"+color.WARNING+"I need output file!"+color.ENDC+"\n\r")

# Or, we need input folder
else:
	print("\n\r"+color.WARNING+"I need input folder and output file!"+color.ENDC+"\n\r")