from connection import *
from datetime import datetime, timedelta
import time

def check_expiry_token(expiry):
	a=time.strftime('%Y-%m-%d %H:%M:%S')
	#print a
	expiry=expiry.strftime('%Y-%m-%d %H:%M:%S')
	#print expiry
	if expiry<a :
		return True
	else:
		return False


def get_role_id(access_token,device_id):
	query="SELECT user_id,expiry FROM user_access where access_token='{0}' and device_id='{1}';".format(access_token,device_id)
	print 'here'
	conn=connect()
	cursor=conn.cursor()
	cursor.execute(query)
	row = cursor.fetchone()
	print "row in get_role_id in oath" ,row
	if row is not None:
		user_id= row[0]
		expiry=row[1]
		if check_expiry_token(expiry)==True:
			conn.close()
			return {"message":"user not authorised","reason":"token expired","success":False,'role_id':-1}
		elif check_expiry_token(expiry)==False:
			query='select role_id from user_role where user_id="{0}";'.format(user_id)
			cursor=conn.cursor()
			cursor.execute(query)
			row = cursor.fetchone()
			role_ids=dict()
			i=0
			while row is not None:
				role_ids[i]=row[0]
				i=i+1
				row=cursor.fetchone()	
			#print "role_id=", role_ids
			conn.close()
			return {"message":"user authorised","reason":"token exsists","success":True,"role_id":role_ids}
		else:
			conn.close()
			return {"message":"user not authorised","reason":"unknown","success":False,"role_id":-1}
	else:
		conn.close()
		return {"message":"user not authorised","reason":"please log in first","success":False,"role_id":-1}
	
	
def check_role_permission(role,endpoint):
	conn=connect()
	cursor=conn.cursor()
	#print role_id
	role_id=role['role_id']
	if role_id== -1:
		return {"message":"no allowed permissions","reason":"role not authorised","success":False,"role_id":-1}
	query='select role_id from role_permissions where endpoint="{0}";'.format(endpoint)
	cursor.execute(query)
 	row = cursor.fetchone()
	while row is not None:
		for key, value in role_id.iteritems():
			if(value == row[0]):
				conn.close()
				return {"message":"user authorised","reason":"token exists","success":True,"role_id":value}
		row=cursor.fetchone()
	conn.close()
 	return {"message":"user not authorised","reason":"method not allowed","success":False,'role_id':-1}
	
    
#check_role_permission(get_role_id(access_token,device_id),'post_req')       
