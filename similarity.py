
import re
import jieba


def similarity(a, b):
    """
    @TODO 以后修改，先随便写一个相似度判断
    """
    a = jieba.lcut(a, cut_all=True)
    b = jieba.lcut(b, cut_all=True)
    a, b = set(a), set(b)
    sim = len(a & b) / len(a | b)
    sim = sim * 1.5
    if sim > 1.0:
        sim = 1.0
    return sim


if __name__ == '__main__':
    print(similarity('何使用群聊内消息置顶', '群聊内消息置顶'))
    print(similarity('何使用群聊内消息置顶', '群聊内消息'))
