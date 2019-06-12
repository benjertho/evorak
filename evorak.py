# -*- coding: utf-8 -*-

"""
Evorak

Evolutionary Algorithm for Generating Dvorak-like keyboards for a arbitrary 
languages.
 
Input: (Both files should be csv formatted like the examples.)
    1. Text dictionary of most-used words and their frequency of use
    2. Sample keyboard. 
    
Output: 
    1. Ascii-art text keyboard map 
    2. csv representing said map as a starting point for future runs 

"""
import csv
from copy import deepcopy
import random
import sys

# TODO add char ignore list -> quick and dirty
# TODO add ability for array of elites
# TODO continuous printing of keyboard

class KbKey:
    
    def __init__(self, orig_value, weight, hand, row, pos):
        self.orig_value = orig_value
        self.weight = weight
        self.hand = hand
        self.row = row
        self.pos = pos


class Individual:
    
    def __init__(self):
        self.fitness = 0.0
        self.distance = 0.0
        self.norm_fitness = 0.0
        self.kb_keys = {}
    
    def produce_child():
        pass
             
    def key_print(self):
        for key, item in self.kb_keys.items():
            print("\t" + item.orig_value + ": " + key)
            
    def mod_key_print(self):
        for key, item in self.kb_keys.items():
            if (key != item.orig_value):
                print("\t" + item.orig_value + " -> " + key)
        
        
class Population:
    
    def __init__(self, pop_size, letter_list):
        self.pop_size = pop_size
        self.parents = []
        self.elite = None
        self.kb_key_count = 0
        self.min_row = 0
        self.max_row = 0
        self.max_pos = 0
        self.load_file(letter_list)
    
    def load_file(self, letter_list):
        with open ("kb-it.csv","r") as file:
            # TODO make this skipping code a function
            # Skip the header if the file has one
            has_header = csv.Sniffer().has_header(file.read(10))
            file.seek(0)  # Rewind.
            reader = csv.reader(file, delimiter=',', quotechar='"' )
            if has_header:
                next(reader)  # Skip header row.
            
            # Generate an "individual" from the original keyboard layout
            parent = Individual()
            self.kb_key_count = 0
            for row in reader:
                name = (row[0]).lower()
                if name != '':
                    if name not in parent.kb_keys:
                        parent.kb_keys[name] = KbKey(name, 1.0 + (self.kb_key_count * 0.1), int(row[1]), int(row[2]), int(row[3]))
                        self.kb_key_count += 1           
                        self.min_row = min(parent.kb_keys[name].row, self.min_row)
                        self.max_row = max(parent.kb_keys[name].row, self.max_row)
                        self.max_pos = max(parent.kb_keys[name].pos, self.max_pos)
                    else:
                        print("WARNING: " + name + " is duplicated in keyboard file")
        
        # Include most freq letters from dict while keeping kb similar to orig
        
        # Truncate letter list to number of keys avail
        letter_list = letter_list[:self.kb_key_count]
        # Find non-common elements of keys and letters
        dict_set = set([x[0] for x in letter_list]) 
        kb_set = set(parent.kb_keys.keys())
        dict_unique = list(dict_set - kb_set)
        kb_unique = list(kb_set - dict_set)
        # Pair letters unaccounted for
        if (len(dict_unique) == len(kb_unique)):
            for i in range(len(dict_unique)):
                parent.kb_keys[dict_unique[i]] = parent.kb_keys[kb_unique[i]]
                parent.kb_keys.pop(kb_unique[i])
        else:
            print("Warning: dict_unique and kb_unique of unequal size")
                
        print("\nTotal keys: " + str(self.kb_key_count))
        print("\nInitial changes:")
        parent.mod_key_print()
        # Initialize the population from copies of the original individual
        for i in range(self.pop_size):
            self.parents.append(deepcopy(parent))
        self.elite = self.parents[0]
        
    def reproduce():
        pass
    
    
    def kb_print(self, ind):
        # print "csv", to be used as a future starting point
        
        print ('"Original Keys in Fitness Order (Best First)","Hand (Right = 0)","Row","Pos"')
        for i in range(self.kb_key_count):
            for letter, kb_key in ind.kb_keys.items():
                if kb_key.weight == 1.0 + 0.1 * i:
                    print('"' + letter + '",' + str(kb_key.hand) + ',' + \
                          str(kb_key.row) + ',' + str(kb_key.pos))
        print('')
        # print layout
        row = self.min_row
        pos = 0
        while row <= self.max_row:
            char_printed = False
            for letter, kb_key in ind.kb_keys.items():
                if kb_key.row == row and kb_key.pos == pos:
                    print(letter + ' ', end = '')
                    char_printed = True
                    break
            if char_printed == False:
                print('  ', end = '')
            pos += 1
            if pos > self.max_pos:
                print('')
                pos = 0
                row += 1
        print('')
            
    
