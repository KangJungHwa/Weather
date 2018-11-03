bash-4.1$ vi urlCheck.py 
import sys
import getopt
import smtplib
import urllib2
import socket
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
fromAddress='noreply@'+socket.getfqdn()
toaddress='dl.cto.kr.big.data.monitoring@imcap.ap.ssmb.com';
array_server=['https://bigdataplatform-ukr.apac.nsroot.net:7183/cmf/localLogin',
              'https://tiawccap012sgp.apac.nsroot.net:8443/wcc/ui/Login.html',
              'https://secureaccess.uat.nam.citigroup.net/idp/startSSO.ping?PartnerSpId=dkorhu-165345-SPID',
              'https://bdicr101x13h2.apac.nsroot.net:7187/login.html',
              'http://kriclu0125.apac.nsroot.net:7980/SASLogon/login?service=http%3a%2f%2Fkriclu0125.apac.nsroot.net%3A7980%2FSASStudio%2Fj_spring_cas_security_check'];

def sendMail(title,msg):
        msg = MIMEText(msg)
        msg['Subject'] = title
        msg['From']=fromAddress
        msg['To'] = toaddress
        s = smtplib.SMTP('localhost')
        s.sendmail(fromAddress,toaddress, msg.as_string())
        s.quit()

def getURL(url):

        result=urllib2.urlopen(url).getcode();
        print "~~11~~:", result;
        return result;

def check_server(server_ip, server_kind):
    try:
        result=getURL(server_ip);
    except:
          result=999

    if(result != 200):
        title='[URL STATUS ERROR] : ' +server_kind;
        msg='System error. Url could not Connect! contact your server manager';
        msg+='\n\n';
        msg+=server_ip;
        msg+='\n\n';
        msg+=str(result);
        print 'SYSTEM ERROR. :'+ server_ip;
        sendMail(title,msg);
    else:
        title='[URL STATUS OK] : '+ server_kind;
        msg='url request not authorized but server is alive';
        msg+='\n\n';
        msg+=server_ip;
        msg+='\n\n';
        msg+=str(result);
        print 'SYSTEM OK';
        sendMail(title,msg);

def main():
    URL_list = ['Cloudera Manager','AUTOSYS', 'HUE','Cloudera Navigator', 'SAS Web Console']
    seq=-1;
    for server_ip in array_server:
        seq=seq+1;

        check_server(server_ip,URL_list[seq]);
if __name__ == "__main__":
    main();
