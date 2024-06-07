from typing import Optional


class BaseException(Exception):
    code = 400
    error_no = 100
    message: str

    def __init__(
        self,
        message: str | None = None,
        error_args: tuple = (),
        data: dict | list | None = None,
    ):
        if not error_args:
            error_args = (self.error_no, message)
        super().__init__(*error_args)
        self.message = message
        self.additional_data = data


class NotOKResponseError(BaseException):
    code: int = 500
    error_no: int = 500

    request_data: Optional[dict] = None
    response_status_code: int = None
    response_data: Optional[dict] = None

    def __init__(
        self,
        url,
        request_data,
        response_status_code,
        response_data,
        message: str = "외부 서버 HTTP 요청 실패.",
    ):
        super().__init__(
            message,
            error_args=(response_status_code, response_data),
        )
        self.url = url
        self.request_data = request_data
        self.response_status_code = response_status_code
        self.response_data = response_data

    def __repr__(self) -> str:
        return (
            f"NotOKResponseError(\n"
            f"\turl={self.url}\n"
            f"\trequest_data={self.request_data}\n"
            f"\tstatus_code={self.response_status_code}\n"
            f"\tmessage={self.response_data}\n"
            f")"
        )
