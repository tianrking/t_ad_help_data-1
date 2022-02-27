import os
import requests
import pandas as pd


app_id = os.environ.get('app_id', "cli_a29da89ab7b99013")
app_secret = os.environ.get('app_secret', "MYqvkrh3x64kvcifOaOFsRxS1suJnygW")
tenant_access_token = None


def get_tenant_access_token(app_id, app_secret):
    ret = requests.post(
        'https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal',
        json={
            "app_id": app_id,
            "app_secret": app_secret
        },
        timeout=30
    )
    tenant_access_token = ret.json()['tenant_access_token']
    return tenant_access_token


tenant_access_token = get_tenant_access_token(app_id, app_secret)


def fetch_table_by_range(
    spreadsheetToken='shtcnmY1KOKGOAXRi11q0XEtkSb',
    start='A1',
    end='D1000',
    sheet='dc2aff',
):
    """
    Args:
        value_range: dc2aff是sheetid，A1到D100
    """
    value_range = f'{sheet}!{start}:{end}'
        
    ret2 = requests.get(
        f'https://open.feishu.cn/open-apis/sheets/v2/spreadsheets/{spreadsheetToken}/values/{value_range}',
        headers={
            'Authorization': f'Bearer {tenant_access_token}',
            'Content-Type': 'application/json; charset=utf-8',
        },
        timeout=30
    )
    data = ret2.json()['data']['valueRange']['values']
    headers = data[0]
    body = list(filter(lambda row: any(row), data[1:]))
    for i, row in enumerate(body):
        for j, col in enumerate(row):
            if col is None:
                row[j] = ''
            elif isinstance(col, list) and len(col) > 0 and isinstance(col[0], dict) and 'text' in col[0]:
                row[j] = col[0]['text']
        body[i] = row
    df = pd.DataFrame(body, columns=headers)
    return df


if __name__ == '__main__':
    df = fetch_table_by_range(
        spreadsheetToken='shtcnmY1KOKGOAXRi11q0XEtkSb',
        start='A1',
        end='D1000',
        sheet='dc2aff',
    )
    print(df)
