def list_to_json(list_items):
    json_list = []
    for item in list_items:
        json_list.append(item.to_json().replace("\"", "\'"))
    return json_list
