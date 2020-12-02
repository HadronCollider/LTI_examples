REQUEST_INFO = ('headers', 'data', 'url', 'secret')


def check_content(data):
    for key in REQUEST_INFO:
        if key not in data: raise KeyError("Required param '{}' not in {}".format(key, data))
