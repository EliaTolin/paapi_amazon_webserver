import config
import init_server as init
from services.factory_services import *

flask_app = init_services()
 
if __name__ == '__main__':
    if init.init_server():   
        flask_app.run(host='0.0.0.0', debug=config.DEBUG)
    else:
        print("###### THERE WAS AN ERROR, CHECK THE LOGS ######")
        exit(-1)
