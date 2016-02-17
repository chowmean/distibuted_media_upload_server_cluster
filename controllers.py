import json
from flask.ext.restful import Resource
from flask import request 
from connection import *
from _parser_app import *
from upload_file_post import *
from resources import *
from oauth_permission import *
from profiles import *
from login_checker import *

## to check permission for particuar user for an endpoint use this
#  check_role_permission(get_role_id(access_token,device_id),"endpoint name")



class check_connection(Resource):
	def get(self):
		if connect() != False:
	    		return {"connect":True,"succes":True}
		else:	
			return {"connect":False,"succes":True}

#examle api get_request class controller for get request with variable
class get_request(Resource):
	def get(self,id,ty):
		return {"data":"this is the second class","succes":True,"id":id,"ty":ty}


class index(Resource):
	def get(self):
    		return {"message":"another end point","succes":True}


class first_class(Resource):
	def get(self):
		return {"data":"hey","succes":True}



class second_class(Resource):
	def get(self):
		return {"data":"this is the second class","succes":True}


class post_request(Resource):
	def post(self):
		if parse_main(request)=='multipart':
			return upload_file_data(request,UPLOAD_FOLDER)
		b=get_header(request)
		a=parse_main(request)
		print b
		return a
	def put(self):
			return parse_main(request)

#author =supermacy
#login checker url


class login_check(Resource):
	def post(self):
		user_json=parse_main(request)
		print user_json
		if "success" in user_json.keys():
			if(user_json['success']==False):
		  		return user_json
		header=get_header(request)
		ret=login(user_json,header['device_id'])
		return ret


class logout_check(Resource):
	def post(self):
		header=get_header(request)
		access_token=header['access_token']
		ret =logout(access_token)
		return ret

#till here


class profile(Resource):
	def post(self):
		print request.headers
		user_data=parse_main(request)
		print user_data
		if "success" in user_data.keys():
			if(user_data['success']==False):
				return user_data
		else: 
			return {"message":"internal server error","success":"false"}
		username=user_data['username']
		header=get_header(request)
		device_id=header['device_id']
		if 'access_token' in  header.keys():
			access_token=header['access_token']
			print access_token
			user_id=get_user_id(access_token)
			if user_id==-1:
				return {"message":"user does not exists","success":False}
			#see spelling of pro
		 	a=check_role_permission(get_role_id(access_token,device_id),'profile')	
			print 'value permission',a
			if a['success']==True:
				f_user_id=get_user_id_from_username(username)
				if f_user_id==user_id:
					return get_profile(username,"full")
				else:
					if is_friend(user_id,f_user_id):
						return get_profile(username,"full")
					else:
						return get_profile(username)
			else:
					return {"message":"trying to get unauthorised access","success":False}       

		else:
			return get_profile(username)       
			
			
			
'''					
class connections(Resource):
	def post(self):
		print request.headers
		user_data=parse_main(request)
		print user_data
		if "success" in user_data.keys():
			if(user_data['success']==False):
				return user_data
		header=get_header(request)
		if 'device_id' in header.keys():
			device_id=header['device_id']
		else:
			return {"message":"device not recognized","success":False}
		if 'access_token' in header.keys():
			access_token=header['access_token']
		else:
			return {"message":"user not authorized","success":False}
		user_id=get_user_id(access_token)
	        if user_id == -1:
                                return  {"message":"user not authorized, access token mismatch","success":False}	

		if 'username' in user_data.keys():
			username=user_data['username']
			a=check_role_permission(get_role_id(access_token,device_id),'connections')
			if a['success']==True:
				f_user_id=get_user_id_from_username(username)
				if f_user_id==-1:
					return {"message":"no user with this username","success":False}
				else:	
					if f_user_id==user_id:
						return get_connections(user_id,f_user_id,"full")
					else:
						if is_friend(user_id,f_user_id):
							return get_connection(user_id,f_user_id,"full")
						else:
							return get_connection(user_id,f_user_id,"restricted")
		else:
			a=check_role_permission(get_role_id(access_token,device_id),'connections')
			if a['success']==True:
				return get_connection(user_id)	
			else:
				return {"message":"user not authoriased to use this endpoint","success":False}	
				
				
		
class add_friend(Resource):
	def post(self):
		print request.headers
		user_data=parse_main(request)
		print user_data
		if "success" in user_data.keys():
			if(user_data['success']==False):
				return user_data
		header=get_header(request)
		if 'device_id' in header.keys():
			device_id=header['device_id']
		else:
			return {"message":"device not recognized","success":False}
		if 'access_token' in header.keys():
			access_token=header['access_token']
		else:
			return {"message":"user not authorized","success":False}
		if 'friend_id' in user_data.keys():
			f_id=user_data['friend_id']
			a=check_role_permission(get_role_id(access_token,device_id),'add_friend')
			if a['success']==True:
				return request_friend(get_user_id(access_token),f_id)	
			else:
				return {"message":"user not authoriased to use this endpoint","success":False}	
		else:
			return {"message":"bad request","success":False}
			
			
			
			
			
			
			
				
class respond_add_friend(Resource):
	def post(self):
		user_data=parse_main(request)
		print user_data
		if "success" in user_data.keys():
			if(user_data['success']==False):
				return user_data
		header=get_header(request)
		if 'device_id' in header.keys():
			device_id=header['device_id']
		else:
			return {"message":"device not recognized","success":False}
		if 'access_token' in header.keys():
			access_token=header['access_token']
		else:
			return {"message":"user not authorized","success":False}
		if 'friend_id' in user_data.keys() and 'response' in user_data.keys():
			f_id=user_data['friend_id']
			response=user_data['response']
			a=check_role_permission(get_role_id(access_token,device_id),'respond_add_friend')
			if a['success']==True:
				return confirm_friend(get_user_id(access_token),friend_id,response)	
			else:
				return {"message":"user not authoriased to use this endpoint","success":False}	
		else:
			return {"message":"bad request","success":False}
			
			'''
			
