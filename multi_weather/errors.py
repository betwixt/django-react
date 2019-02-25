




class AerisAPIError(Exception):
    def __init__(self, errcode):
        self.errcode = errcode

#  When cannot get proper response from weather api, usually due to invalid key
class ConnectionError(Exception):
    pass


#  When weather api reports error due to incomplete data for request
class InputValueError(AerisAPIError):
    pass
