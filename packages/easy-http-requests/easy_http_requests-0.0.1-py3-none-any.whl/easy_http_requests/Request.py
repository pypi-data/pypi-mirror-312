class Request:
    def __init__(self, method, url, headers=None, body=None):
        self.method = method
        self.url = url
        self.headers = headers
        self.body = body

    def __str__(self):
        return f"Request(method={self.method}, url={self.url}, headers={self.headers}, body={self.body})"
