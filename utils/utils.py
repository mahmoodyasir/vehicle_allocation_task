from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse


def create_response(success: bool, message: str, status_code: int, **kwargs):
    return JSONResponse(status_code=status_code, content={'success': success, 'message': message, **jsonable_encoder(kwargs)})