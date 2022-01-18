import fastapi.encoders
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

from api.handlers import api_router
from index_router import index_router
from middlewares.response_validation import response_validation_middleware, parse_raw
from middlewares.server_timing import ServerTimingMiddleware

app = FastAPI()
app.include_router(api_router)
app.include_router(index_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origin_regex=r'https?://localhost:[0-9]{1,5}',
    allow_methods=['*'],
    allow_headers=['*'],
)

app.add_middleware(
    BaseHTTPMiddleware,
    dispatch=response_validation_middleware
)

app.add_middleware(ServerTimingMiddleware, calls_to_track={
    'dependencies_execution': (fastapi.routing.solve_dependencies,),
    'endpoint_running': (fastapi.routing.run_endpoint_function,),
    'pydantic_validation': (parse_raw,),
    'json_rendering': (
        fastapi.responses.JSONResponse.render,
        fastapi.responses.ORJSONResponse.render,
    ),
    'total': (response_validation_middleware,)
})
