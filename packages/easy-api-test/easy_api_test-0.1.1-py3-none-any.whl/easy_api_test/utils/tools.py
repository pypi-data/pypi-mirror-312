import datetime
from io import BytesIO
from typing import Any, Callable, TypedDict
from lljz_tools.excel import ExcelWriter

class ParametrizeData[T](TypedDict):
    argvalues: list[T]
    ids: list[str]

def p[T](*args: tuple[str, T]) -> ParametrizeData[T]:
    return ParametrizeData(argvalues=[d[1] for d in args], ids=[d[0] for d in args])


def get_time_range(start: int = 0, end: int = 0, start_key: str = 'startTime', end_key: str = 'endTime') -> dict[str, str]:
    today = datetime.date.today()
    start_date = today - datetime.timedelta(days=start)
    end_date = today - datetime.timedelta(days=end)
    return {start_key: f'{start_date} 00:00:00', end_key: f'{end_date} 23:59:59'}


def remove_null_values[T: Any](data: T) -> T:
    """
    移除字典或列表、元组、集合中的空值

    :param data: 字典或列表、元组、集合
    :return: 移除空值后的字典或列表、元组、集合
    """
    if isinstance(data, dict):
        return {k: remove_null_values(v) for k, v in data.items() if v is not None} # type: ignore
    elif isinstance(data, list | tuple | set):
        return type(data)(remove_null_values(v) for v in data)  # type: ignore
    else:
        return data


def assert_not_with_system_error(func: Callable, *args: Any, system_error_message: str = '系统错误', show_error_message: str = '此处期望执行失败，实际执行成功！', **kwargs: Any):
    """
    期望方法执行失败，且不能是系统错误

    :param func: 方法
    :param args: 方法参数
    :param system_error_message: 用来断言判断是否为系统错误的错误信息
    :param show_error_message: 断言失败后显示的错误信息
    :param kwargs: 方法参数
    """

    try:
        func(*args, **kwargs)
    except AssertionError as e:
        assert system_error_message in str(e), str(e)
    else:
        raise AssertionError(show_error_message)


def to_excel_data(data: list[dict]) -> bytes:
    """
    将列表转换为Excel文件数据
    """
    file = BytesIO()
    excel = ExcelWriter(file)
    excel.write(iter(data))
    excel.save()
    return file.getvalue()