class Dictionary:
    
    def __init__(self):
        self.letter_dict = {}
        self.digraph_dict = {}
        self.ending_dict = {}        
        self.letter_list = []

        self.load_file()

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
            for row in reader:
                word = (row[1]).lower() # convert to lowercase
                freq = float(row[2])
                word_len = len(word)
                
                # Do not include numbers or words with numbers
                if any(char.isdigit() for char in word):
                    continue
                
                # exclude both for formatting issues and because it is "uppercase" of '
                if word == '"':
                    continue
                                
                # Letter frequency 
                if (word_len > 0):
                    #word_list.append([word,freq])
                    for letter in word:
                        if letter in self.letter_dict:
                            self.letter_dict[letter] += freq
                        else : 
                            self.letter_dict[letter] = freq
                
                # Digraph (letter pair) frequency
                if (word_len > 1):
                    for i in range(word_len - 1):
                        if word[i:i+2] in self.digraph_dict:
                            self.digraph_dict[word[i:i+2]] += freq
                        # check for reversed digraph
                        elif word[i+1] + word[i] in self.digraph_dict:
                            self.digraph_dict[ word[i+1] + word[i] ] += freq
                        else : 
                            self.digraph_dict[word[i:i+2]] = freq
                
                # Word ending frequency
                if word[-1] in self.ending_dict:
                    self.ending_dict[word[-1]] += freq
                else : 
                    self.ending_dict[word[-1]] = freq
            
        # Generate sorted letter list from dict
        for letter, freq in self.letter_dict.items():
            self.letter_list.append([letter, freq])
        self.letter_list.sort(key=lambda x: x[1], reverse = True)
        
        #print (self.letter_dict)
        
    def clean(self, kb_key_count):
        self.letter_list = self.letter_list[:kb_key_count]
        represented_set = set([x[0] for x in self.letter_list]) 
        total_set = set(self.letter_dict.keys())
        purge_set = total_set - represented_set
        print("\nCharacters unaccounted for:")
        for letter in purge_set:
            # key in list because we're deleting them and it throws errors otherwise
            for key in list(self.letter_dict):
                if letter == key:
                    print("\t" + letter + "\t" + str(self.letter_dict[key]))
                    del self.letter_dict[key]
            for key in list(self.digraph_dict):
                if letter in key:
                    del self.digraph_dict[key]
            for key in list(self.ending_dict):
                if letter in key:
                    del self.ending_dict[key]
        print('')
                    
class Evorak():
    
    def __init__(self, pop_size, mutation_rate, cutoff):
        random.seed()
        self.cutoff = cutoff
        self.mutation_rate = mutation_rate
        self.dict = Dictionary()
        self.pop = Population(pop_size, self.dict.letter_list)
        self.dict.clean(self.pop.kb_key_count)
        self.current_run = 0
        self.runs_without_improvement = 0
        self.temp_key = KbKey("a", 1, 0, 0, 0)
        self.best_distance_yet = sys.float_info.max
        self.best_distance_initial = sys.float_info.max
        
    def run(self):
        self.assign_fitnesses()
        best_distance_initial = self.best_distance_yet
        
        while self.runs_without_improvement < self.cutoff:
            self.current_run += 1
            self.assign_fitnesses()
            self.next_generation()
            # Print progress
            sys.stdout.write('\r') # return carriage
            sys.stdout.write("Run: " + str(self.current_run) + ", Best/Initial: " + str(round(100 * self.best_distance_yet/best_distance_initial, 5)) + "%       ")
            sys.stdout.flush()
        print('\n')
        
        self.pop.kb_print(self.pop.elite)
    
    def next_generation(self):
        offspring = []
        offspring.append(deepcopy(self.pop.elite))
        while len(offspring) < self.pop.pop_size:
            parent = random.choice(self.pop.parents)
            # Stochastic acceptance based on parent fitness
            if parent.norm_fitness > random.random():
                offspring.append(deepcopy(parent))
                # with a probability mutation_rate swap 2 keys of the newest individual
                # TODO move this functionality into individual
                if self.mutation_rate > random.random():
                    kb_key1 = random.choice(self.dict.letter_list)[0]
                    kb_key2 = random.choice(self.dict.letter_list)[0]
                    self.temp_key = offspring[-1].kb_keys[kb_key1]
                    offspring[-1].kb_keys[kb_key1] = offspring[-1].kb_keys[kb_key2]
                    offspring[-1].kb_keys[kb_key2] = self.temp_key
        self.pop.parents = offspring
        
    def assign_fitnesses(self):
        max_distance = sys.float_info.min
        min_distance = sys.float_info.max
        max_fitness = sys.float_info.min
        for parent in self.pop.parents:
            # Score based on freq of use and key preference and weight
            freqpref_element = 0.0
            # consider the ending of words to balance which hand spaces
            left_hand_ending = 0.0
            right_hand_ending = 0.0
            for letter, freq in self.dict.letter_dict.items():
                freqpref_element += freq * parent.kb_keys[letter].weight
                if parent.kb_keys[letter].hand == 0:
                    right_hand_ending += freq
                else:
                    left_hand_ending += freq
            ending_element = abs(right_hand_ending - left_hand_ending)
            # Consider how often a hand must type two characters in a row
            digraph_element = 0.0
            for digraph, freq in self.dict.digraph_dict.items():
                if parent.kb_keys[digraph[0]].hand == parent.kb_keys[digraph[1]].hand:
                    digraph_element += freq
                    
            # Geometric mean
            parent.distance = pow(freqpref_element * ending_element * digraph_element, 1.0/3.0)
            max_distance = max(max_distance, parent.distance)
            min_distance = min(min_distance, parent.distance)                
                        
        # Best fitness is actually the smallest of the values calculated above,
        # so perform reversal and normalization
        for parent in self.pop.parents:
            parent.fitness = max_distance + min_distance - parent.distance
            if parent.fitness > max_fitness:
                max_fitness = parent.fitness
                self.pop.elite = parent
            
        for parent in self.pop.parents:
            parent.norm_fitness = parent.fitness / max_fitness
        
        if self.pop.elite.distance < self.best_distance_yet:
            self.best_distance_yet = self.pop.elite.distance
            self.runs_without_improvement = 0
        else:
            self.runs_without_improvement += 1
        
        
if __name__ == "__main__":
    # pop_size, mutation_rate, cutoff
    evo = Evorak(1000, 0.5, 10)     
    evo.run()
