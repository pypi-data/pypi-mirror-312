

def singleton(cls):
    """
    A singleton decorator that ensures only one instance of a class is created.
    """
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance
