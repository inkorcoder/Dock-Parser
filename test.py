#!/usr/bin/env python
#-*- coding: utf-8 -*-
# python test.py -i ../apertura -o test.json -q -e dist -c \\n \\r \\# \\t

# @module
# ┝ title:{{}}
# ┝ type:{{}}
# ┝ caption:{{}}
# ┝ @property
# ╎ ┝ name:{{}}
# ╎ ┕ caption:{{}}
# ┝ @method
# ╎ ┝ name:{{}}
# ╎ ┝ caption:{{}}
# ╎ ┝ argumants:{{}}
# ╎ ┕ return:{{}}
# ┝ @mixin
# ╎ ┝ name:{{}}
# ╎ ┝ caption:{{}}
# ╎ ┝ argumants:{{}}
# ╎ ┕ return:{{}}
# ┕ @plugin
#   ┝ name:{{}}
#   ┕ caption:{{}}

# import
import sys, argparse, os, time, re

class color:
	HEADER 	= '\033[95m'
	OKBLUE 	= '\033[94m'
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL 		= '\033[91m'
	ENDC 		= '\033[0m'

	def disable(self):
		self.HEADER = ''
		self.OKBLUE = ''
		self.OKGREEN = ''
		self.WARNING = ''
		self.FAIL = ''
		self.ENDC = ''

# include parser
parser = argparse.ArgumentParser(add_help=True)

# input
parser.add_argument("-i","--input_folder",help="Input folder",default=False)
# output
parser.add_argument("-o","--output_file",help="Output JSON file",default=False)
# exeptions
parser.add_argument("-e", "--exeptions",help="Add files or folders, which not to be documented.",nargs="+",default=False)
# quiet mode
parser.add_argument("-q", "--quiet_mode",help="Disable not used files log.",nargs="?",default=False)
# cut symbols
parser.add_argument("-c", "--cut_symbols",help="These characters will be stripped from names, captions and other. !!!IMPORTANT!!! - you must shield some characters (for example: \# - good, # - error. \\\\n - good, \\n - error).",nargs="+",default=False)

# argparser
args = parser.parse_args()

# total count of modules
total_modules = 0

# module parsing
def get_module(inp):
	title 	= re.findall(r'@module.*?title:(.*?)\*n', inp, re.MULTILINE|re.DOTALL)
	typ 	= re.findall(r'@module.*?type:(.*?)\*n', inp, re.MULTILINE|re.DOTALL)
	caption = re.findall(r'@module.*?caption:(.*?)\*n', inp, re.MULTILINE|re.DOTALL)
	return [title,caption,typ]

# properties parsing
def get_module_properties(inp):
	name 		= re.findall(r'@property.*?name:(.*?)\*n', inp, re.MULTILINE|re.DOTALL)
	caption = re.findall(r'@property.*?caption:(.*?)\*n', inp, re.MULTILINE|re.DOTALL)
	return [name,caption]

# methods parsing
def get_module_methods(inp):
	name 			= re.findall(r'@method.*?name:(.*?)\*n', inp, re.MULTILINE|re.DOTALL)
	caption 	= re.findall(r'@method.*?caption:(.*?)\*n', inp, re.MULTILINE|re.DOTALL)
	arguments = re.findall(r'@method.*?arguments:(.*?)\*n', inp, re.MULTILINE|re.DOTALL)
	returns 		= re.findall(r'@method.*?return:(.*?)\*n', inp, re.MULTILINE|re.DOTALL)
	return [name,caption,arguments,returns]

# mixins parsing
def get_module_mixins(inp):
	name 			= re.findall(r'@mixin.*?name:(.*?)\*n', inp, re.MULTILINE|re.DOTALL)
	caption 	= re.findall(r'@mixin.*?caption:(.*?)\*n', inp, re.MULTILINE|re.DOTALL)
	arguments = re.findall(r'@mixin.*?arguments:(.*?)\*n', inp, re.MULTILINE|re.DOTALL)
	returns 		= re.findall(r'@mixin.*?return:(.*?)\*n', inp, re.MULTILINE|re.DOTALL)
	return [name,caption,arguments,returns]

