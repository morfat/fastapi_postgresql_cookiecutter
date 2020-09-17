from fastapi import FastAPI, Request, status

from app.api.api_v1.api import api_router

from app.api.errors import HTTPRequestError
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from fastapi.encoders import jsonable_encoder

app = FastAPI(debug=True, version="1.0", title="API")

app.include_router(
    api_router,
    prefix="/v1"
)

@app.exception_handler(HTTPRequestError)
async def bad_request_exception_handler(request: Request, exc: HTTPRequestError):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            'code': exc.code,
            'message': exc.message,
            'detail': exc.detail
        }
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    ''' "content=jsonable_encoder({"detail": exc.errors(), "body": exc.body})," '''


    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({
            'code': 'invalid_request',
            'message': 'Request Validation Error',
            'detail': exc.errors()
        })
    )
   

