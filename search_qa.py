

from open_search import client, index_name
from encode import encode


def search_qa(query, size=5):
    _Q_vec = encode(query)

    query = {
        '_source': ['Q_text', 'Ans_url', 'Q_vec', "Ans_text"],
        'size': size,
        'query': {
            "bool": {
                "should": [
                    {
                        "knn": {
                            "Q_vec": {
                                "vector": _Q_vec,
                                "k": 2
                            }
                        }
                    },
                    {
                        "match_phrase": {
                            "Q_text": query
                        }
                    },
                    {
                        "match_phrase": {
                            "Ans_text": query
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


def search_qa_format(query,size=5):
    response = search_qa(query,size)
    return_data_sturct = {}
    return_data = {}
    return_data_score = {}
    
    time = 1
    for i in response['hits']['hits']:
        print(i['_source']['Q_text'], i['_source']
              ['Ans_url'], i['_score'], i['_id'])
        # return {'ANS':i['_source']['Ans']}
        # return_data.update('Q_text':i['_source']['Q_text'])
        # return { 'answer':response}
        # {'Q_text':i['_source']['Q_text'],'Ans':i['_source']['Ans'],'Score':i['_score']}
        return_data_sturct[time] = {
            'Q': i['_source']['Q_text'], 'Score': i['_score'], 'Ans': i['_source']['Ans_url']}
        return_data[time] = i['_source']['Q_text'] + \
            "\n" + i['_source']['Ans_url'] + " "
        return_data_score[time] = i['_score']
        # print(i['_score'])
        if i['_score'] >= 1:
            time = time + 1
            
    # print(return_data)

    format_return_data = ""

    for i in return_data:
        format_return_data = format_return_data + \
                    "%s. " % i + return_data[i] + "\n"
    return format_return_data + "\n需要更多帮助请输 /help"
    # try:
    #     for i in return_data:
    #         if return_data_score[time-1] >= 0:
    #             format_return_data = format_return_data + \
    #                 "%s. " % i + return_data[i] + "\n"
    #     return format_return_data + "\n需要更多帮助请输 /help"
    # except:
    #     return "目前没有收录您的问题哦~"


if __name__ == '__main__':
    search_qa_format('广告')
