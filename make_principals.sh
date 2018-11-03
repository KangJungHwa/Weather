bash-4.1$ vi gen_prin.sh 
#! /bin/sh
PROG=`basename $0`
if [ -z "$2" ]
then
 echo $PROG "{filename containing the nodes} {env: DEV or PROD}"
 exit 1
fi
FILE=$1
if [ ! -f "$FILE" ]
then
 echo "{file containing the nodes not found}"
 exit 1
fi
ENV=$2
if [ "$ENV" = "DEV" -o "$ENV" = "PROD" ]
then
 if [ "$ENV" = "DEV" ]
 then
 DOMAIN=KRUXDEV.DYN.NSROOT.NET
 else
 DOMAIN=CTIP.NAM.NSROOT.NET
 fi
else
 echo $PROG "{filename containing the nodes} {env: DEV or PROD}"
 exit 1
fi
# for j in dio gpainstall bigdata datameer cloudera-scm HTTP mapred hdfs zookeeper hbase hive oozie hue flume sqoop httpfs yarn
# when impala is added then include it in this list
#for j in rawwebbehavior namcards namcts keytrends tresatapoc namisg sendmaillog citiclientfirst patternbreaking newsilkroads
#
for j in datameer cloudera-scm HTTP mapred hdfs zookeeper hbase hive oozie hue flume sqoop httpfs yarn
do
 # for i in `cat 50node.txt`
 # for i in `cat VM_lab.txt`
 for i in `cat $FILE`
 do
# echo $j/$i.nam.nsroot.net@CTIP.NAM.NSROOT.NET
 echo $j/$i.apac.nsroot.net@$DOMAIN
 done
done

