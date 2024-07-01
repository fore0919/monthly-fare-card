class LogHelper:
    hash_id: str
    url: str
    client_ip: str
    method: str
    data: dict

    def __init__(self, hash_id, url, client_ip, method, data):
        self.hash_id = hash_id
        self.url = url
        self.client_ip = client_ip
        self.method = method
        self.data = data

    @property
    def message(self) -> dict:
        return {
            "data": self.data,
            "method": self.method,
            "hash_id": self.hash_id,
        }

    @property
    def extra(self) -> dict:
        return {"url": self.url, "remote_addr": self.client_ip}