# plugins parsing
def get_module_plugins(inp):
	name 		= re.findall(r'@plugin.*?name:(.*?)\*n', inp, re.MULTILINE|re.DOTALL)
	caption = re.findall(r'@plugin.*?caption:(.*?)\*n', inp, re.MULTILINE|re.DOTALL)
	return [name,caption]

# main function
def parse_keys(_file, _output, _status, _quiet, _file_name, _path):

	_input_file = open(_file)
	input_file = _input_file.read()

	match = re.search('@module', input_file)

	if match:

		global total_modules
		total_modules += 1
		print("> "+color.HEADER+_file+color.ENDC+" ("+str(len(input_file))+")")
		time.sleep(0.3)

		# start
		_output.write("\n\r\t{\n\r")
		_output.write("\n\r\t\t\"filename\": \""+str(_file_name)+"\",\n\r")
		_output.write("\t\t\"path\": \""+str(_path)+"\",\n\r")
		_output.write("\t\t\"file\": \""+str(_file)+"\",\n\r")
		_output.write("\t\t\"size\": \""+str(os.path.getsize(_file))+"\",\n\r")
		_output.write("\t\t\"length\": \""+str(len(input_file))+"\",\n\r")

		global args
		if args.cut_symbols != False:
			regexp = "|"
			for c in args.cut_symbols:
				regexp += c+"|"
			input_ = re.sub("^\s+"+regexp+"\s+$", '', str(input_file))
		else:
			input_ = str(input_file)

		module 						= get_module(input_)
		module_properties = get_module_properties(input_)
		module_methods 		= get_module_methods(input_)
		module_mixins 		= get_module_mixins(input_)
		module_plugins 		= get_module_plugins(input_)

		# module
		module_names = ['title','caption','type']
		i = 0
		for g in module:
			_output.write("\t\t\""+module_names[i]+"\": \""+g[0]+"\",\n\r")
			i += 1

		# properties
		if len(module_properties[0]) > 0:
			_output.write("\n\r\t\t\"properties\": [\n\r")
			i = 0
			while (i < len(module_properties[0])):
				if (i+1) < len(module_properties[0]):
					_output.write("\t\t\t{\"name\": \""+module_properties[0][i]+"\", \"caption\": \""+module_properties[1][i]+"\"},\n\r")
				else:
					_output.write("\t\t\t{\"name\": \""+module_properties[0][i]+"\", \"caption\": \""+module_properties[1][i]+"\"}\n\r")
				i += 1
			if len(module_methods[0]) > 0 or len(module_plugins[0]) > 0 or len(module_mixins[0]) > 0:
				_output.write("\t\t],\n\r")
			else:
				_output.write("\t\t]\n\r")

		# methods
		if len(module_methods[0]) > 0:
			_output.write("\n\r\t\t\"methods\": [\n\r")
			i = 0
			while (i < len(module_methods[0])):
				if (i+1) < len(module_methods[0]):
					_output.write("\t\t\t{\n\r\t\t\t\t\"name\":      \""+module_methods[0][i]+"\",\n\r\t\t\t\t\"caption\":   \""+module_methods[1][i]+"\",\n\r\t\t\t\t\"arguments\": \""+module_methods[2][i]+"\",\n\r\t\t\t\t\"returns\":   \""+module_methods[3][i]+"\"\n\r\t\t\t},\n\r")
				else:
					_output.write("\t\t\t{\n\r\t\t\t\t\"name\":      \""+module_methods[0][i]+"\",\n\r\t\t\t\t\"caption\":   \""+module_methods[1][i]+"\",\n\r\t\t\t\t\"arguments\": \""+module_methods[2][i]+"\",\n\r\t\t\t\t\"returns\":   \""+module_methods[3][i]+"\"\n\r\t\t\t}\n\r")
				i += 1
			if len(module_mixins[0]) > 0 or len(module_plugins[0]) > 0:
				_output.write("\t\t],\n\r")
			else:
				_output.write("\t\t]\n\r")

		# mixins
		if len(module_mixins[0]) > 0:
			_output.write("\n\r\t\t\"mixins\": [\n\r")
			i = 0
			while (i < len(module_mixins[0])):
				if (i+1) < len(module_mixins[0]):
					_output.write("\t\t\t{\n\r\t\t\t\t\"name\":      \""+module_mixins[0][i]+"\",\n\r\t\t\t\t\"caption\":   \""+module_mixins[1][i]+"\",\n\r\t\t\t\t\"arguments\": \""+module_mixins[2][i]+"\",\n\r\t\t\t\t\"returns\":   \""+module_mixins[3][i]+"\"\n\r\t\t\t},\n\r")
				else:
					_output.write("\t\t\t{\n\r\t\t\t\t\"name\":      \""+module_mixins[0][i]+"\",\n\r\t\t\t\t\"caption\":   \""+module_mixins[1][i]+"\",\n\r\t\t\t\t\"arguments\": \""+module_mixins[2][i]+"\",\n\r\t\t\t\t\"returns\":   \""+module_mixins[3][i]+"\"\n\r\t\t\t}\n\r")
				i += 1
			_output.write("\t\t]\n\r")

		# plugins
		if len(module_plugins[0]) > 0:
			_output.write("\n\r\t\t\"plugins\": [\n\r")
			i = 0
			while (i < len(module_plugins[0])):
				if (i+1) < len(module_plugins[0]):
					_output.write("\t\t\t{\""+module_plugins[0][i]+"\": \""+module_plugins[1][i]+"\"},\n\r")
				else:
					_output.write("\t\t\t{\""+module_plugins[0][i]+"\": \""+module_plugins[1][i]+"\"}\n\r")
				i += 1
			_output.write("\t\t]\n\r")

		# end
		if _status == False:
			_output.write("\t},")
		else:
			_output.write("\t}")

	else:
		# global args
		if args.quiet_mode == False:
			print("  "+_file)
			time.sleep(0.07)


