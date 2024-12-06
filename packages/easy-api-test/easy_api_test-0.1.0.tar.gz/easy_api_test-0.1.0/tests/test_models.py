import sys
import os
from typing import Any, Union
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from easy_api_test.core.models import Model

def test_dict_conversion():
    # 测试字典转换
    data = {
        'id': 1,
        'name': 'test',
        'details': [
            {'id': 1, 'name': 'detail1'},
            {'id': 2, 'name': 'detail2'}
        ],
        'metadata': {
            'created_at': '2024-03-20',
            'tags': ['tag1', 'tag2']
        }
    }
    model = Model.from_dict(data)
    
    # 验证转换结果
    assert isinstance(model, Model)
    assert isinstance(model.metadata, Model)
    assert isinstance(model.details[0], Model)
    assert model.details[0].name == 'detail1'
    assert model.metadata.tags == ['tag1', 'tag2']
    print("Dict conversion test passed!")

def test_list_conversion():
    # 测试列表转换
    data = [
        {'id': 1, 'name': 'test1', 'details': [{'id': 1, 'name': 'detail1'}]},
        {'id': 2, 'name': 'test2', 'details': [{'id': 2, 'name': 'detail2'}]}
    ]
    models = Model.from_list(data)
    
    # 验证转换结果
    assert isinstance(models, list)
    assert all(isinstance(m, Model) for m in models)
    assert isinstance(models[0].details[0], Model)
    assert models[0].name == 'test1'
    assert models[1].details[0].name == 'detail2'
    print("List conversion test passed!")


def test_type_hint():
    class User(Model):
        id: int | str  # 使用新语法
        name: str
        age: Union[int, float]  # 使用传统语法
        scores: list[float]
        settings: dict[str, Any]
        tags: list[str] | None  # 使用新语法
        
    user = User.from_dict({'id': 1, 'name': 'test', 'age': 20, 'scores': [90, 80, 70], 'settings': {'theme': 'light'}, 'tags': ['python', 'programming']})
    print(user.id)
if __name__ == "__main__":
    test_dict_conversion()
    test_list_conversion()