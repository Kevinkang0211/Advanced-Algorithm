# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 19:42:26 2020

@author: admin
"""
import sys
import numpy as np
import time

start_time = time.time()


#先設定initial的Lower bound
LB_old = sys.maxsize
visit_num =0
total_job = [1,2,3,4,5,6,7,8,9,10]
best_list =[]
bounded_list=[]

job_list = np.array([[1,2,3,4,5,6,7,8,9,10],           #job j
                     [0,5,12,15,20,29,39,53,60,66],           #rj
                     [8,10,5,20,7,6,18,15,3,10]])          #pj

#job_list = np.array([[1,2,3,4,5,6],           #job j
 #                    [0,2,2,6,7,9],           #rj
  #                   [6,2,3,2,5,2]])          #pj




def srpt(remain_item):
    
    length = len(remain_item)
    A = np.zeros((4,length))
    
    #建立工作抵達時間與執行時間對照表
    for i in range(len(remain_item)):
        for j in range(len(job_list[0])):
            
            if remain_item[i]==job_list[0,j]:
                A[0,i] = job_list[0,j] #job index
                A[1,i] = job_list[1,j] #arrive time
                A[2,i] = job_list[2,j] #process time  備註:最後一列紀錄release time
     
    r = np.array(A[1])
    p = np.array(A[2])
    
    
    
    h = np.ones(length,int)*999
    
    time = np.zeros(length,int)
    
    i = 0
    j = 0
    
    
    def add_heap(h, p, j):
        h[j] = p[j]
        heapify(h, p, r, time, 0)
    
    def check_arrived(i,r):
        for j in range(len(r)):
            if(i == r[j]):
                return True,j
            else:
                return False
    
    def swap(t1, t2):
        return t2, t1
    
    def heapify(h,p,r,time,i):
        left = 2*i+1
        right = 2*i+2
        if left<len(p):
            if(left <= len(h) and h[left] < h[i]):
                smallest = left
            else:
                smallest = i
            if(right < len(h) and h[right]<h[smallest]):
                smallest = right
            if smallest != i:
                h[i],h[smallest] = swap(h[i],h[smallest])
                p[i],p[smallest] = swap(p[i],p[smallest])
                r[i],r[smallest] = swap(r[i],r[smallest])
                time[i],time[smallest] = swap(time[i],time[smallest])
                heapify(h,p,r,time,smallest)
    
    def adjust():
        timer = int(len(h)/2.0)-1
        for i in range(timer,-1,-1):
            
            heapify(h, p, r, time, i)
        #timer = int(len(h)/2.0)-1
        #for i in range(timer,0,-1):
            #heapify(h, p, r, time, 0)
    
    
    #看所有的程序是否皆已完成
    def is_complete(p):    
        check = 0
        for i in range(len(p)):
            if(p[i] == 0):
                check = check+1
        if check == len(p):
            return False
        else:
            return True
    
    
    #看CPU是否空閒下來，目前到達的程序皆已經完成
    def not_free():
        check = 0        
        for j in range(len(r)):
            if(h[j]==999 or h[j]==1111):
                check = check+1
        if(check == len(r)):
            return False
        else:
            return True
    
    release_time =0
    
    while bool(is_complete(p)):
        adjust()
    
        if(h[0]==0):
            h[0] = 1111
            time[0] = i
            #heapify(h, p, r, time, 0)
            adjust()
        
        for j in range(len(r)):
            if(i == r[j]):
                add_heap(h,p,j)
            if(j<(length-1) and i==r[j+1]):
                add_heap(h,p,j+1)    
        
        
        if(not_free()):
            p[0] = p[0]-1
            h[0] = h[0]-1
            #time[0] = time[0]+1
    
    
    
        i = i+1
        release_time = i
    sum_time = 0
    for i in range(len(r)):
        sum_time = sum_time + time[i]
        
    return sum_time+release_time










#計算工作排序的總完成時間
def compute_sum_time(perm):
    length = len(perm)
    #檢查所有工作是否都完成了
    def is_complete(A):
        check = 0
        for i in range (len(A[2])):
            if A[2,i] == 0:
                check+=1
        if check == len(A[2]):
            return True
        else:
            return False
        
    
    t= 0
    current = 0
    #sum_time = 0
    
    A = np.zeros((4,length))
    
    #建立工作抵達時間與執行時間對照表
    for i in range(len(perm)):
        for j in range(len(job_list[0])):
            if perm[i]==job_list[0,j]:
                A[0,i] = job_list[0,j]
                A[1,i] = job_list[1,j]
                A[2,i] = job_list[2,j]
                
    #開始進行程序執行
    while(not is_complete(A)):
        
        if(t >= A[1,current]):
            A[2,current]-=1
            
        if(A[2,current]==0):
            A[3,current] = t+1
            current+=1
        t+=1
        
    
    #print(A)
    #sum_time = A[2].sum()
    
     
    return_list = [A[3].sum(),A[3][len(perm)-1]]
    return return_list


#==========================DFS with B&B===========================

def dfs_permutation(all_seq, seq_walked):
    global LB_old,best_list,bounded_list,total_job,visit_num
    
    #check ==0 代表第一次到下一層level
    check = 0
    #LB_old=9999
    for i in all_seq:
        
        if check !=0:
            seq_walked = seq_walked[0:len(seq_walked)-1]
            
        seq_walked = seq_walked + [i] #紀錄已走過節點
        
        check +=1
       
        remain_seq =  [x for x in [1,2,3,4,5,6] if x not in seq_walked ]
        
        
        LB = compute_sum_time(seq_walked)[0] + srpt(remain_seq)
        visit_num +=1
        #cmax = compute_sum_time(seq_walked)
        
        #print(LB_old)
        #print(cmax)
        #print(LB)
    
        #if LB>LB_old:
         #   if len(seq_walked)!=len(total_job):
          #      bounded_list += [seq_walked,LB_old,LB]
        if LB<=LB_old:
            dfs_permutation(remain_seq, seq_walked)
            
           
                
        if len(seq_walked)==6: #已抵達leafnode
            if LB<LB_old:
                LB_old = LB
                best_list = seq_walked
                #print(LB)
    #print(bounded_list)
 

#執行主程式
dfs_permutation(total_job[:6],[])

print('Best permutation is:' , best_list,'\n')
print('Sum of completion time:', LB_old,'\n')
end_time = time.time()
print('DFS without Branch and Bound takes: ' , round(end_time-start_time,4), 'seconds','\n')
#print('Permutation bounded(前十個) :' , bounded_list[:30])
#print(compute_sum_time([1,2,3,5]))
#print(srpt([4,6,7,8,9,10]))
print('visit number:' , visit_num)
        
        
        
print(compute_sum_time([1,2,3,5,6,4]))
        
        
        
        
        
        
        
        
        
        
        
        
