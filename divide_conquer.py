import random
class Solution(object):
    # 在数字zero_num前添加zero_num个前置0
    def addZero(self, num, zero_num):
        return '0' * zero_num + num

    # 去除前缀0
    def removeZero(self,num):
        # 如果长度为1直接返回，可能是单独的0
        if len(num) == 1:
            return num
        k = 0 # 记住前缀0的个数
        i = 0
        n = len(num)
        
        while i < n:
            if num[i] != '0':
                break
            k += 1
            i += 1
        # print(k)
        if k == n: # 如果全0返回0
            return '0'
        else:
            return num[k:]

    # 大整数加法
    def add(self, num1, num2):
        sign = ''
         # 处理负号，如果有负号去除负号；如果数字为正，sign为空，否则为-
        flag_num1 = False
        flag_num2 = False
        if num1[0] == '-':
            flag_num1 = True
            num1 = num1[1:]
        if num2[0] == '-':
            flag_num2 = True
            num2 = num2[1:]
        if flag_num1 and flag_num2:
            sign = '-'
        elif not flag_num1 and not flag_num2:
            sign = ''
        elif flag_num1 and not flag_num2:
            return self.subtract(num2, num1)
        else:
            return self.subtract(num1, num2)

        res = '' # 结果

        # 去除前缀0
        num1 = self.removeZero(num1)
        num2 = self.removeZero(num2)

        # 翻转方便相加
        num1 = num1[::-1]
        num2 = num2[::-1]
        # 获取长度
        n1 = len(num1)
        n2 = len(num2)
        c = 0 # 进位
        # 按位相加
        for i in range(max(n1, n2)):
            temp = c
            if i < n1:
                temp += int(num1[i])
            if i < n2:
                temp += int(num2[i]) 
            c = temp // 10
            temp = temp % 10
            res = str(temp) + res

        if c == 1: # 是否最后一位进位
            res = '1' + res
        res = sign + res
        return res

    # 大整数相减
    def subtract(self, num1, num2):
        res = '' # 结果

        # 去除前缀0
        num1 = self.removeZero(num1)
        num2 = self.removeZero(num2)
        # 获取长度
        n1 = len(num1)
        n2 = len(num2)
        tempres = [0 for _ in range(max(n1, n2))] # 临时存储答案
        sign = '' # 判断正负号,空表示正，'-'表示负
        if n1 > n2:
            sign = ''
        elif n1 < n2:
            sign = '-'
        else: # 比较num1与num2大小
            flag = True # 判断是否num1=num2
            for i in range(n1):
                if num1[i] == num2[i]:
                    continue
                if num1[i] > num2[i]:
                    sign = ''
                    flag = False
                    break
                elif num1[i] < num2[i]:
                    sign = '-'
                    flag = False
                    break
            if flag: # 相等直接返回0
                return '0'
        
        # 翻转方便相减
        num1 = num1[::-1]
        num2 = num2[::-1]

        # 若num1大直接相减，否则num2-num1
        for i in range(len(tempres)):
            num1_i = num1[i] if i < n1 else 0
            num2_i = num2[i] if i < n2 else 0
            if sign == '':
                tempres[i] = int(num1_i) - int(num2_i)
            else:
                tempres[i] = int(num2_i) - int(num1_i)
        
        # 计算借位
        for i in range(len(tempres)-1):
            if tempres[i] < 0:
                tempres[i+1] -= 1
                tempres[i] += 10
        
        end = len(tempres) - 1
        for i in range(len(tempres)-1,-1,-1):
            if tempres[i] != 0:
                break
            end -= 1

        res = sign
        for i in range(end,-1,-1):
            res += str(tempres[i])
        
        return res


    # 尾部添加0
    def addZeroLast(self, num, zero_num):
        num += '0' * zero_num
        return num
            

    # 乘法
    def multiply(self, num1, num2):
        # # 如果有0直接返回0
        # if num1 == '0' or num2 == '0':
        #     return '0'
        sign = ''
         # 处理负号，如果有负号去除负号；如果数字为正，sign为空，否则为-
        flag_num1 = False
        flag_num2 = False
        if num1[0] == '-':
            flag_num1 = True
            num1 = num1[1:]
        if num2[0] == '-':
            flag_num2 = True
            num2 = num2[1:]
        if (flag_num1 and flag_num2) or (not flag_num1 and not flag_num2):
            sign = ''
        else:
            sign = '-'
        
        # 进行预处理，通过添加前置0将num1和num2都处理成相同位数，且均为2的指数
        init_len = 4 # 长度初始化为4
        if len(num1) > 2 or len(num2) > 2: # 如果长度大于2，那么最小长度至少为4
            if len(num1) > len(num2):
                while init_len < len(num1): # 计算所需长度
                    init_len *= 2 
            else:
                while init_len < len(num2): # 计算所需长度
                    init_len *= 2
            # 添加前置0
            num1 = self.addZero(num1, init_len - len(num1))
            num2 = self.addZero(num2, init_len - len(num2))    
        
        # 单独处理长度小于等于2的情况，使形式统一
        if len(num1) == 1:
            num1 = self.addZero(num1, 1)
        if len(num2) == 1:
            num2 = self.addZero(num2, 1)
        
        # 获取数字长度
        n = len(num1)

        # 对大整数进行划分，前面已经对n为1的情况进行处理
        a0, a1 = num1[0:n//2], num1[n//2:]
        b0, b1 = num2[0:n//2], num2[n//2:]

        if n == 2: # 长度为2时递归结束
            a0, a1, b0, b1 = map(int, (a0,a1,b0,b1))
            z = (a0 * 10 + a1) * (b0 * 10 + b1)
            res = str(z)
        else:
            c2 = self.multiply(a1, b1) # c2 = a1 * b1
            c0 = self.multiply(a0, b0) # c0 = a0 * b0
            temp_c1_1 = self.subtract(a0, a1) # a0 - a1
            temp_c1_2 = self.subtract(b1, b0) # b1 - b0
            c1 = self.multiply(temp_c1_1, temp_c1_2) # (a0 - a1) * (b1 - b0)
            c1 = self.add(c1, c0)
            c1 = self.add(c1, c2) # (a0 - a1) * (b1 - b0) + c0 + c2
            s0 = self.addZeroLast(c0, n) # c0 * 10 ^ n
            s1 = self.addZeroLast(c1, n // 2) # c1 * 10 ^ n//2
            res = self.add(self.add(s0, s1), c2) 
        
        res = self.removeZero(res)
        res = sign + res
        return res

    
solution = Solution()

max_test = 5 # 最大测试个数
max_len = 100 # 最长整数长度
random.seed(0) # 设计随机种子

for i in range(max_test):
    a = random.randint(0,eval("1e"+str(max_len))) # 选取a，a在0-1e100
    b = random.randint(0,eval("1e"+str(max_len)))
    ans = str(a*b)
    res = solution.multiply(str(a),str(b)) # FFT方法计算大整数乘法
    print(f'test {i+1}:\na = {a}\nb = {b}')
    print(f'python结果: {ans}')
    print(f'FFT的结果 : {res}')
    print('正确！' if ans == res else '错误！')