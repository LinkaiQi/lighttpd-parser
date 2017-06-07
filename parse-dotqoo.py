#!/usr/bin/python

import re, argparse, os

DEFAULT_PATH = "/var/log/lighttpd/access.log"

# command line input arguments
options = {}

# RegexObject dictionary
OS = {}
browser = {}
brand = {}

# referers = {}
# days = {}
hosts = {}
# files = {}
# urls = {}
extensions = {}
stat_OS = {}
stat_browser = {}
stat_brand = {}

total_digits = 10
current_lines = 0

# stat table
table = {}



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


# show top 100 host name
def show_sorted_host(dictionary):
	counter = 0
	for entry in sorted(dictionary, key=dictionary.get, reverse=True):
		if counter == 100:
			break
		print str(dictionary[entry]).rjust(total_digits),
		print entry.ljust(35)
		counter += 1


def parse():
	global table, OS, browser, brand, DEFAULT_PATH
	current_lines = 0

	if options['auto']:
		paths = [DEFAULT_PATH]
	else:
		paths = options['logfiles']

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


				if ip not in table:
					# table column OS, browser, brand
					table[ip] = [None, None, None]

				# OS
				for regex, name in OS.iteritems():
					result = regex.search(device)
					if result:
						table[ip][0] = name + " " + result.group(2).replace('_', '.')

				# browser
				for regex, name in browser.iteritems():
					result = regex.search(device)
					if result:
						table[ip][1] = name

				# brand
				for regex, name in brand.iteritems():
					result = regex.search(device)
					if result:
						table[ip][2] = name


			except ValueError:
				print "Corrupt log line at line %d, contents: %s" % (current_lines + 1, line[:-1])

			# line counter
			current_lines += 1
			if current_lines % 10000 == 0:
				print " >>> Processed %d lines." % current_lines


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
	global OS, browser, brand

	# OS
	android = re.compile(r"(Android) ?(\d+\.\d+(\.\d+)?)")
	OS[android] = "Android"
	# re.search(r"(Android) ?(\d+\.\d+(\.\d+)?)", "dsfsdfsdk Android 4.3").group(2)
	# Android 4.3 /  Android 6.0.1
	ios_1 = re.compile(r"(iOS)[ |;](\d+\.\d+(\.\d+)?)")
	OS[ios_1] = "iOS"
	# re.search(r"(iOS)[ |;](\d+\.\d+(\.\d+)?)", "dsfsdfsdk iOS;10.3.3").group(2)
	# iOS;10.2.1 / iOS 10.2.1 / iOS/8.1
	ios_2 = re.compile(r"(iPhone\d+\,\d+)/(\d+\.\d+(\.\d+)?)")
	OS[ios_2] = "iOS"
	# re.search(r"(iPhone\d+\,\d+)/(\d+\.\d+(\.\d+)?)", "iPhone7,1/10.2.1 (14D27)").group(2)
	# iPhone7,1/10.2.1 (14D27)
	ios_3 = re.compile(r"(iPhone OS) (\d+_\d+(_\d+)?)")
	OS[ios_3] = "iOS"
	# TODO the return value of group(2) is "_", not dot
	# re.search(r"(iPhone OS) (\d+_\d+(_\d+)?)", "(CPU iPhone OS 10_2_1)").group(2)
	# iPhone OS 10_2_1

	# BROWSER
	mozilla = re.compile(r"mozilla", re.IGNORECASE)
	browser[mozilla] = "mozilla"
	# TODO all convert to lower case letter
	# re.search(r"mozilla", "MoZiLLa", re.IGNORECASE).group()
	# Mozilla/5.0 (Linux...)
	dalvik = re.compile(r"dalvik", re.IGNORECASE)
	browser[dalvik] = "dalvik"
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
	global stat_OS, stat_browser, stat_brand

	for ip, info in table.iteritems():
		if info[0] not in stat_OS:
			stat_OS[info[0]] = 0
		if info[1] not in stat_browser:
			stat_browser[info[1]] = 0
		if info[2] not in stat_brand:
			stat_brand[info[2]] = 0

		stat_OS[info[0]] += 1
		stat_browser[info[1]] += 1
		stat_brand[info[2]] += 1


def print_result():
	global stat_OS, stat_browser, stat_brand, extensions

	print "\nTop OS:"
	show_sorted(stat_OS)

	print "Top browser:"
	show_sorted(stat_browser)

	print "Top manufacturer:"
	show_sorted(stat_brand)

	# print "Top extension"
	# show_sorted(extensions)

	print "Top 100 host:"
	show_sorted_host(hosts)

	print ''



def main():
	read_arg()
	compile_regex()
	parse()
	get_stats()

	print_result()

	# for key, value in table.iteritems():
	# 	print key, value













if __name__ == '__main__':
	main()
