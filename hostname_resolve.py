import socket
import sys
hostname=sys.argv[1]
print hostname
def hostname_resolves(hostname):
    """
    Check if hostname resolves
    :param hostname:
    :return:
    """
    try:
        if socket.gethostbyname(hostname) == '0.0.0.0':
            print "Error [{'host': '%s', 'fqdn': '%s'}]" % \
                  (socket.gethostbyname(hostname), socket.getfqdn(hostname))
            return False
        else:
            print "Success [{'host': '%s', 'fqdn': '%s'}]" % \
                  (socket.gethostbyname(hostname), socket.getfqdn(hostname))
            return True
    except socket.error:
        print "Error 'host': '%s'" % hostname
        return False
hostname_resolves('bdicr101x03h2')
