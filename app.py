from resources import application
from flask import request
import urls
application.debug=True;

if __name__ == '__main__':
    application.run(host='0.0.0.0',port=8091)
