import gzip
import base64
import io
import json
import pandas as pd
import openpyxl
import requests

import shutil
import stat
from math import ceil
from os import path


# 这是在数据里找到所有充能罗盘的数据
def getCompassData(df):
    # df_com代表所有base_type为充能罗盘的行
    df_com = df[df['baseType'] == '充能罗盘']
    # df_com_4代表所有base_type为4次的行
    df_com_4 = df_com[df_com['name'].str.contains('使用剩余 4 次')]
    return df_com_4


# 这是找到觉醒六分仪-d价格数据的
def getDivToSextant(df):
    div = df[df['baseType'] == '神圣石']
    sextant = df[df['baseType'] == '觉醒六分仪']
    div_sextant = pd.DataFrame([{'name': sextant['name'].item(), '数量': 1, 'calculated': (sextant['calculated'].item()), "单位": "混沌石"}])
    return div_sextant


def load_Tencent_Server_Data(Tencent_Server_Url):
    try:
        Tencent_Server_Data = requests.get(Tencent_Server_Url, verify=False).text
        # TODO: 需要添加在日志窗口的网页响应码输出
        compressed_bytes = base64.b64decode(str(Tencent_Server_Data).encode("utf-8-sig"))
        with gzip.GzipFile(fileobj=io.BytesIO(compressed_bytes), mode='rb') as f:
            decompressed_bytes = f.read()
        decompressed_json = decompressed_bytes.decode('utf-8')
        decompressed_data = json.loads(decompressed_json)
        return decompressed_data
    except Exception as e:
        print(f"Error: {e}")
        raise e


# 得到罗盘与价格对应的字典
def get_price_compass_dir(compass_data):
    price_compass_dir = {}

    for index, row in compass_data.iterrows():
        pure_name = row['name'].replace('使用剩余 4 次', "").replace('充能罗盘', "")
        price_compass_dir[pure_name] = row['calculated']
    return price_compass_dir


# 返回数据并处理，最终返回出来的是罗盘名字与其价格的对应字典
def Tencent_compass_data(Tencent_Server_Url):

    price_json = load_Tencent_Server_Data(Tencent_Server_Url)  # 这是解码数据,price_josn里面就有数据了

    # 对json格式数据采用pandas处理
    df = pd.DataFrame(price_json)
    # 读取内部的所有罗盘数据
    compass_data = getCompassData(df)
    div_sex = getDivToSextant(df)

    return get_price_compass_dir(compass_data)
    # ################ debug item #################
    # try:
    #     df.to_excel('../all_data.xlsx', index=False)
    # except PermissionError as e:
    #     print(r"../all_data.xlsx 已经存在！")
    # ################ debug item #################
    # try:
    #     compass.to_excel('../compass_data.xlsx', index=False)
    # except PermissionError as e:
    #     print(r"../compass_data.xlsx 已经存在！")
    # ################ debug item #################


# Tencent_Server_Url = "https://gitee.com/hhzxxx/exilence-next-tx-release/raw/master/price2.txt"
# a = Tencent_compass_data(Tencent_Server_Url)
# list = []
# with open("../sextant_trans_1.txt", "r")as f:
#     for line in f.readlines():
#         list.append(line.replace("\n", ""))
#
# print(list)


def Tencent_compass_data_alias(price_compass_dir, compass_list_all):
    price_compass_dir_alias = {}
    for each_sextant in compass_list_all:
        for each_key, each_item in price_compass_dir.items():
            if each_sextant in each_key:
                price_compass_dir_alias[each_sextant] = each_item

    # for each_key, each_item in price_compass_dir_alias.items():
    #     print(f"{each_key} : {each_item}")
    return price_compass_dir_alias


compass_list_all = [
 '你的魔法地图额外包含4个魔法怪物群',
 '菌潮遭遇战',
 '该地图内的保险箱已被腐化',
 '区域内有一个走私者秘藏 ',
 '地图的品质加成也会影响掉落物品的稀有度',
 '不会受到反射伤害',
 '传奇怪物掉落腐化物品',
 '被悬赏的叛徒',
 '击败敌人将会吸引更强大的怪物登场',
 '该地图会额外出现 1 个战乱之殇事件',
 '每使用 1 个献祭碎片就能让该地图出现献祭之礼的几率增加 50%',
 '魔法怪物群大小提高 25%',
 '在你的地图中的驱灵祭坛处第1次重置恩典无消耗',
 '地图首领由 1 个神秘先驱者守护',
 '该地图会额外出现 1 个裂隙',
 '该地图会出现 2 位额外的【盗贼流放者】',
 '地图内有驱灵祭坛',
 '不朽辛迪加目标处获得的情报提高100%',
 '地图内的战乱之殇怪物掉落的印记和裂片会复制',
 '这些地图会额外出现 1 个精华',
 '该地图会出现 1 个额外深渊',
 '地图内裂隙属于夏乌拉',
 '你的未鉴定的地图中的怪物群规模提高20%',
 '该地图会出现【伊恩哈尔】',
 '该地图会出现【阿尔瓦】',
 '这些地图的腐化瓦尔怪物掉落的物品有 25% 的几率被腐化',
 '该地图会出现【尼克】',
 '你的地图的品质为20%',
 '地图内发现的地图被 8 个词缀腐化',
 '地图内的庄园至少有一片黄庄稼',
 '夺宝奇兵契约额外有一个基底词缀',
 '复制一头地图中被捕捉的魔物',
 '地图中有一个惊悸迷雾之镜',
 '额外掉落一个征服者地图',
 '至少有一片紫庄稼',
 '该地图会出现【琼】',
 '惊悸迷雾奖励条进度加快 100%',
 '你的地图中发现的圣油高一阶',
 '符纹怪物之印的数量提高 100%',
 '至少有一片蓝庄稼',
 '前 3 个被附身的怪物会掉落 1 个额外的锈蚀圣甲虫',
 '前 3 个被附身的怪物会掉落 1 个额外的抛光圣甲虫',
 '额外掉落一个塑界守卫地图',
 '前 3 个被附身的怪物会掉落 1 个额外的传奇物品',
 '前 3 个被附身的怪物会掉落 1 个额外的镀金圣甲虫',
 '玩家的瓦尔技能无法用于【阻灵术】',
 '物理属性怪物',
 '额外掉落一个裂界守卫地图',
 '该地图会出现 25 个额外神秘木桶堆',
 '击败后可转化的怪物',
 '地图首领由守卫守护完成该地图时会额外掉落 1 张地图',
 '玩家使用药剂回复的生命和魔力会立即回复',
 '这些地图吸引鱼',
 '冰霜属性怪物',
 '闪电属性怪物',
 '火焰属性怪物',
 '击败敌人时，玩家获得一个额外的瓦尔之灵',
 '你的地图包含古灵庄园',
 '地图内裂隙属于艾许',
 '前 3 个被附身的怪物会掉落 1 张额外地图',
 '地图内裂隙属于索伏',
 '混沌属性怪物',
 '隐忍神龛',
 '共鸣神龛',
 '腐化的异界地图中的地图首领额外掉落2个瓦尔物品',
 '地图内裂隙属于乌尔尼多',
 '地图首领额外掉落一件传奇物品',
 '地图内裂隙属于托沃',
 '地图内有致命贪婪遭遇战',
 '保险箱里的怪物已暴怒']