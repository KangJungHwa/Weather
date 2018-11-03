import filecmp
import os
import os.path
import sys
import difflib
import subprocess
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def listfile(path1):
    common_paths = []

    for path, dirs, files in os.walk(path1):
        for name in files:
            print path+'/'+name
       # abs1 = os.path.join(path1, path)
       # print abs1
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print len(sys.argv)
        print "Usage: listfile.py {path1} "
        sys.exit()

    paths = sys.argv[1]
    if not os.path.exists(paths):
        print "%s does not exist!" % path
        sys.exit()
    basepath = os.path.commonprefix(paths).rstrip('/')
    listfile(paths)