# function
def create_output( inp, outp, quiet):

	filesCount = 0
	dirsCount = 0
	removedFilesCount = 0
	removedDirsCount = 0

	output = open(outp, 'w')
	output.write("[")

	for dirname, dirnames, filenames in os.walk(inp):
		for subdirname in dirnames:
			dirsCount += 1
		for filename in filenames:
			filesCount += 1
			if filesCount < len(filenames):
				parse_keys(os.path.join(dirname, filename), output, False, quiet, filename, dirname)
			else:
				parse_keys(os.path.join(dirname, filename), output, True, quiet, filename, dirname)
		if args.exeptions:
			for exep in args.exeptions:
				if exep in dirnames:
					removedDirsCount += 1
					dirnames.remove(exep)
				if exep in filenames:
					removedFilesCount += 1
					filenames.remove(exep)

	output.write("\n\r]")

	if total_modules > 0:
		print("\n\rModules created: "+str(total_modules))
	else:
		print("\n\rIt's no gived modules.")
	print(
		"File(s): "+str(filesCount)+"   Dir(s): "+str(dirsCount)+"   "+
		"Exeptions: "+str(removedFilesCount)+"file(s), "+
		str(removedDirsCount)+"dir(s)\n\r")

	return inp+outp

# 
if args.input_folder:
	print("\n\r input: <-- "+color.HEADER+args.input_folder+color.ENDC+"")
	if args.output_file:
		print("output: --> "+color.OKGREEN+args.output_file+color.ENDC+"\n\r")
		create_output(args.input_folder, args.output_file, args.quiet_mode)
	else:
		print("\n\r"+color.WARNING+"I need output file!"+color.ENDC+"\n\r")

else:
	print("\n\r"+color.WARNING+"I need input folder and output file!"+color.ENDC+"\n\r")