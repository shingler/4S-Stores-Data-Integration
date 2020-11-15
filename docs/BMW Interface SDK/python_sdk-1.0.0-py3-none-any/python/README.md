## 文档



### 数据签名

```python
from sign.security_util import get_signature_dict

data = get_signature_dict(ori_data)

# data即为签名后的字典
# get_signature_dict可以将请求方法作为关键字参数传入
```



### 接口

#### `get_signature_dict`

`get_signature_dict(sign_data, method='GET')`

- `sign_data`：字典，包含了要签名的字段
- `method`：请求方法

该接口返回签名后的字典