import math
from datetime import datetime, timezone


def radical_score(stat, pubdate):
    """V3 Radical 激进版算法"""
    view = stat['view']
    like = stat['like']
    coin = stat['coin']
    favorite = stat['favorite']
    reply = stat['reply']
    danmaku = stat['danmaku']
    share = stat['share']
    
    # 基础热度
    h_base = math.log(view + 1)
    
    # 互动率
    interaction_rate = (like + coin * 2 + favorite * 1.5 + 
                       reply * 1.5 + danmaku * 0.5 + share) / view if view > 0 else 0
    
    # 互动增强因子
    i_booster = 1 + 3 * interaction_rate
    
    # 时间衰减
    days_since_pub = (datetime.now(timezone.utc) - pubdate).days
    d_decay = math.exp(-days_since_pub / 10)
    
    # 最终得分
    score = 10000 + (h_base * i_booster * d_decay * 500)
    return score


def normal_score(stat, pubdate):
    """V3 Normal 普通版算法"""
    view = stat['view']
    like = stat['like']
    coin = stat['coin']
    favorite = stat['favorite']
    reply = stat['reply']
    danmaku = stat['danmaku']
    share = stat['share']
    
    # 基础热度
    h_base = math.log(view + 1) * (1 + 0.3 * math.log(coin + 1))
    
    # 互动率
    interaction_rate = (like + coin * 2 + favorite * 1.5 + 
                       reply * 1.5 + danmaku * 0.5 + share) / view if view > 0 else 0
    
    # 互动增强因子
    i_booster = 1 + 1.5 * interaction_rate
    
    # 时间衰减
    days_since_pub = (datetime.now(timezone.utc) - pubdate).days
    d_decay = math.exp(-days_since_pub / 30)
    
    # 最终得分
    score = 10000 + (h_base * i_booster * d_decay * 800)
    return score


def e_sp_score(stat, pubdate):
    """V3 E SP 无时间衰减版算法 - 基于普通版去掉时间衰减"""
    view = stat['view']
    like = stat['like']
    coin = stat['coin']
    favorite = stat['favorite']
    reply = stat['reply']
    danmaku = stat['danmaku']
    share = stat['share']
    
    # 基础热度
    h_base = math.log(view + 1) * (1 + 0.3 * math.log(coin + 1))
    
    # 互动率
    interaction_rate = (like + coin * 2 + favorite * 1.5 + 
                       reply * 1.5 + danmaku * 0.5 + share) / view if view > 0 else 0
    
    # 互动增强因子
    i_booster = 1 + 1.5 * interaction_rate
    
    # 最终得分（去掉时间衰减）
    score = 10000 + (h_base * i_booster * 800)
    
    return score


def get_score_calculator(formula_name):
    """根据公式名称返回对应的计算函数"""
    formulas = {
        'radical': radical_score,
        'normal': normal_score,
        'e_sp': e_sp_score
    }
    return formulas.get(formula_name, normal_score)
