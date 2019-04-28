# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import csv

'''
Function definitions
'''


def loadFile():
    wordList = []
    letterCount = {}
    with open ("italian-word-list-total.csv","r") as csvfile:
        myreader = csv.reader(csvfile, delimiter=';')
        count = 0
        for row in myreader:
            if (len(row[1]) > 0):
                wordList.append(row[1])
                for letter in row[1]:
                    if letter in letterCount :  
                        letterCount[letter] += 1
                    else : 
                        letterCount[letter] = 1
                    
    print(letterCount)
                    
                    
    return wordList




'''
 Main Program
'''
    
wordList = loadFile()
