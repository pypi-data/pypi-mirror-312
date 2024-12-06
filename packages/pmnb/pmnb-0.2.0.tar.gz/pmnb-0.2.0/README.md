# 产品经理常用工具pmnb（pm牛逼） import pmnb as pm

## jsq （计算器首字母）方法：from pmnb import jsq
 * ipr：提升量计算：输入：jsq.ipr(之前的值，新的值)，输出：提升的绝对值，相对值  
 * ABSample：AB样本量计算  ABSample(),直接执行，根据提示输入就有结果
 * rank_wilson_score:威尔逊置信区间下界，jsq.rank_wilson_score(正样本数，总数)
 * confidence：置信度计算，直接执行，输出置信区间，置信度

## feed（内容相关） 方法：from pmnb import feed
 * xsd：相似度的首字母，计算标题相似度，输入文本1跟文本2，输出他们的相似度
 * count_words:统计excel某个sheet里某一列的词频

## analyse(分析相关) 方法：from pmnb import analyse
 * lr_one_hot()：根据lr模型输出各个特征以及重要程度,字符用one-hot编码
 * lr_factorize():根据lr模型输出各个特征以及重要程度,字符用序号编码
 * Tree_one_hot()：根据决策树模型输出各个特征以及重要程度,字符用one-hot编码
 * Tree_factorize():根据决策树模型输出各个特征以及重要程度,字符用序号编码
 * xgb_one_hot()：根据xgb模型输出各个特征以及重要程度,字符用one-hot编码
 * xgb_factorize():根据xgb模型输出各个特征以及重要程度,字符用序号编码


## growth（增长相关） 方法：from pmnb import growth
 * DAU:DAU预估，输入次日，7日，15日留存，日新增，天数，返回留存曲线跟第X天的DAU
