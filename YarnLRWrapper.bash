########################################################################## 
##YarnLRWrapper.bash 
## Report Long running jobs from Yarn 
########################################################################## 


# Variables 


hours=3 
email="dl.cto.global.gpa.big.data.support@imcnam.ssmb.com,dl.gfts.global.bigdata.coe@imcnam.ssmb.com" 
cluster_name_email="CHINA DEV" 
html_file=/home/gpabdadmin/bin/YarnLongRunningJobs/OutputYarnLR.html 
ca_cert=/home/gpabdadmin/bin/YarnLongRunningJobs/ca-cert.pem 


# Logic 


> $html_file 
/opt/cloudera/parcels/CDH/lib/hue/build/env/bin/python /home/gpabdadmin/bin/YarnLongRunningJobs/YarnLR.py $hours $html_file $ca_cert 
retval=$? 


# Email if there are Jobs 


if [ $retval -eq 0 ]; then 
  cat $html_file | grep MAPREDUCE &> /dev/null 
# cat $html_file | grep SPARK &> /dev/null 
  retval=$? 
  if [ $retval -eq 0 ]; then 
    ( 
    echo "To: $email" 
    echo "Subject: Yarn Long Running Jobs - $cluster_name_email" 
    echo "Content-Type: text/html" 
    echo "From: noreply" 
    echo 
    fmt -w 70 $html_file 
    echo 
    ) | /usr/sbin/sendmail -t   
  fi 
fi 
