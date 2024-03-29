#!/usr/bin/python

import re, argparse, os
from datetime import datetime

DEFAULT_PATH = "/var/log/lighttpd/access.log"

# command line input arguments
options = {}

# RegexObject dictionary
OS = {}
base = {}
brand = {}

# referers = {}
# days = {}
hosts = {}
# files = {}
# urls = {}
extensions = {}
stat_OS = {}
stat_base = {}
stat_brand = {}

total_digits = 10
current_lines = 0

# stat table
table = {}

record = {}
# ip: {[init-time, last-update, duration], [_,_,_], ....}



def show_sorted(dictionary):
	global table

	for entry in sorted(dictionary, key=dictionary.get, reverse=True):
		if options['minimum'] == None or dictionary[entry] > int(options['minimum']):
			print str(dictionary[entry]).rjust(total_digits),
			if not entry:
				print "UNIDENTIFIED".ljust(15),
			else:
				print entry.ljust(15),
			# show Percentage
			print format(dictionary[entry] / float(len(table)) * 100, '.2f') , "%"
	print ""


# show top 20 host name
def show_sorted_host(dictionary):
	counter = 0
	for entry in sorted(dictionary, key=dictionary.get, reverse=True):
		# only print top 20 host name
		# put the rest in local txt file
		if counter == 20:
			break
		print str(dictionary[entry]).rjust(total_digits),
		print entry.ljust(35)
		counter += 1
	print ""


# use dalvik and mozilla format quick parse device info
def quick_parse(ip, device):
	global base, table

	# base
	for regex, name in base.iteritems():
		if regex.match(device):

			# initalize values
			os = base_version = brand = model = build = None

			if name == "Dalvik":
				system, extra = device.split(')')
				base_version, sys_info = system.split('(')
				base_version = base_version.rstrip()
				# Compatible mode
				if len(base_version.split()) > 1:
					base_version, mode = base_version.split()
					if mode != "Compatible":
						# raise ValueError('unsupported form')
						return False
					# TODO ..........
					# raise ValueError('unsupported form')
					return False
				# normal form
				else:
					sys_info = sys_info.split(';')
					os = sys_info[2][1:]
					temp = sys_info[3].split()
					brand = temp[0]
					model = temp[1:-1]
					if model == []:
						model = None
					build = temp[-1]
					# value assignment
					# OS, base, brand, model, build
					# table[ip] = [os, base_version, brand, model, build]
					# return True

			elif name == "Mozilla":
				system, extra = device.split(')', 1)
				base_version, sys_info = system.split('(')
				base_version = base_version.rstrip()
				sys_info = sys_info.split(';')

				# cannot get 'model', 'build' from Windows OS
				if sys_info[0] == "iPhone":
					result = regex_iOS.search(system)
					if result:
						os = "iOS " + result.group(2).replace('_', '.')
						brand = "Apple"
					else:
						return False
						# raise ValueError('unsupported form')

				# cannot get 'brand', 'model', 'build' from Windows OS
				elif sys_info[0] == "Windows":
					# os = sys_info[2].strip()
					pass

				# handle by	dalvik base
				elif sys_info[0] == "Linux":
					pass

				elif sys_info[0] == "compatible":
					# build = sys_info[1].strip()
					# os = sys_info[2].strip().strip(')')
					return False

				# unsupported form
				else:
					return False
					# raise ValueError('unsupported form')

			# value assignment
			# OS, base, brand, model, build
			values = [os, base_version, brand, model, build]
			for i in range(len(values)):
				if values[i] != None:
					table[ip][i] = values[i]
	return True

	# if find dalvik and mozilla expression, return match = True


