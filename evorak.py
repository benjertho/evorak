# -*- coding: utf-8 -*-

"""
Evorak

Evolutionary Algorithm for Generating Dvorak-like keyboards for a specific 
language.
 
Input: A text dictionary of most-used words and frequency of use and 
    a sample keyboard. Both files should be csv formatted like the examples.
    
Output: An ascii-art text keyboard map and change list

"""
import csv
from copy import deepcopy
import random


# TODO combine mirrored digraphs
# TODO define alphabet from most used characters
# TODO deal with character exceptions such as [' -> "]
# TODO add char ignore list -> quick and dirty

class KbKey:
    
    def __init__(self, value, weight, hand, row, pos):
        self.value = value
        self.weight = weight
        self.hand = hand
        self.row = row
        self.pos = pos

class Individual:
    
    def __init__(self, ):
        self.fitness = 0.0
        self.kb_keys = {}
    
    
    
    def produce_child():
        pass
    
    def key_print(self):
        for key, item in self.keys.items():
            print("\t" + key + ": " + item.value)
            
    def mod_key_print(self):
        for key, item in self.keys.items():
            if (key != item.value):
                print("\t" + key + " -> " + item.value)
        
    
class Population:
    
    def __init__(self, pop_size, letter_list):
        [self.parents, self.letter_count, self.letter_list] = self.load_file(pop_size, letter_list)            
        self.offspring = []
        self.total_fitness = 0.0
    
    def load_file(self, size, letter_list):
        with open ("kb-it.csv","r") as file:
            # Skip the header if the file has one
            has_header = csv.Sniffer().has_header(file.read(10))
            file.seek(0)  # Rewind.
            reader = csv.reader(file, delimiter=',', quotechar='"' )
            if has_header:
                next(reader)  # Skip header row.
            
            # Generate an "individual" from the original keyboard layout
            breeder = individual()
            count = 0
            for row in reader:
                name = (row[0]).lower()
                if name != '':
                    if name not in breeder.keys:
                        breeder.keys[name] = key(name, 1.0 + count * 0.1, row[1], \
                                    row[2], row[3])
                        count += 1
                    else:
                        print("WARNING: " + name + " is duplicated in keyboard file")
        
        # Include most freq letters from dict while keeping kb similar to orig
        
        # Truncate letter list to number of keys avail
        letter_list = letter_list[:count]
        # Find non-common elements of keys and letters
        dict_set = set([x[0] for x in letter_list]) 
        kb_set = set(breeder.keys.keys())
        dict_unique = list(dict_set - kb_set)
        kb_unique = list(kb_set - dict_set)
        # Pair letters unaccounted for
        if (len(dict_unique) == len(kb_unique)):
            for i in range(len(dict_unique)):
                breeder.keys[kb_unique[i]].value = dict_unique[i]
        else:
            print("Warning: dict_unique and kb_unique of unequal size")
                
        print("\nTotal keys: " + str(count))
        print("\nInitial changes:")
        breeder.mod_key_print()
        # Initialize the population from copies of the original individual
        breeders = []
        for i in range(size):
            breeders.append(deepcopy(breeder))
        return breeders, count, letter_list
        
    def reproduce():
        pass
    
    
    
class Dictionary:
    
    def __init__(self):
        [self.letter_dict, self.digraph_dict, self.ending_dict, self.letter_list] = self.load_file()

    # word list source http://crr.ugent.be/programs-data/subtitle-frequencies
    # csv files should be formatted with commas as field delimiters and 
    # double quotes as text delimiters
    def load_file(self):
        with open ("subtlex-it.csv","r") as file:
            # Skip the header if the file has one
            has_header = csv.Sniffer().has_header(file.read(10))
            file.seek(0)  # Rewind.
            reader = csv.reader(file, delimiter=',', quotechar='"' )
            if has_header:
                next(reader)  # Skip header row.

            # Generate dicts from file
            letter_dict = {}
            digraph_dict = {}
            ending_dict = {}
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
                        if letter in letter_dict:
                            letter_dict[letter] += freq
                        else : 
                            letter_dict[letter] = freq
                
                # Digraph (letter pair) frequency
                if (word_len > 1):
                    for i in range(word_len - 1):
                        if word[i:i+2] in digraph_dict:
                            digraph_dict[word[i:i+2]] += freq
                        else : 
                            digraph_dict[word[i:i+2]] = freq
                
                # Word ending frequency
                if word[-1] in ending_dict:
                    ending_dict[word[-1]] += freq
                else : 
                    ending_dict[word[-1]] = freq
            
        # Generate sorted letter list from dict
        letter_list = []
        for letter, freq in letter_dict.items():
            letter_list.append([letter, freq])
        letter_list.sort(key=lambda x: x[1], reverse = True)
        
        return [letter_dict, digraph_dict, ending_dict, letter_list]
        
    def clean(self, letter_list):
        represented_set = set([x[0] for x in letter_list]) 
        total_set = set(self.letter_dict.keys())
        purge_set = total_set - represented_set
        print("\nUnrepresented characters and occurences:")
        for letter in purge_set:
            #print("\t" + letter)
            for key in list(self.letter_dict):
                if letter in key:
                    print("\t" + letter + "\t" + str(self.letter_dict[key]))
                    del self.letter_dict[key]
            for key in list(self.digraph_dict):
                if letter in key:
                    del self.digraph_dict[key]
            for key in list(self.ending_dict):
                if letter in key:
                    del self.ending_dict[key]
    
            
class Evorak():
    
    def __init__(self, pop_size, run_cnt):
        random.seed()
        self.run_cnt = run_cnt
        self.dict = dictionary()
        self.pop = population(pop_size, self.dict.letter_list)
        self.dict.clean(self.pop.letter_list)
        
    def run(self):
        for i in range(self.run_cnt):
            self.total_fitness = self.assign_fitnesses(self.pop, self.dict)
            self.next_generation()
    
    def next_generation(self, total_fitness, pop_size):
        resolution = total_fitness / pop_size
        offset = random.random() * resolution
        for parent in population.parents:
            # TODO stochastic acceptance
        
    def assign_fitnesses(self, population, dictionary):
        max_fitness = 0
        min_fitness = 0
        for individual in population:
            # Score based on freq of use and key preference and
            freqpref_element = 0.0
            # consider the ending of words to balance which hand spaces
            left_hand_ending = 0.0
            right_hand_ending = 0.0
            for [letter, freq] in dictionary.letter_dict:
                freqpref_element += freq * individual.kb_keys[letter].weight
                if individual.kb_keys[letter].hand == 0:
                    right_hand_ending += freq
                else:
                    left_hand_ending += freq
            ending_element = abs(right_hand_ending - left_hand_ending)
            # Consider how often a hand must type two characters in a row
            digraph_element = 0.0
            for [digraph, freq] in dictionary.digraph_dict:
                if individual.kb_keys[digraph[0]].hand == individual.kb_keys[digraph[1]].hand:
                    digraph_element += freq
                    
            # Geometric mean
            individual.fitness = pow(freqpref_element * ending_element * digraph_element, 1.0/3.0)
            if individual.fitness > max_fitness:
                max_fitness = individual.fitness
        
        # Best fitness is actually the smallest of the values calculated above,
        # so perform reversal and normalize
        for individual in population:
            individual.fitness = (max_fitness - individual.fitness + min_fitness) / max_fitness
            
        # Total fitness
        total_fitness = 0.0
        for individual in population:
            total_fitness += individual.fitness
            
        return total_fitness
        
if __name__ == "__main__":
    evo = evorak(20, 10)
    evo.run()
    
