#@author: supermacy
#parsing http requests

import json

def parse(req_data,req_type=""):
	try:
		if req_data!="":
			if req_type=='json':
				try:
					json_data=json.loads( req_data)
					return json_data
				except:
					ret=dict()
					ret['message']='THe data is not in correct format';
					ret['success']=False
					return ret
					pass

			elif req_type =='form':
				return req_data
			else:
			 	return req_data
		else:
			return "";
	except Exception, e:
		raise
	


def parse_main(reqt):		
		data =""
		req_type=reqt.headers.get('Content-Type')
		print (req_type)
		if req_type != "":
			if req_type=='application/x-www-form-urlencoded':
				req_type='form'
				data=parse(reqt.form,req_type)
			elif req_type.split(';')[0]=='application/json':
				req_type='json'
				data=parse(reqt.get_data(),req_type)
			elif req_type.split(';')[0] == 'multipart/form-data':
				uploaded_files = reqt.files
				data="multipart"
    		else:
				data=parse(data)
		return data



#function for extraction of headers
#author -Supermacy

def get_header(req):
	headers=req.headers
	data=dict()
	if headers.get('accessToken'):
		data['access_token']=headers.get('accessToken')
	if headers.get("deviceId"):
		data['device_id']=headers.get('deviceId')
	data['content_type']=headers.get('Content-Type')
	data['user_agent']=headers.get('User-Agent')
	return data	
