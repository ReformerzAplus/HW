import pandas as pd
import xml.etree.ElementTree as et
from functools import reduce

df_cols = ["買賣","鄉鎮市區","交易標的","土地區段位置建物區段門牌","土地移轉總面積平方公尺","都市土地使用分區","非都市土地使用分區","非都市土地使 用編定","交易年月日","交易筆棟數","移>轉層次","總樓層數","建物型態","主要用途","主要建材","建築完成年月","建物移轉總面積平方公尺","建物現況格局-房","建物現況格局-廳","建物現況格局-衛","建物現況格局-隔間","有無管理組織","總價元","單價元平方公尺","車位類別","車位移轉總面積平方公尺","車位總價元","備註","編號","主建物面積","附屬建物面積","陽台面積","電梯","移轉編號"]

CN_NUM = {'一層' : 1, '二層' : 2, '三層' : 3, '四層' : 4, '五層' : 5, '六層' : 6, '七層' : 7, '八層' : 8, '九層' : 9, '十層' : 10, '十一層' : 11, '十二層' : 12, '十三層' : 13, '十四層' : 14, '十五層' : 15, '十六層' : 16, '十七層' : 17, '十八層' : 18, '十九層' : 19, '二十層' : 20, '二十一層' : 21, '二十二層' : 22, '二十三層' : 23, '二十四層' : 24, '二十五層' : 25, '二十六層' : 26, '二十七層' : 27, '二十八層' : 28, '二十九層' : 29, '三十層' : 30, '三十一層' : 31, '三十二層' : 32, '三十三層' : 33, '三十四層' : 34, '三十五層' : 35, '三十六層' : 36, '三十七層' : 37, '三十八層' : 38, '三十九層' : 39, '四十層' : 40, '四十一層' : 41, '四十二層' : 42, '四十三層' : 43, '六十八層' : 68 ,'八十五層' : 85}

def parse_XML(xml_file, df_cols):
    xtree = et.parse(xml_file)
    xroot = xtree.getroot()
    rows = []

    for node in xroot:
        res = []
        res.append(node.attrib.get(df_cols[0]))
        for el in df_cols[1:]:
            if node is not None and node.find(el) is not None:
                res.append(node.find(el).text)
            else:
                res.append(None)
        rows.append({df_cols[i]: res[i]
                     for i, _ in enumerate(df_cols)})

    out_df = pd.DataFrame(rows, columns=df_cols)

    return out_df



df_a = parse_XML('/Users/ReformerzAplus/project_2/hw_1/a_lvr_land_a.xml',df_cols)
df_b = parse_XML('/Users/ReformerzAplus/project_2/hw_1/b_lvr_land_a.xml',df_cols)
df_e = parse_XML('/Users/ReformerzAplus/project_2/hw_1/e_lvr_land_a.xml',df_cols)
df_f = parse_XML('/Users/ReformerzAplus/project_2/hw_1/f_lvr_land_a.xml',df_cols)
df_h = parse_XML('/Users/ReformerzAplus/project_2/hw_1/h_lvr_land_a.xml',df_cols)
df_all = pd.concat([df_a, df_b, df_e, df_f, df_h])



filter_a_1 = df_all["主要用途"] == "住家用"
filter_a_2 = df_all["建物型態"].str.startswith('住宅大樓')
filter_a_3 = df_all["總樓層數"].map(CN_NUM).fillna(0).astype(int)
filter_a_3 = filter_a_3.where(filter_a_3 >= 13)

result = df_all[(filter_a_1 & filter_a_2 & filter_a_3)]

total_data_count = len(result.index)
print("總件數: ",total_data_count)

total_post_car = result["交易筆棟數"].apply(lambda x:x[-1]).astype(int).sum()
print("總車位數: ",total_post_car)

avg_value = ((result["總價元"].astype(int).sum())/total_data_count)
print("平均總價元: ",avg_value)

avg_post_car_value = ((result["車位總價元"].astype(int).sum())/total_post_car)
print("平均車位總價元: ", avg_post_car_value)


filter_b_df = { '總件數': [total_data_count] , '總車位數': [total_post_car] , '平均總價元': [avg_value] , '平均車位總價元': [avg_post_car_value] }
filter_b = pd.DataFrame(filter_b_df)

result.to_csv(r'/Users/ReformerzAplus/project_2/filter_a.csv', encoding='utf_8_sig', index = False, header=True)
filter_b.to_csv(r'/Users/ReformerzAplus/project_2/filter_b.csv', encoding='utf_8_sig', index = False, header=True)
