import helper.debug_message as dbg_message
import init_server as init
from services.factory_services import *
import traceback

flask_app = init_services()

if __name__ == '__main__':
    try:
        if not init.init_server():
            print("###### THERE WAS AN ERROR, CHECK THE LOGS ######")
            exit(-1)

    except Exception as e:
        dbg_message.show_message_debug(message="EXCEPTION CAPTURED IN MAIN",
                                       type_message=dbg_message.TypeMessage.ERROR)
        traceback.print_exc()
