"""Modulo con la metaclase para aplicar el patron Singleton"""
class SingletonMetaclass(type):
    """Metaclase Singleton"""
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]
