#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 31 17:03:24 2019

@author: ben
"""
import random                                                                                                                       

size = 8
nums = []          
addr = []                                                                                                               
for i in range(size):
    addr.append(i)
    nums.append(random.random()) 

total_val = sum(nums)
max_val = max(nums)

d = {}                                                                                                                              
pop = 0                                                                                                                         
while pop < 1000: 
    i = random.choice(addr) 
    if (nums[i] / max_val) > random.random(): 
        pop += 1
        if i in d: 
            d[i] += 1 
        else:
            d[i] = 1
            
for i in range(size):
    print(nums[i], d[i], (nums[i] * 100 / total_val) / ( d[i]/10.0) )
                                                                    
                                                               