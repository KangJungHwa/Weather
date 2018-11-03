import socket, sys, time, ConfigParser, csv, pprint, urllib2
from optparse import OptionParser
# 호출할때 -p 옵션을 주고 config 파일을  세팅해야한다.
yes = set(['yes','y', 'ye', ''])
no = set(['no','n'])
host = socket.getfqdn()
swd=sys.path[0]
parser = OptionParser()
parser.add_option('-p', '--parameterfile', dest='PARAMETER_FILE', default='', help='A parameter file for default and custom values by default config.ini' )
parser.add_option('-l', '--logfile', dest='LOG_FILE', default='', help='A log file' )
parser.add_option('-r', '--remove', action='store_true', dest='REMOVE', help='Remove Cloudera Software' )

(options, args) = parser.parse_args()

if not options.PARAMETER_FILE:
    print 'No option passed in. Default parameter file (config.ini) assumed must be readible'
    PARAMETER_FILE='config.ini'
else:
    PARAMETER_FILE=options.PARAMETER_FILE
    print PARAMETER_FILE
if not options.LOG_FILE:
    now=time.strftime("%F-%T")
    LOG_DIR='/var/log/CATE'
    LOG_FILE=LOG_DIR+'/'+'install-cloudera-'+now+'.log'
else:
    LOG_FILE=options.LOG_FILE

CONFIG = ConfigParser.ConfigParser()
CONFIG.read(PARAMETER_FILE)
MYSQL_HOSTS = CONFIG.get("MYSQL", "mysql.hosts").split(',')
print MYSQL_HOSTS
if not MYSQL_HOSTS[0]:
    print 'Must enter a MySQL server host in the ' + PARAMETER_FILE + ' file'
    sys.exit(1)
