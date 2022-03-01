
from distutils.log import error
from fastapi import Request
import pandas as pd

from app import app
from search_qa import search_qa_format
from items import Item_jzmh
from jzmh import send_message

from contextvars import ContextVar
# 定义上下文变量
_flag = ContextVar('1') 

# var = ContextVar("var", default=123)

@app.get("/")
def return_hello(request: Request):
    client_host = request.client.host
    client_port = request.client.port

    try:
        return client_host
    except:
        return  "I can't get ur information via %s" % client_host 


@app.post("/v1/QA/search/jzmh/sentResult")
async def sent_result(request: Request):
    print(await request.json())

app.fff = 5

@app.post("/v1/QA/search/jzmh/message")
async def receive_message(item: Item_jzmh,request : Request):
    gg_data = item.data.payload.text
    try:
        try:
            gg_data.index('/help')
            print('help')
            _help = "1. 想返回更多的条目请输入 \n/more"+"\n"+"若检索到则会返回更多的条目 \n" + \
              "2. 想返回较少的讯息请输入 \n/less"+"\n"+"尽可能推送准确的结果给您 \n" + \
            "3. 如果需要电话咨询请输入 \n/callme"+"\n"+"我们将会第一时间联系您 \n" +\
            "4. 访问官网请输入 官网"
            app.fff = 5
            send_message(chatid=item.data.chatId, text=_help)
            return
            
        except:
            pass
        
        try:
            gg_data.index('/more')
            print('help')
           
            app.fff = 8
            send_message(chatid=item.data.chatId, text="好的 将为您返回更多查询结果")
            return
        
        except:
            pass
        
        try:
            gg_data.index('/reset')
            print('help')
           
            app.fff = 5
            send_message(chatid=item.data.chatId, text="好的 将为您返回更多查询结果")
            return
        
        except:
            pass
        
        try:
            gg_data.index('/less')
            print('help')
            app.fff = 2
            send_message(chatid=item.data.chatId, text="好的 将为您返回精确的查询结果")
            return
        
        except:
            pass
        
        try:
            gg_data.index('/callme')
            print('help')
            _phone = "请输入您的联系方式 "
            send_message(chatid=item.data.chatId, text="好的 已记录您的联系方式")
            return
        
        except:
            pass
        
        try:
            gg_data.index('官网')
            print('help')
            _offical_website = "微信广告帮助中心\nhttps://ad.weixin.qq.com/guide \n" +\
                "企业微信帮助中心\nhttps://open.work.weixin.qq.com/help2/pc?person_id=1 \n"+\
                "腾讯广告帮助中心\nhttps://e.qq.com/ads/helpcenter/"
            send_message(chatid=item.data.chatId, text=_offical_website)
            return
        
        except:
            
            item["I dont know i am item"]
            
    except:
        search_text = gg_data
        format_return_data = search_qa_format(search_text,app.fff)
        send_message(chatid=item.data.chatId, text=format_return_data)
        # try:
        #     search_text = gg_data
        #     format_return_data = search_qa_format(search_text)
        #     send_message(chatid=item.data.chatId, text=format_return_data)
        # except:
        #     send_message(chatid=item.data.chatId, text="在线查询人数过多 请稍后再试~~")
        #     return "在线查询人数过多 请稍等~~"