def parse():
	global table, regex_iOS, OS, base, brand, DEFAULT_PATH
	current_lines = 0

	# write unparseable log to file
	fp = open("unparseable_log.txt", 'w')

	# if auto flag is provided, add DEFAULT_PATH to 'paths'
	paths = options['logfiles']
	if options['auto']:
		paths.append(DEFAULT_PATH)

	for logpath in paths:
		try:
			log = open(logpath, 'r')
		except IOError:
			print "Could not find file %s, ignored entry." % logpath
			# read next log file
			continue

		for line in log:
			try:
				ipTime, request, stat, referer, space, device = line.split('"', 5)

				# try:
				#	uri = request.split()[1]
				#	extension = os.path.splitext(uri)[1][1:]
				# except:
				#	extension = ''
				ip, hostname, time = ipTime.split(None, 2)
				time = time[3:-8]
				time_obj = datetime.strptime(time, '%d/%b/%Y:%H:%M:%S')

				# extension (HTML, png ..)
				# if len(extension) <= 5:
				#	if extension not in extensions:
				#		extensions[extension] = 1
				#	else:
				#		extensions[extension] += 1

				# hostname (eg. short.weixin.qq.com)
				if hostname not in hosts:
					hosts[hostname] = 1
				else:
					hosts[hostname] += 1;

				# if not in record, create an entry
				if ip not in table:
					# table column: OS, base, brand, model, build
					table[ip] = [None, None, None, None, None]
					record[ip] = [[time_obj, time_obj, time_obj-time_obj]]

				# update connection duration
				# ip: {[init-time, last-update, duration], [_,_,_], ....}
				latest_record = record[ip][-1]
				if (time_obj - latest_record[1]).total_seconds() < 300:
					latest_record[1] = time_obj
					latest_record[2] = time_obj - latest_record[0]
				else:
					record[ip].append([time_obj, time_obj, time_obj-time_obj])

				# update duration
				# table[ip][4] = str(time_obj - table[ip][3])

				# dalvik and mozilla format quick parse device info
				success = quick_parse(ip, device)
				# IF dalvik and mozilla format parser does not work
				# AND haven't get device info yet
				# -> THEN try regular regex parse insterad
				if table[ip][4] == None:

					# OS
					for regex, name in OS.iteritems():
						result = regex.search(device)
						if result and table[ip][0] == None:
							# table column: OS, base, brand, model, build
							table[ip][0] = name + " " + result.group(2).replace('_', '.')

					# base
					for regex, name in base.iteritems():
						result = regex.search(device)
						if result and table[ip][1] == None:
							table[ip][1] = result.group()

					# brand
					for regex, name in brand.iteritems():
						result = regex.search(device)
						if result and table[ip][2] == None:
							table[ip][2] = name

				if not success:
					raise ValueError('unsupported quick_parse form')




			except ValueError:
				fp.write("Corrupt log line at line " + str(current_lines+1) + "  " + device)
				#print "Corrupt log line at line %d, contents: %s" % (current_lines + 1, line[:-1])

			# line counter
			current_lines += 1
			if current_lines % 10000 == 0:
				print " >>> Processed %d lines." % current_lines

	# close 'unparseable_log.txt'
	fp.close()


def read_arg():
	global options, DEFAULT_PATH

	parser = argparse.ArgumentParser(description='Parse a lighttpd access log.')

	parser.add_argument('logfiles', metavar='logfile', type=str, nargs='+',
	                   help='path(s) of the logfile(s)')

	parser.add_argument('-a', '--auto', action="store_true", default=False,
						help ='get the access.log file from default directory ' + DEFAULT_PATH)

	# parser.add_argument('-e', '--extensions', dest='extensions', action='store',
	#                   help='specify a comma-separated list of extensions to ignore during parsing')

	parser.add_argument('-m', dest='minimum', action='store',
	                   help ='the counting threshold that has to be exceeded to display the entry')

	args = parser.parse_args()
	options = vars(args)


