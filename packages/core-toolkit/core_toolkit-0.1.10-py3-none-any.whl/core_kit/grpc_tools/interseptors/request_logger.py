import logging
from typing import Any, Callable

import grpc
from google.protobuf.json_format import MessageToJson
from grpc_interceptor import AsyncServerInterceptor

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RequestLoggerInterceptor(AsyncServerInterceptor):
    async def intercept(
            self,
            method: Callable[..., Any],
            request_or_iterator: Any,
            context: grpc.ServicerContext,
            method_name: str,
    ) -> Any:
        logger.info(f"Received request: {MessageToJson(request_or_iterator)}")
        result = await super().intercept(method, request_or_iterator, context, method_name)
        logger.info(f"Response: {MessageToJson(result)}")
        return result
