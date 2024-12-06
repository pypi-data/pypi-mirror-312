

from easy_api_test.core.http_client import HttpClient


class API[T: HttpClient]:
    
    
    def __init__(self, http_client: T):
        self.client: T = http_client
