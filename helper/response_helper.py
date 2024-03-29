import json
import constant.response_constants as response_constant
import constant.exception.generic_error_code_message as generic_error_code_message


def make_response(data="", new_page=None, num_elements=None, status_code=generic_error_code_message.no_error):
    try:
        response = dict()
        response[response_constant.data_field] = data
        response[response_constant.status_field] = status_code
        if new_page:
            response[response_constant.new_page_field] = new_page
        if num_elements:
            response[response_constant.num_elements] = num_elements
        return json.dumps(response)

    except TypeError:
        raise TypeError
    except ValueError:
        raise ValueError
