# lighttpd-parser

Parse a lighttpd access log.

### usage:
    parse-dotqoo.py [-h] [-a] [-m MINIMUM] logfile [logfile ...]

### positional arguments:
    logfile     path(s) of the logfile(s)

### optional arguments:
    -h, --help  show this help message and exit
    -a, --auto  get the access.log file from default directory
              /var/log/lighttpd/access.log
    -m MINIMUM  the counting threshold that has to be exceeded to display the
              entry