def compile_regex():
	global regex_iOS, OS, base, brand

	regex_iOS = re.compile(r"(iPhone OS) (\d+_\d+(_\d+)?)")
	# re.search(r"(iPhone OS) (\d+_\d+(_\d+)?)", "(CPU iPhone OS 10_2_1)").group(2)
	# iPhone OS 10_2_1

	# OS
	android = re.compile(r"(Android) ?(\d+\.\d+(\.\d+)?)")
	OS[android] = "Android"
	# re.search(r"(Android) ?(\d+\.\d+(\.\d+)?)", "dsfsdfsdk Android 4.3").group(2)
	# Android 4.3 /  Android 6.0.1
	ios_1 = re.compile(r"(iOS)[^01-9]?(\d+\.\d+(\.\d+)?)")
	OS[ios_1] = "iOS"
	# re.search(r"(iOS)[^01-9]?(\d+\.\d+(\.\d+)?)", "dsfsdfsdk iOS;10.3.3").group(2)
	# iOS;10.2.1 / iOS 10.2.1 / iOS/8.1
	ios_2 = re.compile(r"(iPhone\d+\,\d+)/(\d+\.\d+(\.\d+)?)")
	OS[ios_2] = "iOS"
	# re.search(r"(iPhone\d+\,\d+)/(\d+\.\d+(\.\d+)?)", "iPhone7,1/10.2.1 (14D27)").group(2)
	# iPhone7,1/10.2.1 (14D27)
	ios_3 = re.compile(r"(iPhone OS) (\d+_\d+(_\d+)?)")
	OS[ios_3] = "iOS"
	# re.search(r"(iPhone OS) (\d+_\d+(_\d+)?)", "(CPU iPhone OS 10_2_1)").group(2)
	# iPhone OS 10_2_1


	# Base
	mozilla = re.compile(r"Mozilla/")
	base[mozilla] = "Mozilla"
	# TODO all convert to lower case letter
	# re.search(r"mozilla", "MoZiLLa", re.IGNORECASE).group()
	# Mozilla/5.0 (Linux...)
	dalvik = re.compile(r"Dalvik/")
	base[dalvik] = "Dalvik"
	# TODO all convert to lower case letter
	# re.search(r"dalvik", "Dalvik", re.IGNORECASE).group()
	# Dalvik/2.1.0 (Linux...)


	# Brand
	GIONEE = re.compile(r"GIONEE", re.IGNORECASE)
	OPPO = re.compile(r"OPPO", re.IGNORECASE)
	vivo = re.compile(r"vivo", re.IGNORECASE)
	ZTE = re.compile(r"ZTE", re.IGNORECASE)
	Apple = re.compile(r"(iPhone)|(iOS)", re.IGNORECASE)
	HUAWEI = re.compile(r"HUAWEI", re.IGNORECASE)
	HONOR = re.compile(r"HONOR", re.IGNORECASE)
	Xiaomi = re.compile(r"Xiaomi", re.IGNORECASE)
	Meizu = re.compile(r"Meizu", re.IGNORECASE)
	HTC = re.compile(r"HTC", re.IGNORECASE)
	Samsung = re.compile(r"Samsung", re.IGNORECASE)
	Lenovo = re.compile(r"Lenovo", re.IGNORECASE)
	Coolpad = re.compile(r"Coolpad", re.IGNORECASE)
	Redmi = re.compile(r"Redmi", re.IGNORECASE)
	LG = re.compile(r"LG")

	# add to brand list
	brand = {GIONEE:"GIONEE", OPPO:"OPPO", vivo:"vivo", ZTE:"vivo", Apple:"Apple", HUAWEI:"HUAWEI", HONOR:"HONOR",
	         Xiaomi:"Xiaomi", Meizu:"Meizu", HTC:"HTC", Samsung:"Samsung", LG:"LG", Lenovo:"Lenovo", Coolpad:"Coolpad",
			 Redmi: "Redmi"}


def get_stats():
	global stat_OS, stat_base, stat_brand

	for ip, info in table.iteritems():
		if info[0] not in stat_OS:
			stat_OS[info[0]] = 0
		if info[1] not in stat_base:
			stat_base[info[1]] = 0
		if info[2] not in stat_brand:
			stat_brand[info[2]] = 0

		stat_OS[info[0]] += 1
		stat_base[info[1]] += 1
		stat_brand[info[2]] += 1


def print_result():
	global stat_OS, stat_base, stat_brand, extensions

	print "\nDetected total %d devices" % len(table)

	print "\nTop OS:"
	show_sorted(stat_OS)

	print "Top base:"
	show_sorted(stat_base)

	print "Top manufacturer:"
	show_sorted(stat_brand)

	# print "Top extension"
	# show_sorted(extensions)

	print "Top 20 host:"
	show_sorted_host(hosts)

	print "For more details please check 'hostname', 'info_table' and 'conn_timestamp' located in the current directory"

	print ''


def write_to_file():
	global table, hosts, record

	# write info table
	fp = open("info_table.txt", 'w')
	for ip, info in table.iteritems():
		# construct device info (eg. Redmi Note 2)
		dev = str(info[2])
		if info[3] != None:
			for value in info[3]:
				dev += ' ' + value
		fp.write(ip.rjust(20) + ' | ' + str(info[0]).ljust(15) + str(info[1]).ljust(14)
			+ dev.ljust(16) + str(info[4])+ '\n')
	fp.close()

	# write hostname
	fp = open("hostname.txt", 'w')
	for entry in sorted(hosts, key=hosts.get, reverse=True):
		fp.write(str(hosts[entry]).rjust(total_digits) + ' ' + entry.ljust(35) + '\n')
	fp.close()

	# write connection timestamp
	fp = open("conn_timestamp.txt", 'w')
	for ip, info in table.iteritems():
		fp.write(ip.rjust(18) + ' ' + str(info) + '\n')
		for conn in record[ip]:
			fp.write(("Start: " + str(conn[0])).rjust(45) + "  Duration:" + str(int(conn[2].total_seconds())) + "secs\n")
		fp.write('\n')
	fp.close()





def main():
	read_arg()
	compile_regex()
	parse()
	get_stats()

	print_result()
	write_to_file()






if __name__ == '__main__':
	main()
