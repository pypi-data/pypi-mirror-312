from typing import Callable
from django.http import HttpResponse, HttpRequest


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
