# -*- coding: utf-8 -*-
"""
Created on Mon Dec 14 21:57:39 2020

@author: kevin
"""

#test = [[62.0, [6]], [58.0, [5]], [56.0, [3]], [61.0, [4]], [59.0, [2]]]

#temp_list = [1,2,3]
#test += [[100,temp_list]]

#test = [1,2,3]

#test +=[4,5,6]


#print(test)

#remain =[2,3,4,5,6]

#for i in remain:
 #   print(i)
    
    
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 14 18:14:51 2020

@author: kevin
"""
import numpy as np 
import sys
#job_list = [1,2,3,4]

queue = []
best_perm = []
LB_old = sys.maxsize

job_list = np.array([[1,2,3,4,5,6],           #job j
                     [0,2,2,6,7,9],           #rj
                     [6,2,3,2,5,2]])          #pj



def compute_sum_time(perm):
    
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
    
    A = np.zeros((4,6))
    
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
    return A[3].sum()

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
        
    #rint(release_time)
    #print(sum_time+release_time)
    return sum_time+release_time


#================BFS with B&B ===========================
def bfs(job_list):
    global queue,LB_old
    
    
    def heapify(h,i):
        left = 2*i+1
        right = 2*i+2
        if left<len(h):
            if(left <= len(h) and h[left] < h[i]):
                smallest = left
            else:
                smallest = i
            if(right < len(h) and h[right]<h[smallest]):
                smallest = right
            if smallest != i:
                #swap h[i],h[smallest]
                h[i],h[smallest] = h[smallest],h[i]
                
                heapify(h,smallest)
    
    def check_leaf(queue):
        global LB_old,best_perm
        check = 0
        for i in range(len(queue)):
            #如果Queue中有一個sublist已經有6個排好 那就是答案
            if len(queue[i][1])==6:
                check+=1
                #LB_old = queue[i][0]
                #best_perm = queue[i][1]
                #queue = pop(queue)

        if check==1:
            return True
            
    def adjust():
        timer = int(len(queue)/2.0)-1
        for i in range(timer,-1,-1):
            heapify(queue,i)
            
    def pop(queue):
        candidate = queue[0]
        
        queue[0] = queue[len(queue)-1]
        queue = queue[0:len(queue)-1]
        
        return candidate,queue
   
    def divide():
        global queue
        #pop up heap中LB最小的
        candidate,queue = pop(queue)
        
        remain_list = [x for x in [1,2,3,4,5,6] if x not in candidate[1]]
        
        for i in remain_list:
            
            temp_list = candidate[1]+[i]
            LB = compute_sum_time(temp_list)+srpt([x for x in [1,2,3,4,5,6] if x not in temp_list])
            queue +=[[LB,temp_list]]
             
        adjust()
        
            
    
    #==========initial===========
    for i in job_list:
        remain_list = [x for x in [1,2,3,4,5,6] if x != i ]
        
        LB = compute_sum_time([i])+srpt(remain_list)
        queue +=[[LB,[i]]]
    
    adjust()
    #============================
    #print(queue)
    
    
    #要先找到第一個解
    while(not check_leaf(queue)):
        divide()

 
    while(queue[0][0]<LB_old):
        #找出已排好的 並比較LB POP掉他
        for i in range(len(queue)):
            if len(queue[i][1])==len(job_list):
                if queue[i][0]<LB_old:
                    LB_old = queue[i][0]
                    best_perm = queue[i][1]
                    #pop out
                    queue[0] = queue[len(queue)-1]
                    queue = queue[0:len(queue)-1]
                    adjust()
        
        #heapify後 抓出queue第一項，繼續divide
        divide()

    print('total completion time is ' , LB_old)
    print('with the permutation of: ',best_perm)

    
    
    
bfs(job_list[0])

