import random
from math import cos, sin, pi
class Solution(object):

    def FFT(self, a_real, a_image, flag):
        # a_real和a_image分别表示a的实数和虚数部分，flag为False表示做傅里叶变换，否则是傅里叶逆变换
        n = len(a_real)
        if n == 1: # 递归结束
            return a_real, a_image
        # wn 
        wn_real = cos(2*pi/n) 
        wn_image = sin(2*pi/n)

        if flag:# 判断是否做傅里叶逆变换
            wn_image = -wn_image
        # w
        w_real = 1.0
        w_image = 0.0
        # a_0
        a_0_real = [a_real[i] for i in range(0,n,2)]
        a_0_image = [a_image[i] for i in range(0,n,2)]
        # a_1
        a_1_real = [a_real[i] for i in range(1,n,2)]
        a_1_image = [a_image[i] for i in range(1,n,2)]

        # 求y_0和y_1
        y_0_real, y_0_image = self.FFT(a_0_real, a_0_image, flag)
        y_1_real, y_1_image = self.FFT(a_1_real, a_1_image, flag)
        
        # 最终输出
        y_real = [0 for _ in range(n)]
        y_image = [0 for _ in range(n)]

        for k in range(n//2):
            tag = k + n // 2  # k + n/2
            # w * y_1_k的实部和虚部
            wy1k_real = w_real * y_1_real[k] - w_image * y_1_image[k] 
            wy1k_image = w_real * y_1_image[k] + w_image * y_1_real[k]
            # y_k = y_0_k + w * y_1_k
            y_real[k] = y_0_real[k] + wy1k_real 
            y_image[k] = y_0_image[k] + wy1k_image
            # y_tag = y_0_k - w * y_1_k
            y_real[tag] = y_0_real[k] - wy1k_real 
            y_image[tag] = y_0_image[k] - wy1k_image
            # w = w * wn
            w_real_temp = w_real * wn_real - w_image * wn_image
            w_image_temp = w_real * wn_image + w_image * wn_real
            w_real = w_real_temp
            w_image = w_image_temp
        
        return y_real, y_image


    def multiply(self, num1, num2):
        n1, n2 = len(num1), len(num2) 
        
        # 计算长度为2的幂的长度
        total_len = 1 # 初始长度1
        max_len = max(n1, n2)
        while total_len < max_len:
            total_len *= 2
        total_len *= 2

        # a和b存放输入的数，c存放点值相乘得到的结果，ans存放最后的答案
        a_real = [0 for _ in range(total_len)] # a 实数部分
        b_real = [0 for _ in range(total_len)] # a 虚数部分
        a_image = [0 for _ in range(total_len)] # b 实数部分
        b_image = [0 for _ in range(total_len)] # b 虚数部分
        c_real = [0 for _ in range(total_len)] # c 实数部分
        c_image = [0 for _ in range(total_len)] # c 虚数部分
        ans = [0 for _ in range(total_len + 1)] # a 实数部分


        # 翻转系数，同时添加0使长度为2的幂
        for i in range(total_len):
            if i < n1:
                a_real[i] = int(num1[n1-i-1])
            if i < n2:
                b_real[i] = int(num2[n2-i-1])
            a_image[i] = b_image[i] = 0
        
        # 使用FFT将向量a和向量b转化为点值表示
        a_real, a_image = self.FFT(a_real, a_image, 0)
        b_real, b_image = self.FFT(b_real, b_image, 0)

        # 点值相乘得到向量c的点值表示
        for i in range(total_len):
            c_real[i] = a_real[i] * b_real[i] - a_image[i] * b_image[i]
            c_image[i] = a_real[i] * b_image[i] + a_image[i] * b_real[i]
        
        # 通过FFT逆变换将向量c由点值表示变成系数表示
        c_real, c_image = self.FFT(c_real, c_image, 1)
        for i in range(total_len):
            c_real[i] /= total_len
            c_image[i] /= total_len
        
        # 进位，使每位均为整数
        for i in range(total_len):
            ans[i] = int(c_real[i] + 0.5)
        for i in range(total_len):
            ans[i+1] += ans[i] // 10
            ans[i] %= 10
        
        # 获取最终答案
        len_ans = n1 + n2 - 1
        while ans[len_ans] == 0 and len_ans > 0:
            len_ans -= 1
        
        res = ''
        for i in range(len_ans,-1,-1):
            res += str(ans[i])
        
        return res

solution = Solution()

max_test = 5 # 最大测试个数
max_len = 100 # 最长整数长度
random.seed(1) # 设计随机种子

for i in range(max_test):
    a = random.randint(0,eval("1e"+str(max_len))) # 选取a，a在0-1e100
    b = random.randint(0,eval("1e"+str(max_len)))
    ans = str(a*b)
    res = solution.multiply(str(a),str(b)) # FFT方法计算大整数乘法
    print(f'test {i+1}:\na = {a}\nb = {b}')
    print(f'python结果: {ans}')
    print(f'FFT的结果 : {res}')
    print('正确！' if ans == res else '错误！')
    
