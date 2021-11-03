import csv 
import re
import numpy as np
#随机种子固定
np.random.seed(0)
import os
import random
random.seed(1)


#This function is used to compute the mutation score on a subset of kill matrix
#labelarray: kill matrix (labelarray[i][j]: the i-th test case can or cannot kill the j-th mutant)
#testlist : (index of )T to compute MS(T,M) e.g. [1,2]
#mutantlist: (index of )M to compute MS(T,M) len(mutantlist)>0, e.g. [1,2]
def computeMS(labelarray,testlist,mutantlist):
    newlabel=[]
    for t in testlist:
        tlabel=[]
        for m in mutantlist:
            tlabel.append(labelarray[t][m])
            #print(tlabel)
        newlabel.append(tlabel)
    killed=0
    for i in range(0,len(mutantlist)):
        x=0
        for j in range(0,len(testlist)):
            x=x+newlabel[j][i]
            if x==1:
                killed=killed+1
                break
    return float(killed)/len(mutantlist)





#This function is used to generate a sequence of test suites by continuous half-sample
def genSeq(labelarray):
    ans=[]
    testlist=[]
    #所有测试用例编号
    for i in range(0,len(labelarray)):
        testlist.append(i)
    numoftest=len(testlist)
    ans.append(testlist)
    while numoftest!=0:
        #每次把测试用例个数砍一半
        numoftest=int(numoftest/2)
        if numoftest==0:
            break
        rand=[]
        while len(rand)!=numoftest:
            num=random.randint(0,len(testlist)-1)
            if testlist[num] not in rand:
                rand.append(testlist[num])
        #更新当前测试用例集合
        testlist=rand
        ans.append(testlist)
    return ans



#This fuction is used to compute OP on one sequence.
#seq: the test suite suquence geneated by genSeq()
#mu: the selected mutantlist given by the strategy under evaluation. e.g. [1,2]
def OPonetime(seq,labelarray,mu):
    res=[]
    allms=[]
    newms=[]
    allmutantlist=[]
    for i in range(0,len(labelarray[0])):
        allmutantlist.append(i)
    for rand in seq:
        #向约简后变异得分list中添加当前测试用例集合对上约简变异体的变异得分
        newms.append(computeMS(labelarray,rand,mu))
        #向约简前变异得分list中添加当前测试用例集合对上全部变异体的变异得分
        allms.append(computeMS(labelarray,rand,allmutantlist))
    #a是得分集合的长度-1，即比较的order总个数
    a=len(newms)-1
    #right：前后order一致的个数
    right=0
    for i in range(0,a):
        #print(i)
        #相等的仍然相等，不等的仍然不等，则right+1
        if newms[i]-newms[i+1]==0 and allms[i]-allms[i+1]==0:
            right=right+1
        if newms[i]-newms[i+1]!=0 and allms[i]-allms[i+1]!=0:
            right=right+1
    OP=float(right)/a
    return OP




#This function is used to select mutants randomly
#mutantlist is used to decide the number  of selected mutants. (len(mutantlist)=number of selected mutants) e.g. if you want to select 5 mutants randomly, mutantlist=[0,1,2,3,4]
def RMS(labelarray,mutantlist):
    allmutantlist=[]
    randmutantlist=[]
    for i in range(0,len(labelarray[0])):
        allmutantlist.append(i)
    #直到选到和SMS同样多
    while len(mutantlist)!=len(randmutantlist):
        num=random.randint(0,len(allmutantlist)-1)
        if allmutantlist[num] not in randmutantlist:
            randmutantlist.append(allmutantlist[num])
    return randmutantlist



#This fuction is used to compute OP on one sequence for RMS.
def OPRMS(seq,labelarray,mutantlist):
    mu=RMS(labelarray,mutantlist)
    return OPonetime(seq,labelarray,mu)



#This function is used to compute EROP.
def EROP(OP,RMSOP,labelarray,mu):
    numofallmutant=len(labelarray[0])
    RR=float(len(mu))/numofallmutant
    return (OP-RMSOP)*RR
