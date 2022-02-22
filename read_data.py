import pandas as pd

# df = pd.read_csv("/home/tianrking/t_ad_help_data/data/work_wx_ad_text_clean.csv",header=None, names=["0", "Q_text", "Ans"])
# df = df[[ "Q_text", "Ans"]]
# df.to_csv('/home/tianrking/t_ad_help_data/data/work_wx_ad_text_clean_fix.csv', mode='a', header=False)
# print(df.head(1))
df = pd.read_csv("/home/tianrking/t_ad_help_data/data/work_wx_ad_text_clean.csv",header=None, names=["0", "Q_text", "Ans"])
df = df[[ "Q_text", "Ans"]]
print(df.head(1))
