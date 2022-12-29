import tracemalloc

import fastapi
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis.asyncio.client import Redis
from sqlalchemy.util import greenlet_spawn
from starlette.middleware.base import BaseHTTPMiddleware

from config import CORS_ALLOWED_ORIGINS_REGEX
from fix_backward_compatibility import fix_compatibility
from middlewares.response_validation import response_validation_middleware, \
    parse_raw
from middlewares.server_timing import ServerTimingMiddleware
from root_router import root_router
from exceptions_handler import cors_handler

tracemalloc.start()
app = FastAPI(exception_handlers={500: cors_handler})
app.include_router(root_router)

app.add_middleware(
    BaseHTTPMiddleware,
    dispatch=response_validation_middleware
)

app.add_middleware(ServerTimingMiddleware, calls_to_track={
    'dependencies_execution': (fastapi.routing.solve_dependencies,),
    'endpoint_running': (fastapi.routing.run_endpoint_function,),
    'pydantic_validation': (fastapi.routing.serialize_response,),
    'pydantic_validation_': (parse_raw,),
    'json_rendering': (
        fastapi.responses.JSONResponse.render,
        fastapi.responses.ORJSONResponse.render,
    ),
    'sql_requests': (greenlet_spawn,),
    'redis_requests': (Redis.execute_command,),
    'total': (response_validation_middleware,)
})

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origin_regex=CORS_ALLOWED_ORIGINS_REGEX,
    allow_methods=['*'],
    allow_headers=['*'],
)

fix_compatibility()
