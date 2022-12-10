from enum import Enum
import time



class TypeMessage(Enum):
    INFO = 1
    WARNING = 2
    ERROR = 3
    SUCCESS = 4


def show_message_debug(message: " ", type_message: TypeMessage = TypeMessage.INFO):
    base_message = "####{0}#### {1} ####{2}####"
    if type_message == TypeMessage.INFO:
        print(base_message.format(time.strftime("%d-%m-%Y %H:%M:%S"),message, "INFO"))
    elif type_message == TypeMessage.WARNING:
        print(base_message.format(time.strftime("%d-%m-%Y %H:%M:%S"),message, "WARNING"))
    elif type_message == TypeMessage.ERROR:
        print(base_message.format(time.strftime("%d-%m-%Y %H:%M:%S"),message, "ERROR"))
    elif type_message == TypeMessage.SUCCESS:
        print(base_message.format(time.strftime("%d-%m-%Y %H:%M:%S"),message, "SUCCESS"))
