import config
import init_server as init
from init_services.celery_init import make_celery
from init_services.flask_init import make_flask


app = make_flask()
celery = make_celery(app)


@app.route('/')
def hello_world():
    return 'Hello, PA API Amazon Server!\n'


if __name__ == '__main__':
    if init.init_server():
        app.run(host='0.0.0.0', debug=config.DEBUG)
    else:
        print("###### THERE WAS AN ERROR, CHECK THE LOGS ######")
        exit(-1)
