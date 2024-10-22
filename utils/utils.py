from datetime import date, datetime
from decimal import Decimal
from uuid import UUID
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse


def create_response(success: bool, message: str, status_code: int, **kwargs):
    return JSONResponse(status_code=status_code, content={'success': success, 'message': message, **jsonable_encoder(kwargs)})



def default_converter(o):
    if isinstance(o, datetime):
        return o.__str__()
    elif isinstance(o, date):
        return o.__str__()
    elif isinstance(o, UUID):
        return o.__str__()
    elif isinstance(o, Decimal):
        return float(o)
    else:
        raise TypeError(f"Object of type {o.__class__.__name__} is not JSON serializable")