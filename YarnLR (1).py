############################################################################ 
#YarnLR.py 
# Yarn Application Runtime via REST API 
# -*- coding: iso-8859-15 -*- 
# Important : Code is TimeZone relevant 
####################################################################### 
# 14-Jan-2016, Subramaniam S, Initial Draft in Bash 
# 01-Aug-2016, Subramaniam S, Coverted to Python Implementation 
# 13-Oct-2016, Subramaniam S, Added Active RM detection, Modularized  
# 29-Nov-2016, Subramaniam S, Added http/https options, SSL connect 
####################################################################### 


# Imports 


import requests 
import json 
import datetime 
import time 
import sys 
import re 


# Inputs from Wrapper 


hours=int(sys.argv[1]) 
html_file=sys.argv[2] 
 ca_cert=sys.argv[3] 
 

 # Get Active RM URL 
 

 

 def get_active_rm(): 
 

     global rm_url 
     rm_url = "" 
 

     conf = open("/etc/hadoop/conf/yarn-site.xml", "r") 
 

     flag = detect = False 
     rm = [] 
     for line in conf: 
         if flag and "8088" in line: 
             rm.append("http://" + line[line.find(">") + 1:line.find("</value>")]) 
             flag = False 
         if flag and "8090" in line: 
             rm.append("https://" + line[line.find(">") + 1:line.find("</value>")]) 
             flag = False 
         if re.search("yarn.resourcemanager.webapp.https.address|yarn.resourcemanager.webapp.address", line): 
             flag = True 
 

     for c in rm: 
         try: 
             r = requests.get(c, data={'key': 'value'}, verify=ca_cert) 
             detect = True 
         except requests.exceptions.RequestException: 
             detect = False 
         if detect: 
             message = "This is standby RM. Redirecting to the current active RM" 
             if message not in str(r.content): 
                 rm_url = str(c) 
 

 

 # Connect to Cluster and retrieve Apps 
 

 

 def get_job_data(): 
 

     try: 
         r = requests.get(rm_url + '/ws/v1/cluster/apps', data={'key': 'value'}, verify=ca_cert) 
         # r.json 
     except requests.exceptions.RequestException as e: 
         print "Caught in Requests : " + str(e) 
         sys.exit(404) 
     except: 
         print "Caught in Connect : ", sys.exc_info()[0] 
         sys.exit(4) 
 

     # Print whatever fits 
 

     try: 
 

         # Prep HTML File (Optional) 
 

         target = open(html_file, 'w') 
         html = """ 
             <html> 
             <head> 
             <script type="text/javascript"></script> 
             <style> 
             /* Sortable tables */ 
             table.sortable thead { 
             background-color:#5fef0b; 
             color:#000000; 
             font-weight: italic; 
             cursor: default; 
             } 
             </style> 
             <title> Yarn Long Running Apps </title> 
             </head> 
             <body bgcolor=#ffffff> 
             <table style="width:100%" class="sortable" border=1> 
             <thead> 
             <tr> 
             <th>Application ID </th> 
             <th>Application Name </th> 
             <th>User</th> 
             <th>State</th> 
             <th>Type</th> 
             <th>Start Time</th> 
             <th>Run Time (Days:HH:MM:SS) </th> 
             </tr> 
             </thead> 
             <tbody> 
         """ 
         target.write(html) 
 

         # Check if there are apps being listed 
 

         if r.content == "{\"apps\":null}": 
             print "No jobs found on the Cluster, was Yarn restarted recently" 
             target.write("</tbody></table><h3>No Jobs on the Cluster....</h3></body></html>") 
             target.close() 
             sys.exit(2) 
 

         sub1 = "" 
         sub2 = "" 
         ejson = json.loads(r.content) 
         for key in ejson.keys(): 
             sub1 = ejson[key] 
             sub2 = sub1["app"] 
 

         # print "Full App List " + str(sub2) 
         # print "\n" 
 

         for lists in sub2: 
 

             app = lists 
 

             if str(app["state"]) == "RUNNING" and str(app["applicationType"]) == "MAPREDUCE": 
           # if str(app["state"]) == "RUNNING" and str(app["applicationType"]) == "SPARK": 
                 appID = str(app["id"]) 
                 user = str(app["user"]) 
                 state = str(app["state"]) 
                 aType = str(app["applicationType"]) 
                 aName = str(app["name"]) 
                 start = str( 
                     datetime.datetime.fromtimestamp(float(app["startedTime"]) / 1000.).strftime('%Y-%m-%d %H:%M:%S')) 
                 finish = str( 
                     datetime.datetime.fromtimestamp(float(app["finishedTime"]) / 1000.).strftime('%Y-%m-%d %H:%M:%S')) 
                 timer = start + ", " + finish 
 

                 st_epoch = int((app["startedTime"]) / 1000.) 
                 en_epoch = int((app["finishedTime"]) / 1000.) 
                 current = int(time.time()) 
 

                 # alltime = str(st_epoch) + "," + str(en_epoch) + "," + str(current) 
                 subtime = current - st_epoch 
                 m, s = divmod(subtime, 60) 
                 h, m = divmod(m, 60) 
                 d, h = divmod(h, 24) 
 

                 if h >= int(hours): 
                         print appID + ", " + aName + ", " + user + ", " + state + ", " + aType + ", " + start + ", " + "%d:%d:%02d:%02d" % (d, h, m, s) 
                         trtd = "</td><td>" 
                         html2 = "<tr><td>" + appID + trtd + aName + trtd + user + trtd + state + trtd + aType + trtd + start + trtd + \ 
                                                         "%d:%d:%02d:%02d" % (d, h, m, s) + "</td></tr>" 
                         target.write(html2) 
 

         target.write("</tbody></table></body></html>") 
         target.close() 
 

     except Exception as e: 
         print "Caught Exception in Parse Block ", e 
 

 

 ## Method Calls 
 

 get_active_rm() 
 

 get_job_data() 
