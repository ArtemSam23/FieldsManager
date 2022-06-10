from fastapi import HTTPException

class GetItemException(HTTPException):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return 'GetItemException, {0} '.format(self.message)
        else:
            return 'GetItemException has been raised'


