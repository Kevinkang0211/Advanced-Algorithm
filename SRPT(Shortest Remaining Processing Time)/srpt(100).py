import numpy as np
import pandas as pd

p_t = pd.read_csv('p_t.csv')
r_t = pd.read_csv('r_t.csv')

p = np.array(p_t)
p = p[0]
#p = p[:80]
r = np.array(r_t)
r = r[0]
#r = r[:80]


h = np.ones(100,int)*999

#h_index = np.zeros(10,int)

#for i in range(10):
#    h_index[i]+=i

time = np.zeros(100,int)

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
        if(j<99 and i==r[j+1]):
            add_heap(h,p,j+1)    
    
    
    if(not_free()):
        p[0] = p[0]-1
        h[0] = h[0]-1
        #time[0] = time[0]+1



    i = i+1
    

    

    
    print(i)
    print(time)
    print(h)
    print(r)


sum_time = 0
for i in range(len(r)):
    sum_time = sum_time + time[i]

print('sum of completion time is: ' + str(sum_time))
   






