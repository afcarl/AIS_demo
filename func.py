# coding=utf8
# some functions are from http://blog.csdn.net/u010902721/article/details/23531359 (simon-zhao)
import math
import random
import numpy as np

def sum(fitvalue):
    total = 0
    for i in range(len(fitvalue)):
        total += fitvalue[i]
    return total

def cumsum(fitvalue):
    for i in range(len(fitvalue)):
        t = 0
        j = 0
        while (j <= i):
            t += fitvalue[j]
            j = j + 1
        fitvalue[i] = t

def selection(pop, fitvalue):  # 自然选择（轮盘赌算法）
    newfitvalue = []
    totalfit = sum(fitvalue)
    for i in range(len(fitvalue)):
        newfitvalue.append(fitvalue[i] / totalfit)
    cumsum(newfitvalue)
    ms = []
    poplen = len(pop)
    for i in range(poplen):
        ms.append(random.random())  # random float list ms
    ms.sort()
    fitin = 0
    newin = 0
    newpop = pop
    while newin < poplen:
        if (ms[newin] < newfitvalue[fitin]):
            newpop[newin] = pop[fitin]
            newin = newin + 1
        else:
            fitin = fitin + 1
    pop = newpop

def mutation(pop, pm):  # 基因突变
    px = len(pop)
    py = len(pop[0])
    for i in range(px):
        if (random.random() < pm):
            mpoint = random.randint(0, py - 1)
            if (pop[i][mpoint] == 1):
                pop[i][mpoint] = 0
            else:
                pop[i][mpoint] = 1

def crossover(pop, pc):  # 个体间交叉，实现基因交换
    poplen = len(pop)
    for i in range(poplen - 1):
        if (random.random() < pc):
            cpoint = random.randint(0, len(pop[0]))
            temp1 = []
            temp2 = []
            temp1.extend(pop[i][0: cpoint])
            temp1.extend(pop[i + 1][cpoint: len(pop[i])])
            temp2.extend(pop[i + 1][0: cpoint])
            temp2.extend(pop[i][cpoint: len(pop[i])])
            pop[i] = temp1
            pop[i + 1] = temp2

def decodechrom(pop):  # 将种群的二进制基因转化为十进制（0,1023）
    temp = []
    for i in range(len(pop)):
        t = 0
        for j in range(10):
            t += pop[i][j] * (math.pow(2, j))
        temp.append(t)
    return temp

def target_func(x):
    return 10 * np.sin(5 * x) + 7 * np.cos(4 * x)

def calobjvalue(pop):  # 计算目标函数值
    temp1 = []
    objvalue = []
    temp1 = decodechrom(pop)
    for i in range(len(temp1)):
        x = temp1[i] * 10 / 1023  # （0,1023）转化为 （0,10）
        objvalue.append(target_func(x))
    return objvalue  # 目标函数值objvalue[m] 与个体基因 pop[m] 对应

def calfitvalue(objvalue):  # 转化为适应值，目标函数值越大越好，负值淘汰。
    fitvalue = []
    temp = 0.0
    Cmin = 0
    for i in range(len(objvalue)):
        if (objvalue[i] + Cmin > 0):
            temp = Cmin + objvalue[i]
        else:
            temp = 0.0
        fitvalue.append(temp)
    return fitvalue

def best(pop, fitvalue):  # 找出适应函数值中最大值，和对应的个体
    px = len(pop)
    bestindividual = []
    bestfit = fitvalue[0]
    for i in range(1, px):
        if (fitvalue[i] > bestfit):
            bestfit = fitvalue[i]
            bestindividual = pop[i]
    return [bestindividual, bestfit]

def b2d(b):  # 将二进制转化为十进制 x∈[0,10]
    t = 0
    for j in range(len(b)):
        t += b[j] * (math.pow(2, j))
    t = t * 10 / 1023
    return t

# The following functions are written by myself (Snowkylin), used in AIS.py

def buildmemorycell(pop, fitvalue, mnum):
    p = [(pop[i], fitvalue[i]) for i in range(len(pop))]
    p.sort(key=lambda x:x[1], reverse=True)
    return p[0:mnum]

def caldensity(pop, h):
    popsize = len(pop)
    chromlength = len(pop[0])
    h01 = - 0.5 * np.log(0.5) * 2  # 同为0或同为1时该位信息熵为0
    q = [[0 for i in range(popsize)] for j in range(popsize)]
    for i in range(popsize):
        for j in range(i, popsize):
            h = 0
            for k in range(chromlength):
                if pop[i][k] != pop[j][k]:
                    h += h01
            q[i][j] = q[j][i] = 1 / (1 + h / chromlength)
    density = [0 for i in range(popsize)]
    for i in range(popsize):
        l = 0
        for j in range(popsize):
            if q[i][j] >= h:
                l += 1
        density[i] = l / popsize
    return density

def calsurvivep(fitvalue, density, hl):
    popsize = len(fitvalue)
    p = [0 for i in range(popsize)]
    sumf = sum(fitvalue)
    for i in range(popsize):
        if (density[i] >= hl):
            p[i] = fitvalue[i] * (1 - density[i]) / (density[i] * sumf)
        else:
            p[i] = fitvalue[i] / (density[i] * sumf)
    return p

def update(pop, memory):
    objvalue = calobjvalue(pop)                     # 计算目标函数值
    fitvalue = calfitvalue(objvalue)                # 计算个体的适应值
    p = [(pop[i], fitvalue[i], i) for i in range(len(pop))]
    p.sort(key=lambda x: x[0])
    for i in range(len(memory)):
        pop[p[i][2]] = memory[i][0]



