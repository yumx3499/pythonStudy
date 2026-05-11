### 余弦相似度

import numpy as np
#计算两个向量的点积
def get_dot_product(vec1, vec2):
    if len(vec1) != len(vec2):
        raise ValueError("两个向量的维度必须相同")
    dot_sum = 0
    for a,b in zip(vec1, vec2):
        dot_sum += a * b
    return dot_sum

#计算两个向量的模长
def get_mod(vec):
    mod_sum = 0
    for a in vec:
        mod_sum += a**2
    return np.sqrt(mod_sum)

#计算余弦相似度
def get_cosine_similatity(vec1,vec2):
    result = get_dot_product(vec1,vec2)/(get_mod(vec1)*get_mod(vec2))
    print(result)

if __name__ == "__main__":
    vec1 = [2,3,4,9,5]
    vec2 = [1,2,3,-1,6]
    vec3 = [1,2,3,4,5]
    get_cosine_similatity(vec1,vec2) 
    get_cosine_similatity(vec1,vec3) 