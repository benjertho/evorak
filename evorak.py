# -*- coding: utf-8 -*-
"""
Evorak

Evolutionary Algorithm for Generating Dvorak-like keyboards for a specific 
language.
 
Input: A text dictionary of most-used words with frequency.
Output: An ascii-art text keyboard map

"""
import csv

'''
Function definitions
'''

# TODO digraphs include spaces at end of word
# TODO exclude numbers from char search
# TODO map upper and lower to lowercase
# 


class individual(list):
    def __init__():
        self.map = {}
    
    def evaluate_fitness():
        # TODO geometric mean of diff metrics or alternating selection rounds for pareto front
        # TODO digraphs on alternating hands
        # TODO balance of last-letters between hands
        # TODO most used letters on best keys
        pass
    
    def produce_child():
        pass
    
class population():    
    def __init__():
        self.total_fitness = 0.0
        pass
    
    def reproduce():
        pass
    
    
    
class dictionary():
    
    def __init__():
        self.word_list = load_file()
        self.letter_count = {}
        self.letter_pair_counts = {}


    # word list source http://crr.ugent.be/programs-data/subtitle-frequencies
    # csv files should be formatted with commas as field delimiters and 
    # double quotes as text delimiters
    def load_file():
        with open ("subtlex-it.csv","r") as file:
            # Skip the header if the file has one
            has_header = csv.Sniffer().has_header(file.read(1024))
            file.seek(0)  # Rewind.
            reader = csv.reader(file, delimiter=',', quotechar='"' )
            if has_header:
                next(reader)  # Skip header row.


            count = 0
            for row in myreader:
                word = row[1]
                freq = float(row[2])
                
                if any(char.isdigit() for char in row[1])
                    continue
                if (len(row[1]) > 0):
                    wordList.append(row[1])
                    for letter in row[1]:
                        if letter in letterCount :  
                            letterCount[letter] += 1
                        else : 
                            letterCount[letter] = 1
                    
    print(letterCount)
    
        
    
class evorak():
    
    def __init__():
        self.load_file()
        
    
                    
                    
    return wordList



if __name__ == "__main__":
    evo = evorak()
    
