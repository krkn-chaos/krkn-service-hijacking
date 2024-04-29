class HttpRequest:
    timestamp: float
    response_body: str
    response_status_code: int
    request_path: str

    def __init__(
        self,
        timestamp: float,
        response_body: str,
        response_status_code: int,
        request_path: str,
    ):
        self.timestamp = timestamp
        self.response_body = response_body
        self.response_status_code = response_status_code
        self.request_path = request_path
