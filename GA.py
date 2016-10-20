# coding=utf8
# from http://blog.csdn.net/u010902721/article/details/23531359 (simon-zhao)
import numpy as np
import matplotlib.pyplot as plt
from func import *

popsize = 50  # 种群的大小
# 用遗传算法求函数最大值：
# f(x)=10*sin(5x)+7*cos(4x) x∈[0,10]
chromlength = 10  # 基因片段的长度
pc = 0.6  # 两个个体交叉的概率
pm = 0.001  # 基因突变的概率
results = []
bestindividual = []
bestfit = 0
fitvalue = []
tempop = [[]]
pop = [[0, 1, 0, 1, 0, 1, 0, 1, 0, 1] for i in range(popsize)]
for i in range(100):                                # 繁殖100代
    objvalue = calobjvalue(pop)                     # 计算目标函数值
    fitvalue = calfitvalue(objvalue)                # 计算个体的适应值
    [bestindividual, bestfit] = best(pop, fitvalue) # 选出最好的个体和最好的函数值
    results.append([bestfit, b2d(bestindividual)])  # 每次繁殖，将最好的结果记录下来
    selection(pop, fitvalue)                        # 自然选择，淘汰掉一部分适应性低的个体
    crossover(pop, pc)                              # 交叉繁殖
    mutation(pop, pc)                               # 基因突变
#results.sort()
print results
for i in range(len(results)):
    print str(results[i][0]) + ' x=' + str(results[i][1]) + ' generation=' + str(i)
x = np.linspace(0, 10, 1000)
plt1 = plt.subplot(1, 2, 1)
plt1.plot(x, target_func(x), linewidth=2)
plt1.plot(results[-1][1], results[-1][0], 'ro')
plt2 = plt.subplot(1, 2, 2)
plt2.plot([i for i in range(len(results))], [results[i][0] for i in range(len(results))], linewidth=2)
plt.show()
