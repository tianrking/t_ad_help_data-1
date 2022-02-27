"""更新数据库"""

from tqdm import tqdm
from encode import encode
from open_search import client, index_name


def update(df):
    assert '问题分类' in df.columns
    assert '问题文本' in df.columns
    assert '答案文本' in df.columns
    assert '答案URL' in df.columns
    # Remove everything
    client.delete_by_query(index=index_name, body={
        'query': {
            'match_all': {}
        }
    })
    for _, row in tqdm(df.iterrows()):
        qtype = row['问题分类']
        question = row['问题文本']
        answer = row['答案文本']
        url = row['答案URL']

        answer_text = ''
        if answer and url:
            answer_text = f'{answer} {url}'
        elif answer:
            answer_text = answer
        elif url:
            answer_text = url

        _Q_vec = encode(question)

        document = {
            'Q_text': question,
            'Q_vec': _Q_vec,
            'Ans': url,
            'Q_type': qtype,
        }
        response = client.index(
            index=index_name,
            body=document,
            refresh=True
        )


if __name__ == '__main__':
    from feishu_sheet import fetch_table_by_range
    df = fetch_table_by_range(
        spreadsheetToken='shtcnmY1KOKGOAXRi11q0XEtkSb',
        start='A1',
        end='D1000',
        sheet='dc2aff',
    )
    update(df)
