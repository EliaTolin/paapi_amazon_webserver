import json
import constant.response_constants as response_constant
import constant.exception.generic_error_code_message as generic_error_code_message


def make_response(data="", status_code=generic_error_code_message.no_error):
    try:
        response = dict()
        response[response_constant.data_field] = data
        response[response_constant.status_field] = status_code
        return json.dumps(response).replace("\"", "\'")

    except TypeError:
        raise TypeError
    except ValueError:
        raise ValueError
