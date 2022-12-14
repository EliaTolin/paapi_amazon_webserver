import decimal


def get_meta(page: int = 0, total_element: int = 0, category: str = ""):
    meta = {'page': page, 'total_element': total_element, 'category': category}
    return meta


def get_final_meta(total_time_s: decimal = 0, total_element: int = 0, category: str = ""):
    meta = {'total_time_s': total_time_s, 'total_element': total_element, 'category': category}
