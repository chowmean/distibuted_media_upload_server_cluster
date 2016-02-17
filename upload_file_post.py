import os,time,random
ALLOWED_EXTENSIONS = set(['mp4','txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','py','csv'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def upload_file_data(reqt,folder):
	if reqt.method == 'POST':
		file = reqt.files
	#	print file['files']
		file_list=[]
		for key, value in file.iteritems():
			if value and allowed_file(value.filename):
				exten=value.filename.rsplit('.', 1)[1]
				file_name=str(int(time.time()))+str(random.randint(1000,9999))+value.filename
				value.save(os.path.join(folder,file_name))
				file_list.append(file_name)
	return file_list
