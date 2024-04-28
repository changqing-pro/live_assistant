import pandas as pd
import json

# 定义函数，将'HistoryContents'列中的json数据转换为"Q: 问题 A: 回答"的格式
def convert_to_qa(data):
    # 在可能的情况下，输入可能是非字符串（例如NaN)，对它们进行处理
    if pd.isnull(data) or not isinstance(data, str):
        return data

    try:
        history_data = json.loads(data)
        qa_str = ""
        for item in history_data:
            if item["dialog"] == "asst":
                qa_str += "Q: " + item["content"] + "\n"
            else:
                qa_str += "A: " + item["content"] + "\n"
        return qa_str.replace('\r\n', '\n')
    except json.JSONDecodeError:
        # 如果数据不是JSON格式，则直接返回原数据
        return data

# 定义函数，其格式是前缀加原数据
def add_prefix(prefix, data):
    if pd.isnull(data) or not isinstance(data, str):
        return data
    return prefix + ": " + data.replace('\r\n', '\n')

# 使用pandas读取Excel文件
df = pd.read_excel('e://历史聊天记录.xlsx', engine='openpyxl')

# 针对'HistoryContents', 'UserQuestion', 'reply'这三列使用对应的处理方式
df['HistoryContents'] = df['HistoryContents'].apply(convert_to_qa)
df['UserQuestion'] = df['UserQuestion'].apply(lambda x: add_prefix("A", x))
df['reply'] = df['reply'].apply(lambda x: add_prefix("Q", x))

# 拼接'HistoryContents', 'UserQuestion', 'reply'这三列
df['combined'] = df['HistoryContents'] + '\n' + df['UserQuestion'] + '\n' + df['reply']

# 将拼接好的列'combined'写入到一个新的Excel文件中
df['combined'].to_excel('e://output.xlsx', index=False)