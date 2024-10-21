class EntityNotFoundError(Exception):
    def __init__(self, status_code:int=400, message:str="Entity is not found."):
        self.status_code = status_code
        self.message = message
        super().__init__(self.message)
        

class ServerInvalidError(Exception):
    def __init__(self, status_code:int=400, message:str="Invalid server type."):
        self.status_code = status_code
        self.message = message
        super().__init__(self.message)
        
class  NotAcceptableError(Exception):
    def __init__(self, status_code:int=406, message:str="Not acceptable"):
        self.status_code = status_code
        self.message = message      
        super().__init__(self.message)
        
class AcknowledgementError(Exception):
    def __init__(self, message:str="Invalid Operation"):
        self.message = message
        super().__init__(self.message)  
        
class ImproperConfigurationError(Exception):
    def __init__(self, message:str="Problem with MongoDB environment variables") -> None:
        super().__init__(message)


class BadRequestError(Exception):
    def __init__(self, status_code:int=400, message:str="Bad Request"):
        self.status_code = status_code
        self.message = message      
        super().__init__(self.message)