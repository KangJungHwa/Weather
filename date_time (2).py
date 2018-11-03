import datetimeimport timeimport calendar
def get_now(*args):    
    if len(args) == 0:        
        now =str(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))    
    else:        
	    now =str(datetime.datetime.fromtimestamp(time.time()).strftime(args[0]))    
	return now
def elapsed_time(sdate,type):    
    return_val=0    
	e = datetime.datetime.now()    
	if not sdate or len(sdate) < 14: 
	    return 0,0,0,0    
		s = datetime.datetime(int(sdate[:4]), int(sdate[4:6]), int(sdate[6:8]),        
		int(sdate[8:10]), int(sdate[10:12]), int(sdate[12:14]))    
	if type=='days':        
	return_val = (e-s).days    
	elif type=='sec':        
	return_val = (e-s).seconds    
	elif type=='hour':        
	sec = (e-s).seconds        
	retrun_val = sec//3600    
	elif type=='minute':        
	sec = (e-s).seconds        
	return_val = sec//60    
	return return_val
def add_days(basedate,addday,format):    
start=datetime.datetime.strptime(basedate,format)    
add_result = start+datetime.timedelta(days=addday)    
return add_result
def get_last_day(year_month):    
syear=year_month[:4]    
smon=year_month[4:6]     
return calendar.monthrange(syear,smon)[1] 
def month_first_weekday(year_month):    
syear=year_month[:4]    
smon=year_month[4:6]     
return calendar.monthrange(syear,smon)[0] 
def date_time_diff(sdate,edate,type):    
return_val=0    
if (not sdate or len(sdate) < 14) or (not edate or len(edate) < 14):         
return 0    e = datetime.datetime(int(edate[:4]), int(edate[4:6]), int(edate[6:8]),        
int(edate[8:10]), int(edate[10:12]), int(edate[12:14]))       
s = datetime.datetime(int(sdate[:4]), int(sdate[4:6]), int(sdate[6:8]),        
int(sdate[8:10]), int(sdate[10:12]), int(sdate[12:14]))    
if type=='days':        
return_val = (e-s).days    
elif type=='sec':        
return_val = (e-s).seconds    
elif type=='hour':        
sec = (e-s).seconds        
retrun_val = sec//3600    
elif type=='minute':        
sec = (e-s).seconds        
return_val = sec//60    
return return_val 
print get_last_day('201702') 
#print add_days('20170610',-31,'%Y%m%d')
#print elapsed_time('20170710162510','sec')
#print get_now()#print get_now('%Y%m%d %H:%M:%S')
