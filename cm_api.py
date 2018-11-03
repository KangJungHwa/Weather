################################################################################
	 2대의 클러스터의 환경설정을 비교해서 클러스터의 문제점 파악하는법
	 api_dump.py를 이용해서 클러스터의 모든 config 파일을 백업받는다.
	 api_dump.py는 cm_api를 이용하기 때문에 cm_api 패키지가 필요하다.
	 tar xvfz cm_api-15.0.0.tar.gz -C /tmp/
	 api_dump.py를 아래경로 밑에 카피해놓고 실행해야 한다.
	 /tmp/cm_api-12.0.0/src/
	 python api-dump.py -s <CM URL> -n <cluster_name> -p <패스워드> -o /tmp/dump
	 dump 받은 클러스터의 환경설정을 아래 cluster-compare.py를 이용해서 비교한다.
	 디렉토리를 지정하면 지정된 디렉토리의 모든 환경설정파일을 비교한다.
	 python cluster-compare.py /tmp/dump /tmp/api_dump
#################################################################################

#################################################################################
# api_dump.py 
python api-dump.py -s <CM URL> -n <cluster_name> -p <패스워드> -o /tmp/dump
#################################################################################

#!/usr/bin/env python
#coding:utf8
#cm_api.py 

import re, math, pprint, json, sys, argparse, os, ConfigParser, shutil,time
from cm_api.api_client import ApiResource
from subprocess import call

t = time.localtime()
timestamp = time.strftime('%b-%d-%Y_%H:%M', t)
debug = False
def buildParser(inputArgs):
    parser = argparse.ArgumentParser(
        description='Cloudera Manager Configuration APIs')

    parser.add_argument('-s', '--src', dest='cmHost', help='Source CM hostname')
    parser.add_argument('-P', '--port', dest='cmPort', default=7183, type=int, help='CM Port')
    parser.add_argument('-n', '--name', dest='clusterName',default='xxxxx', help='Source Cluster Name')
    parser.add_argument('-u', '--user', dest='user', default='admin', help='CM User')
    parser.add_argument('-p', '--pass', dest='password', help='CM Password')
    parser.add_argument('-v', dest='verbose', action='store_true', default=False,
                        help='Enable verbose logging')
    parser.add_argument('-o', '--output-directory', dest='outputDirname',
                        help='Dump the configuration to the specified local directory')
    return parser.parse_args(inputArgs)

def pickCluster(cList):
    # Print all cluster names and allow user to choose
    for i in xrange(len(cList)):
        print str(i) + " : " + cList[i].name + " / " + cList[i].fullVersion
    while True:
        try:
            cNum = int(raw_input("Pick the cluster number from above: "))
        except ValueError:
            print "Please provide a valid number from above"
            continue
        if cNum not in range(len(cList)):
            print "Please provide a valid number from above"
            continue
        else:
            if debug:
                print "Chosen cluster: " + cList[cNum].name
                print "Cluster version: " + cList[cNum].version
            return cList[cNum]

# Get all services for cluster
def getServices(cluster):
    """
    Gets an array of the configured services
    This assumes only 1 type of service per cluster.
    :param cluster
    :return: array of service datatypes
    Datastructure: service.name / .type
    If multiple services exists, add logic to copy a particular services to particular destination service
    """
    services = []
    for s in cluster.get_all_services():
        if debug:
            print s
        services.append(s)
    return services

def dumpConfig(cluster, dname):
    """
    :param cList: cluster list
    :param dname: output dirname
    This will dump the clusters configuration to a file per service.
    This is mainly used as a backup for cluster configuration.
    """
    services = getServices(cluster)
    # Iterate over services and print to file
    for s in services:
        out_conf = ConfigParser.RawConfigParser()
        out_conf.add_section(s.type)
        sConf = s.get_config(view='full')[0]
        if debug:
            print s.name
            pprint.pprint(sConf)
        for name, config in sConf.items():
            out_conf.set( s.type, config.name, config.value.encode('ascii','ignore').decode('ascii') if config.value else config.default )
        fname = "%s/%s.conf" % (dname,s.type.lower())
        with open(fname, "w") as out_file:
            out_conf.write(out_file)

        for group in s.get_all_role_config_groups():
            if debug:
                print "roleConfigGroup: " + group.name
            out_conf = ConfigParser.RawConfigParser()
            out_conf.add_section( group.roleType )
            gConf = group.get_config(view='full')
            for name, config in gConf.items():
                out_conf.set( group.roleType, config.name, config.value if config.value else config.default )
            fname = "%s/%s-%s.conf" % (dname,s.type.lower(), group.roleType.lower())
            with open(fname, "w") as out_file:
                out_conf.write(out_file)


if __name__ == "__main__":
    args = buildParser(sys.argv[1:])

    if args.verbose:
        debug = True

    if (args.cmHost is None):
        print "Must provide source hostnames for CM"
        exit(1)

    if (args.outputDirname is None):
        print "Must provide output directory"
        exit(2)

    if os.path.isdir( args.outputDirname ):
        print "Output directory already exists with configurations, will taking a backup of the directory which can be used for rolling back a config"
    else:
       os.mkdir( args.outputDirname)

    print "HELLO"
    print "host " + args.cmHost
    print "port " + str(args.cmPort)
    print "user " + args.user
    print "password " + args.password
    print "cluster " + args.clusterName

    sapi = ApiResource(args.cmHost, args.cmPort, args.user, args.password,use_tls=1)

    if (args.clusterName is None):
        # Get all cluster names
        sClusters = []
        for c in sapi.get_all_clusters():
            print c
            sClusters.append(c)

        # Choose source and destination clusters
        print "Source cluster: " + args.cmHost
        sCluster = pickCluster(sClusters)
    else:
        sCluster = sapi.get_cluster(args.clusterName)

    sName = args.outputDirname
    shutil.move(sName, sName +timestamp)
    os.mkdir(sName)
    dumpConfig(sCluster, sName)
    if os.path.exists(sName +"_edits"):
        shutil.move(sName +"_edits", sName+ "_edits" +timestamp)
        os.mkdir(sName +"_edits")
    else:
        shutil.copytree(sName, sName + "_edits")