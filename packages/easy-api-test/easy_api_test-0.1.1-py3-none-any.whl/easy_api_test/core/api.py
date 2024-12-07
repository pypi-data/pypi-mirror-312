

from typing import TypeVar, Generic
from easy_api_test.core.http_client import HTTPClient


T = TypeVar('T', bound=HTTPClient)

class API:
    
    
    def __init__(self, http_client: HTTPClient):
        self.client = http_client
