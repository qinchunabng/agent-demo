import numpy as np
"""
计算两个向量的余弦相似度（衡量方向相似性，剔除长度影响）

参数：
    vec_a(np.array):向量A
    vec_b(np.array):向量B
返回:
    float: 余弦相似度度结果（范围[-1,1]，越接近1方向越一致）
公式：
    cos_sim = (vec_a • vec_b ) / (||vec_a|| x ||vec_b||)
"""

def get_dot(vec_a, vec_b):
    """
    计算2个向量的点积，2个向量同维度数字成积之和
    """
    if len(vec_a) != len(vec_b):
        raise ValueError('两个向量必须维度相同')

    dom_sum = 0
    for a, b in zip(vec_a, vec_b):
        dom_sum += a * b

    return dom_sum

def get_norm(vec):
    """
    计算单个向量的模长，对向量的每个数字求平方再求和开根号
    """
    sum_square = 0
    for v in vec:
        sum_square += v * v

    return np.sqrt(sum_square)

def cosine_similarity(vec_a, vec_b):
    """
    余弦相似度：2个向量的点积除以2个向量模长的乘积
    :param vec_a:
    :param vec_b:
    :return:
    """
    result = get_dot(vec_a, vec_b) / (get_norm(vec_a) * get_norm(vec_b))
    return result

if __name__ == '__main__':
    vec_a = [0.5, 0.5]
    vec_b = [0.7, 0.7]
    vec_c = [0.7, 0.5]
    vec_d = [0.5, 0.5]
    print('ab:', cosine_similarity(vec_a, vec_b))
    print('ac:', cosine_similarity(vec_a, vec_c))
    print('ad:', cosine_similarity(vec_a, vec_d))
