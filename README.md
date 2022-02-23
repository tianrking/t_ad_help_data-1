#

## 直接运行

### api

```bash
uvicorn QA_api_txad:app --reload --host 0.0.0.0 --port 1333
```

### curl test

里面的数据类型需要调整成int 和bool 待完善
其中 /v1/QA/search 为通用接口 /v1/QA/search/jzmh 为句子秒回回调接口 payload 为讯息 目前还不是标准格式 但是可以用于测试 即修改 payload后文字 测试对应查询

```bash
curl -X POST -k "127.0.0.1:1333/v1/QA/search/jzmh" -H "charset=UTF-8" -H 'Content-Type: application/json' -d' 
{
    "messageId": "2422188041612737714", 
    "chatId": "5e469a2b8d429806b0fef189",
    "avatar": "a",
    "roomTopic": "abc",
    "roomId": "7215325536@chatroom",
    "contactName": "小北",
    "contactId": "wxid_rr9ej1o8xv9h21",
    "payload": {
        "text": "怎么使用朋友圈"
    },
    "type": "MsgType",
    "timestamp": 1585995128441,
    "token": "5dbe8221fc191f13bc072908",
    "botId": "5d0c86971150c017984cee66",
    "contactType": 1,
    "coworker": false, 
    "botId": "5d0c86971150c017984cee77",
    "botWxid": "1688851085873555",
    "botWeixin": "123"
}
'
```

## idea tree

```mermaid
sequenceDiagram
Wechaty->>QA_api: Question xxx
loop Questioncheck
    QA_api->>Opensearch: Question is exist or not    
end
QA_api-->>Wechaty: Answer

```

```mermaid
classDiagram
OpensearchClass --> F1: Question(text)
OpensearchClass --* F2 : Question(vector)
OpensearchClass --|> F3 : Answer
```

```mermaid
flowchart TD 
   %% A[Start] --> B{I?}
%%B -- Yes --> C[OK]
%%    C --> D[Rethink]
  %%  D --> B
    %%B -- No ----> E[End]
```

```mermaid
flowchart LR
  subgraph Opensearch
    direction TB
    subgraph B1
       %% direction LR
        DATA_1 --> Q_text_1
        DATA_1 --> Q_vec_1
        DATA_1 --> Q_ans_1
    end
    subgraph B2
       %% direction LR
        DATA_2 --> Q_text_2
        DATA_2 --> Q_vec_2
        DATA_2 --> Q_ans_2
    end
    subgraph B3
        ...

    end
  end
  Q_text_x --> Opensearch --> Q_ans_X
  Opensearch --> Q_vec_X
  Opensearch --> Q_text_X
  Opensearch --> Q_score_X

  B1 --> B2
  B2 --> B3
  ```

## WIKI

~~当csv数据更新的时候 或想实现其他功能的时候 需要使用新的索引[create_index.py](#create_index.py) ，对于此项目包含每一个数据的构造。 如 idea tree , 每一个 data 中都含有 Q_text , Q_vec , Q_ans 三个属性 分别对应标准查询问题，及其对应的向量，以及Q_ans 对应的回答。~~
~~当接收到文字讯息时候，将字符串x传入 Opensearch 进行检索 得到对应的 data_X 通过返回的信息可以知道 包含对应的 文字问题，文字问题向量，以及对应答案。 通过返回的文字问题向量与输入文字进行比对，来估计检索的可信度。~~

由于 [opensearch](#https://opensearch.org/) 支持 [knn](https://opensearch.org/docs/latest/search-plugins/knn/index/) 搜索 所以上述方式弃用 下面为opensearch [knn 相关调试记录](#相关调试记录)

### 相关调试记录

#### 若 https 证书存在问题  

可加 -k 参数 [取消cURL SSL验证](https://stackoverflow.com/questions/49012543/how-to-disable-curl-ssl-certificate-verification)

#### 初次使用opensearch-knn

需要使用 index.knn 设置创建索引，然后添加一个或多个数据类型为 knn_vector 的字段

方式一 curl

```bash
# 添加支持knn的索引 
curl -X PUT -k "https://admin:admin@localhost:9200/my-index" -H 'Content-Type: application/json' -d'
{
  "settings": {
    "index.knn": true
  },
  "mappings": {
    "properties": {
      "my_vector1": {
        "type": "knn_vector",
        "dimension": 2
      },
      "my_vector2": {
        "type": "knn_vector",
        "dimension": 4
      }
    }
  }
}'
```

方式二 改写opensearch-py

```bash
python create_index.py 
```

#### 添加数据

可以参考此文件添加数据 以便于初次使用

```bash
python add_data.py
```

#### 搜索数据

方式一 curl

```bash
# knn 查询类型搜索数据 
curl -X GET -k "https://admin:admin@localhost:9200/my-index/_search" 

GET my-index/_search
{
  "size": 2,
  "query": {
    "knn": {
      "my_vector2": {
        "vector": [2, 3, 5, 6],
        "k": 2
      }
    }
  }
}

```

方式二 改写opensearch-py

```bash
python change_data.py
```

#### 数据维度修改

因为选用的 sts 模型为 [paraphrase-multilingual-mpnet-base-v2](https://huggingface.co/sentence-transformers/paraphrase-multilingual-mpnet-base-v2)
所以应修改 dimension : 768

### ~~create_index.py~~

1. ~~**Adding document:**~~

```python
document = {
  'Q_text': 'A BC',
  'Q_vec': '123', # for test
  'Answer': 'abc'
}
id = '1'

response = client.index(
    index = index_name,
    body = document,
    id = id,
    refresh = True
)

print(response)

```

2. ~~**Test search key**~~

```python
q = 'BC'
query = {
  'size': 5,
  'query': {
    'multi_match': {
      'query': q,
      # 'fields': ['title^2', 'director']  # 'director'
      'fields': ['Q_text']
    }
  }
}

response = client.search(
    body = query,
    index = index_name
)

print('\nSearch results:')
print(response)
```

Output

```bash
Search results:
{'took': 2, 'timed_out': False, '_shards': {'total': 4, 'successful': 4, 'skipped': 0, 'failed': 0}, 'hits': {'total': {'value': 1, 'relation': 'eq'}, 'max_score': 0.60996956, 'hits': [{'_index': 'abc_test_index', '_type': '_doc', '_id': '1', '_score': 0.60996956, '_source': {'Q_text': 'A BC', 'Q_vec': '123', 'Answer': 'abc'}}]}}
```

#### 开发环境

```bash
Ubuntu 18.04.6 LTS
fastapi                   0.68.2                   pypi_0    pypi
uvicorn                   0.15.0                   pypi_0    pypi
sentence-transformers              2.1.0
transformers                       4.16.2