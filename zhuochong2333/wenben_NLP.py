from transformers import BertTokenizer, BertForSequenceClassification
import torch


def text_match(msg,data):
    """
    判断文本是否匹配指定类别的函数

    参数:
    msg (str): 待判断的文本

    返回:
    str: 匹配结果的文本描述
    """
    # 定义类别标签及对应的文本描述
    categories = {
        0: f"{data}",
        1: "关闭"
    }

    # 加载预训练的BERT模型和tokenizer
    model_name = "bert-base-chinese"
    tokenizer = BertTokenizer.from_pretrained(model_name)
    model = BertForSequenceClassification.from_pretrained(model_name)

    # 准备输入文本并进行tokenization
    inputs = tokenizer(msg, return_tensors="pt")

    # 使用模型进行推理
    outputs = model(**inputs)
    predictions = torch.argmax(outputs.logits, dim=1)

    # 返回预测结果对应的文本描述
    return predictions.item()


# 使用示例
msg = "打开教务系统"
data = '请打开教务系统'
result = text_match(msg, data)
print("匹配结果：", result)
