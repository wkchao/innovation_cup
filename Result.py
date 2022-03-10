import re
import codecs
from collections import Counter


def cluster(cls):
    source1 = open("calcu_res/text.txt", 'r')
    source2 = open("calcu_res/cluster_result.txt", 'r')
    result1 = codecs.open("calcu_res/final_cluster_result.txt", 'w', 'utf-8')

    #########################################################################
    #                        第一部分 合并实体名称和类簇

    lable = []  # 存储类标 类
    content = []  # 存储实体名称
    name = source1.readline()

    while name != "":
        res = source2.readline()
        res = res.strip('\r\n')

        value = res.split(' ')
        #print(value)
        no = int(value[0]) - 1  # 行号
        va = int(value[1])  # 值
        lable.append(va)
        content.append(name)

        #print(name, res)
        result1.write(name + ' ' + res + '\r\n')
        name = source1.readline()
    else:
        #print('OK')
        source1.close()
        source2.close()
        result1.close()
    """
    # 测试输出 其中实体名称和类标一一对应
    i = 0
    while i < len(lable):
        print(content[i], (i + 1), lable[i])
        i = i + 1
    """
    #########################################################################
    #                      第二部分 合并类簇 类1 ..... 类2 .....

    # 定义定长字符串数组 对应类簇
    output = [''] * cls
    result2 = codecs.open("calcu_res/final_cluster_merge.txt", 'w', 'utf-8')

    # 统计类标对应的实体名称
    i = 0
    while i < len(lable):
        output[lable[i]] += content[i] + ' '
        i = i + 1

    # 输出
    i = 0
    while i < cls:
        # word_list = re.split(' |\n', output[i])
        word_list = output[i].split(' ')
        top = Counter(word_list)
        del top['\n']
        print(top.most_common(5))
        # print('#######')
        result2.write('#######\r\n')
        # print('Label: ' + str(i))
        result2.write('Label: ' + str(i) + '\r\n')
        # print(output[i])
        result2.write(output[i] + '\r\n')
        i = i + 1

    result2.close()


if __name__ == '__main__':
    cluster(3)
