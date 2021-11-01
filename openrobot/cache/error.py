class OpenRobotCacheException(Exception):
    """Base OpenRobot Cache Exception"""

class UnexpectedType(OpenRobotCacheException):
    """An unexpected type was given."""
    
    def __init__(self, expected_type, returned_type):
        self.expected_type = expected_type
        self.returned_type = returned_type

        super().__init__('Expected %s but got %s instead' % (self._get_name(expected_type), self._get_name(returned_type)))

    def __get_name(self, cls):
        try:
            return cls.__name__
        except:
            try:
                return cls.__class__.__name__
            except:
                if type(cls) == type:
                    return cls
                else:
                    return type(cls)

    def _get_name(self, cls):
        if isinstance(cls, (list, tuple)):
            return ', '.join([self.__get_name(x) for x in cls[:-1]]) + ' or ' + self._get_name(cls[len(cls)-1])
        else:
            return self._get_name(cls)