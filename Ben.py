# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import csv
with open ("../../Downloads/italian-word-list-total.csv","r") as csvfile:
    myreader = csv.reader(csvfile, delimiter=';')
    count = 0
    for row in myreader:
        if len(row[1]) == 5:
            count+=1
            print(row[0] , ' = ', row[1])
    print ('you have ', count, ' words with 5 letters')