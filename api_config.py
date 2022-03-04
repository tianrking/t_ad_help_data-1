
import math
from fastapi import Request
from app import app
from open_search import client, config_index_name


def get_settings(token):
    try:
        if isinstance(token, str):
            doc = client.get(index=config_index_name, id=token)
            return doc['_source']
    except:  # may 404
        pass
    return {
        "token": token,
        "threshold_90": 1,
        "threshold_80": 2,
        "threshold_70": 3,
        "threshold_60": 5,
        "threshold_50": -1,
        "lexical_title": 1.0,
        "lexical_answer": 0.1,
        "semantic_title": 1.0,
    }


def put_settings(body):
    client.index(index=config_index_name, id=body['token'], body=body, refresh=True)


@app.get("/api/config/{token}")
async def get_api_config(token: str= None):
    """
    curl localhost:1333/api/config/123
    """
    if not isinstance(token, str) or len(token.strip()) <= 0:
        return {
            "ok": False,
            "error": "Invalid token"
        }
    return {
        "ok": True,
        "data": get_settings(token),
    }


@app.post("/api/config")
async def post_api_config(request: Request):
    """
    curl -XPOST localhost:1333/api/config -H "Content-Type: application/json" \
        -d "{
            "token": 'iamtoken',
            "threshold_90": 1,
            "threshold_80": 2,
            "threshold_70": 3,
            "threshold_60": 5,
            "threshold_50": -1,
            "lexical_title": 0.0,
            "lexical_answer": 0.0,
            "semantic_title": 0.0,
        }"
    """
    body = await request.json()
    if not isinstance(body, dict) or "token" not in body or not isinstance(body["token"], str):
        return {
            "ok": False,
            "error": "invalid request"
        }
    current_settings = get_settings(body["token"])
    for k, v in current_settings.items():
        if k not in body:
            return {
                "ok": False,
                "error": f"need key {k}"
            }
        if k == 'token' and not isinstance(v, str):
            return { 'ok': False, 'error': 'invalid token' }
        elif k != 'token' and (not isinstance(body[k], (int, float)) or not math.isfinite(body[k])):
            return { 'ok': False, 'error': f'invalid value of {k}: {v}' }
        current_settings[k] = body[k]
    put_settings(current_settings)
    return {
        "ok": True,
        "error": "updated"
    }
