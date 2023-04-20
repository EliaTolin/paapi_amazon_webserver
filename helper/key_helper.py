import constant.database.database_constants as database_constants


def get_key_redis(category: str, keywords: str = None):
    if keywords is not None:
        return "{0}_{1}".format(category, keywords.replace(' ', '_'))
    return "{0}".format(category)


def get_key_too_many_redis(category: str, keywords: str = None):
    return "{0}{1}".format(get_key_redis(category, keywords), database_constants.key_suffix_error_too_many)


def get_key_completed_category_redis(category: str, keywords: str = None):
    return "{0}{1}".format(get_key_redis(category, keywords), database_constants.key_suffix_completed_data)


def get_key_preference_category_redis(category: str, keywords: str = None):
    return "{0}{1}".format(get_key_redis(category, keywords), database_constants.key_suffix_preference)
