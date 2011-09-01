# takes two arrays and scores the differe higher is better
# both are lists of variable length that contains a list of 2 ints
import sys
import cPickle


def compare_results(base, compare):
    base_file = open(base, 'r')
    compare_file = open(compare, 'r')
    
    base_list = cPickle.load(base_file)
    compare_list = cPickle.load(compare_file)
    
# take the compared number 
    
    score = 0
    for i in range(len(compare_list)):
        score += abs(compare_list[i][0] - base_list[i][0])
        score += abs(compare_list[i][1] - base_list[i][1])
        
    return score
