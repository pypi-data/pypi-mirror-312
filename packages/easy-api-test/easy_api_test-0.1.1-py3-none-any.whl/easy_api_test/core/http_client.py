from io import BytesIO
from logging import Logger
from multiprocessing import Value
from lljz_tools.client.http_client import HTTPClient as _HTTPClient
from lljz_tools.excel import ExcelReader    
from requests import JSONDecodeError

from easy_api_test.utils.tools import to_excel_data 
from .logger import logger

class HTTPClient(_HTTPClient):

    def __init__(self, base_url: str, *, timeout: int = 60, debug: bool | Logger = True):
        super().__init__(base_url, timeout=timeout, debug=logger if debug is True else debug )


    def post_import_excel(self, url: str, data: list[dict], files_key: str = 'file'):
        """
        上传excel文件，方法会直接将data转换为Excel文件数据并上传
        """
        file = to_excel_data(data)
        return self.post(url, files={files_key: file})

    def get_response_excel(self, status_code=200, *, excel_start_row: int = 1):
        """
        获取响应的Excel文件数据


        :param status_code: 状态码，默认值200
        :param excel_start_row: Excel文件起始行，默认值1

        """
        if not self._response:
            raise ValueError("请先执行请求！")
        assert self._response.status_code == status_code, \
            (f'请求失败，预期[{status_code}]、实际[{self._response.status_code}]。'
             f'响应结果为：{self._response.text[:200]}')
        assert self._response.headers['Content-Disposition'].startswith('attachment;')
        data = self._response.content
        ioData = BytesIO(data)
        excel = ExcelReader(ioData)
        return excel.read(min_row=excel_start_row)
