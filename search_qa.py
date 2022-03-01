

from open_search import client, index_name
from encode import encode
from similarity import similarity


def search_qa(query, size=5):
    # _Q_vec = encode(query)

    query = {
        '_source': ['Q_text', 'Ans_url', "Ans_text"],
        'size': size,
        'query': {
            "bool": {
                "should": [
                    {
                        "knn": {
                            "Q_vec": {
                                "vector": encode(query),
                                "k": 3,
                            }
                        }
                    },
                    {
                        "match": {
                            "Q_text": {
                                "query": query,
                                "boost": 1,
                            }
                        }
                    },
                    {
                        "match": {
                            "Ans_text": {
                                "query": query,
                                "boost": 0.1,
                            }
                        }
                    }
                ]
            },
        }
    }

    response = client.search(
        body=query,
        index=index_name
    )
    return response


def search_qa_format(query, size=5):
    response = search_qa(query, size)
    print(response)
    response = [x['_source'] for x in response['hits']['hits']]
    response = [
        {
            'q': x['Q_text'],
            'url': x['Ans_url'],
            'sim': similarity(x['Q_text'], query),
            'text': f'{i + 1}. {x["Q_text"]}\n{x["Ans_url"]}'
        }
        for i, x in enumerate(response)
    ]
    response = sorted(response, key=lambda x: x['sim'], reverse=True)
    print(response)
    if response[0]['sim'] >= 0.9:
        response = [x for x in response if x['sim'] >= 0.9]
    elif response[0]['sim'] >= 0.8:
        response = [x for i, x in enumerate(response) if i < 2 or x['sim'] >= 0.8]
    elif response[0]['sim'] >= 0.7:
        response = [x for i, x in enumerate(response) if i < 3 or x['sim'] >= 0.7]
    elif response[0]['sim'] >= 0.6:
        response = [x for i, x in enumerate(response) if i < 5 or x['sim'] >= 0.6]
    else:
        return '我找不到这个问题的答案，您是不是要问：\n' + '\n'.join([
            f"{i + 1}. {x['q']} ( {x['url']} ) "
            for i, x in enumerate(response[:3])
        ])
    if len(response) == 1:
        response[0]['text'] = response[0]['text'][3:]
    # print(response)
    return '\n'.join(map(lambda x: x['text'], response))


    # return_data_sturct = {}
    # return_data = {}
    # return_data_score = {}


    
    # time = 1
    # for i in response['hits']['hits']:
    #     print(i['_source'])
    #     # return {'ANS':i['_source']['Ans']}
    #     # return_data.update('Q_text':i['_source']['Q_text'])
    #     # return { 'answer':response}
    #     # {'Q_text':i['_source']['Q_text'],'Ans':i['_source']['Ans'],'Score':i['_score']}
    #     return_data_sturct[time] = {
    #         'Q': i['_source']['Q_text'], 'Score': i['_score'], 'Ans': i['_source']['Ans_url']}
    #     return_data[time] = i['_source']['Q_text'] + \
    #         "\n" + i['_source']['Ans_url'] + " "
    #     return_data_score[time] = i['_score']
    #     # print(i['_score'])
    #     if i['_score'] >= 1:
    #         time = time + 1
            
    # # print(return_data)

    # format_return_data = ""

    # for i in return_data:
    #     format_return_data = format_return_data + \
    #                 "%s. " % i + return_data[i] + "\n"
    # return format_return_data  # + "\n需要更多帮助请输 /help"
    # try:
    #     for i in return_data:
    #         if return_data_score[time-1] >= 0:
    #             format_return_data = format_return_data + \
    #                 "%s. " % i + return_data[i] + "\n"
    #     return format_return_data + "\n需要更多帮助请输 /help"
    # except:
    #     return "目前没有收录您的问题哦~"


if __name__ == '__main__':
    print(search_qa_format('申请流程'))
    while True:
        i = input('> ')
        print(search_qa_format(i))
