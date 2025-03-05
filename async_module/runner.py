import asyncio
import functools
import threading
from queue import Queue
from typing import Any, Awaitable, Callable


class AsyncSyncRunner:
    """
    동기 코드 내에서 비동기 코드를 실행하는 러너.
    - 이벤트 루프가 없는 경우 : asyncio.run()
    - 이미 이벤트 루프가 실행 중인 경우 : 별도의 스레드를 생성 후 asyncio.run() 실행
    """

    @staticmethod
    def run(coro: Awaitable) -> Any:
        try:
            asyncio.get_running_loop()
        except RuntimeError:
            return asyncio.run(coro)
        else:
            return AsyncSyncRunner._run_in_thread(coro)

    @staticmethod
    def _run_in_thread(coro: Awaitable) -> Any:
        q: Queue = Queue()

        def target():
            try:
                result = asyncio.run(coro)
                q.put((True, result))
            except Exception as e:
                q.put((False, e))

        thread = threading.Thread(target=target)
        thread.start()
        thread.join()

        success, value = q.get()
        if success:
            return value
        else:
            raise value


def async_to_sync(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return AsyncSyncRunner.run(func(*args, **kwargs))

    return wrapper
