import uuid
from datetime import datetime
from json import JSONDecodeError

from starlette.requests import Request

from app.helper.logger import LogHelper


async def log_request(request: Request) -> None:
    if request.url.path == "/healthz":
        return None
    hash_id = uuid.uuid4().hex[:6]
    url = str(request.url).split("?")[0]
    client_ip = request.client.host
    method = request.method
    if method == "GET":
        data = dict(request.query_params)
    else:
        if (
            request.headers.get("content-type")
            == "application/x-www-form-urlencoded"
        ):
            data = dict(await request.form())
        else:
            try:
                data = await request.json()
            except JSONDecodeError as jde:
                data = "JSONDecodeError while logging request"
            except Exception as e:
                data = (await request.body()).decode().replace("\\n", "\n")

    log = LogHelper(hash_id, url, client_ip, method, data)
    log.request_time = datetime.now()
    request.state.log = log
    return log
