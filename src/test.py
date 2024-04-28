import pandas as pd

# 读取Excel文件
a_df = pd.read_excel('e:\\终(1).xlsx')
b_df = pd.read_excel('e:\\OD4月锁定过的数据.xlsx')

# 将 create_time 转换为日期格式
b_df['create_time'] = pd.to_datetime(b_df['create_time']).dt.date

# 在B表格中，对 'create_time' 和 'mobile1' 做 groupby 操作并计算数量
b_count = b_df.groupby(['create_time', 'mobile1']).size().reset_index(name='counts')


# A表格中的 '数据所属日期' 转换为日期格式
a_df['数据所属日期'] = pd.to_datetime(a_df['数据所属日期']).dt.date

# 合并A表格和B_count
merged_df = pd.merge(a_df, b_count,  how='left', left_on=['数据所属日期', '手机号'], right_on = ['create_time', 'mobile1'])

# 将counts为空的替换为0
merged_df['counts'] = merged_df['counts'].fillna(0).astype(int)

merged_df.to_excel('e:\\终(1).xlsx', index=False)
