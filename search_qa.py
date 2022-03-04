

from open_search import client, index_name
from encode import encode
from similarity import similarity
from api_config import get_settings


def search_qa(query, size=5, token=None):

    body = {
        '_source': ['Q_text', 'Ans_url', "Ans_text"],
        'size': size,
        'query': {
            "bool": {
                "should": []
            }
        }
    }

    c = get_settings(token)
    if c['semantic_title'] > 0.0:
        weight = c['semantic_title']
        # body['query']['bool']['should'].append({
        #     "knn": {
        #         "Q_vec": {
        #             "vector": encode(query),
        #             "k": 3,
        #         }
        #     }
        # })
        body['query']['bool']['should'].append({
            "script_score": {
                "query": {
                    "match_all": {}
                },
                "script": {
                    "source": f"(1.0 + cosineSimilarity(params.query_value, doc[params.field])) * {weight}",
                    "params": {
                        "field": "Q_vec",
                        "query_value": encode(query)
                    }
                }
            }
        })
    if c['lexical_title'] > 0.0:
        body['query']['bool']['should'].append({
            "match": {
                "Q_text": {
                    "query": query,
                    "boost": c['lexical_title'],
                }
            }
        })
    if c['lexical_answer'] > 0.0:
        body['query']['bool']['should'].append({
            "match": {
                "Ans_text": {
                    "query": query,
                    "boost": c['lexical_answer'],
                }
            }
        })

    response = client.search(
        body=body,
        index=index_name
    )
    return response


def search_qa_format(query, size=5, token=None):
    c = get_settings(token)
    response = search_qa(query=query, size=size, token=token)
    print(response)
    response = [x['_source'] for x in response['hits']['hits']]
    response = [
        {
            'q': x['Q_text'],
            'url': x['Ans_url'],
            'sim': similarity(x['Q_text'], query),
            'text': f'{x["Q_text"]}\n{x["Ans_url"]}'
        }
        for i, x in enumerate(response)
    ]
    response = sorted(response, key=lambda x: x['sim'], reverse=True)

    if response[0]['sim'] >= 0.9:
        filtered_response = [x for i, x in enumerate(response) if i < c['threshold_90'] or x['sim'] >= 0.9]
    elif response[0]['sim'] >= 0.8:
        filtered_response = [x for i, x in enumerate(response) if i < c['threshold_80'] or x['sim'] >= 0.8]
    elif response[0]['sim'] >= 0.7:
        filtered_response = [x for i, x in enumerate(response) if i < c['threshold_70'] or x['sim'] >= 0.7]
    elif response[0]['sim'] >= 0.6:
        filtered_response = [x for i, x in enumerate(response) if i < c['threshold_60'] or x['sim'] >= 0.6]
    else:
        filtered_response = []

    if len(filtered_response) <= 0:
        return '我找不到这个问题的答案，您是不是要问：\n' + '\n'.join([
            f"{i + 1}. {x['q']} ( {x['url']} ) "
            for i, x in enumerate(response[:3])
        ])
    else:
        response = filtered_response

    if len(response) > 1:
        for i, x in enumerate(response):
            x['text'] = f"{i + 1}. {x['text']}"

    return '\n'.join(map(lambda x: x['text'], response))


if __name__ == '__main__':
    print(search_qa_format('申请流程'))
    while True:
        i = input('> ')
        print(search_qa_format(i))
