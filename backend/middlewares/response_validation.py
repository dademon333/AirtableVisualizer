from typing import Any, Sequence, Union, Type

from fastapi import Request
from fastapi.routing import APIRouter
from pydantic import BaseModel
from pydantic.main import ModelMetaclass
from starlette.responses import StreamingResponse
from starlette.routing import Match


def parse_raw(model: Type[BaseModel], content: Union[bytes, str]):
    """Обертка над методом pydantic.BaseModel.parse_raw

    Создано, чтобы замерять скорость этого метода при вызове в response_validation_middleware
    Замеряется с помощью ServerTimingMiddleware, результат попадает в header 'server-timing' всех ответов
    """
    return model.parse_raw(content)


class AsyncGenerator:
    """Возвращает async версию генератора на основе переданной последовательности"""
    def __init__(self, items: Sequence[Any]):
        self.items = items
        self.iterator = items.__iter__()

    def __aiter__(self):
        return self

    async def __anext__(self):
        try:
            return self.iterator.__next__()
        except:
            raise StopAsyncIteration


async def response_validation_middleware(request: Request, call_next):
    """Валидирует ответ сервера с помощью pydantic

    Проблема: fastapi.routing.serialize_response, который используется для валидации ответа endpoint'а,
    слишком медленный (160 кб валидируются ~300-400 мсек)
    Решение: возвращать ORJSONResponse. В этом случае fastapi не проводит валидацию
    Эту функцию берет на себя данный middleware.
    Из ответа он вытаскивает response_model и проводит проверку простым вызовом parse_raw
    При размере в 160 кб достигается ускорение в 10 раз (~30 мсек)

    Дополнительно: с помощью замера скорости этой функции также вычисляется итоговое время ответа сервера
    и добавляется в header 'server-timing' с помощью ServerTimingMiddleware
    """
    response: StreamingResponse = await call_next(request)
    response_body = [x async for x in response.body_iterator]  # Ответ представлен в виде async-генератора
    response.body_iterator = AsyncGenerator(response_body)  # Проитерировав исходный генератор, подставляем непроитерированную копию

    router: APIRouter = request.scope['router']
    for route in router.routes:
        match, _ = route.matches(request.scope)
        if match == Match.FULL \
                and hasattr(route, 'response_model') \
                and issubclass(route.response_model.__class__, ModelMetaclass):
            parse_raw(route.response_model, response_body[0])
            break

    return response
