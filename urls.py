
import os
import controllers
from resources import *



api.add_resource(controllers.first_class,'/api/v1.0/tasks')

api.add_resource(controllers.second_class,'/api/v1.0/tasks2')

api.add_resource(controllers.index,'/api/v1.0/index')

api.add_resource(controllers.check_connection,'/api/v1.0/connect')


#examle api url for get request with vairable
api.add_resource(controllers.get_request,'/api/v1.0/get_req/<int:id>/<int:ty>')



#examle api url for post request with vairable
api.add_resource(controllers.post_request,'/api/v1.0/upload_video',methods=['POST','PUT'])

#url for checking login
api.add_resource(controllers.login_check,'/api/v1.0/login',methods=['POST'])
api.add_resource(controllers.logout_check,'/api/v1.0/logout',methods=['POST'])



#endpoint for profile

api.add_resource(controllers.profile,'/api/v1.0/profile',methods=['POST'])

#for gettting connections
#api.add_resource(controllers.connections,'/api/v1.0/connections',methods=['POST'])

#for sending connection request
#api.add_resource(controllers.add_friend,'/api/v1.0/add_friend',methods=['POST'])
#api.add_resource(controllers.respond_add_friend,'/api/v1.0/respond_add_friend',methods=['POST'])

