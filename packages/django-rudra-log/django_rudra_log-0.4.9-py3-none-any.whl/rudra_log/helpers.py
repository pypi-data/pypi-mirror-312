import traceback
from typing import Callable

from asgiref.sync import iscoroutinefunction, markcoroutinefunction
from django.conf import settings
from django.http import HttpRequest, HttpResponse


class LogSettings:
    def __init__(
        self,
        url: str,
        env_key: str,
        enabled: bool,
        app_exception_handler: Callable[[HttpRequest, Exception, str], HttpResponse],
        can_ignore_exception: Callable[[Exception], bool] = lambda x: False,
        paths_to_exclude: list[str] = [],
        clean_header: Callable[[dict], dict] = lambda x: x,
        get_status_code: Callable[[HttpResponse], int] = lambda x: x.status_code,
        thread_pool_size: int = 24,
    ):
        self.url = url
        self.env_key = env_key
        self.enabled = enabled
        self.app_exception_handler = app_exception_handler
        self.can_ignore_exception = can_ignore_exception
        self.paths_to_exclude = paths_to_exclude
        self.clean_header = clean_header
        self.get_status_code = get_status_code
        self.thread_pool_size = thread_pool_size


class MiddlewareWrapper:
    """
    This class is a wrapper around the middleware class, it helps to catch exceptions raised by custom middleware and handle them by the app_exception_handler.
    """

    settings: LogSettings
    async_capable = True
    sync_capable = False

    def __init__(self, get_response):
        self.settings = getattr(settings, "LOG_SETTINGS")
        self.get_response = get_response
        if iscoroutinefunction(self.get_response):
            markcoroutinefunction(self)

    async def process(self, request):
        raise NotImplementedError

    async def __call__(self, request):
        try:
            return await self.process(request)
        except Exception as e:
            if not self.settings.enabled or not self.settings.can_ignore_exception(e):
                raise e
            return self.settings.app_exception_handler(
                request, e, traceback.format_exc()
            )
