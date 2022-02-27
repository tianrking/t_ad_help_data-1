

from open_search import client, index_name
from encode import encode


def search_qa(query, size=5):
    _Q_vec = encode(query)

    query = {
        '_source': ['Q_text', 'Ans'],
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
                    }
                ]
            }
        }
    }

    response = client.search(
        body = query,
        index = index_name
    )
    return response


def search_qa_format(query):
    response = search_qa(query)
    return_data_sturct = {}
    return_data = {}
    
    time=1 
    for i in response['hits']['hits']:
        print(i['_source']['Q_text'],i['_source']['Ans'],i['_score'],i['_id'])
        # return {'ANS':i['_source']['Ans']}
        # return_data.update('Q_text':i['_source']['Q_text'])
        # return { 'answer':response}
        return_data_sturct[time] = {'Q':i['_source']['Q_text'],'Score':i['_score'],'Ans':i['_source']['Ans']}  # {'Q_text':i['_source']['Q_text'],'Ans':i['_source']['Ans'],'Score':i['_score']}
        return_data[time] = i['_source']['Q_text']+"\n"+ i['_source']['Ans']+ " "
        time = time + 1
    # print(return_data)
    format_return_data = ""
    for i in return_data:
        format_return_data = format_return_data  + "%s. "%i + return_data[i] + "\n"
    return format_return_data


if __name__ == '__main__':
    search_qa_format('广告')
