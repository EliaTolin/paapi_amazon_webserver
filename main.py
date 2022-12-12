import config
import helper.debug_message as dbg_message
import init_server as init
from services.factory_services import *
import traceback

flask_app = init_services()

if __name__ == '__main__':
    try:
        if init.init_server():
            flask_app.run(host='0.0.0.0', debug=config.DEBUG)
        else:
            print("###### THERE WAS AN ERROR, CHECK THE LOGS ######")
            exit(-1)

    except Exception as e:
        dbg_message.show_message_debug(message="EXCEPTION CAPTURED IN MAIN",
                                       type_message=dbg_message.TypeMessage.ERROR)
        traceback.print_exc()
