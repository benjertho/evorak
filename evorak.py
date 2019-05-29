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

# TODO combine mirrored digraphs
# TODO define alphabet from most used characters



class individual(list):
    def __init__(self):
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
    def __init__(self):
        self.total_fitness = 0.0
        pass
    
    def load_file(self):
        with open ("map-it.csv","r") as file:
            # Skip the header if the file has one
            has_header = csv.Sniffer().has_header(file.read(1024))
            file.seek(0)  # Rewind.
            reader = csv.reader(file, delimiter=',', quotechar='"' )
            if has_header:
                next(reader)  # Skip header row.
            
            
            
    def reproduce():
        pass
    
    
    
class dictionary():
    
    def __init__(self):
        [self.letter_freq, self.digraph_freq, self.ending_freq] = self.load_file()

    # word list source http://crr.ugent.be/programs-data/subtitle-frequencies
    # csv files should be formatted with commas as field delimiters and 
    # double quotes as text delimiters
    def load_file(self):
        with open ("subtlex-it.csv","r") as file:
            # Skip the header if the file has one
            has_header = csv.Sniffer().has_header(file.read(1024))
            file.seek(0)  # Rewind.
            reader = csv.reader(file, delimiter=',', quotechar='"' )
            if has_header:
                next(reader)  # Skip header row.

            #word_list = []
            letter_freq = {}
            digraph_freq = {}
            ending_freq = {}
            for row in reader:
                word = (row[1]).lower() # convert to lowercase
                freq = float(row[2])
                word_len = len(word)
                
                # Do not include numbers or words with numbers
                if any(char.isdigit() for char in word):
                    continue
                                
                # Letter frequency 
                if (word_len > 0):
                    #word_list.append([word,freq])
                    for letter in word:
                        if letter in letter_freq:
                            letter_freq[letter] += freq
                        else : 
                            letter_freq[letter] = freq
                
                # Digraph (letter pair) frequency
                if (word_len > 1):
                    for i in range(word_len - 1):
                        if word[i:i+2] in digraph_freq:
                            digraph_freq[word[i:i+2]] += freq
                        else : 
                            digraph_freq[word[i:i+2]] = freq
                
                # Word ending frequency
                if word[-1] in ending_freq:
                    ending_freq[word[-1]] += freq
                else : 
                    ending_freq[word[-1]] = freq
            
            print(ending_freq)
        return [letter_freq, digraph_freq, ending_freq]
    
        
    
class evorak():
    
    def __init__(self):
        self.dict = dictionary()


if __name__ == "__main__":
    evo = evorak()
    
