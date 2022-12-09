import config
import init_server as init
import init_services.celery_services as celery_services
from init_services.factory_services import *


if __name__ == '__main__':
    if init.init_server():
        app = init_services(celery=celery_services.celery_app)
        app.run(host='0.0.0.0', debug=config.DEBUG)
    else:
        print("###### THERE WAS AN ERROR, CHECK THE LOGS ######")
        exit(-1)
