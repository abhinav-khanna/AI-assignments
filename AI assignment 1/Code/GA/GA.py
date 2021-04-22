import random
import copy
import math
import numpy as np


#this function calculates number of attacking pairs
def fitness(individual):
    ind_fitness = 0

    for i in range(len(individual)):
        for j in range(i+1,len(individual)):
            if individual[i] == individual[j] or abs(individual[i] - individual[j]) == abs(i-j):
                ind_fitness += 1

    return ind_fitness

    
# create progeny of the chosen individuals
def crossover(individual1, individual2, crossover_cutoff):
    partition = random.randint(1,len(individual1)-1)

    temp_11 = individual1[:partition]
    temp_12 = individual1[partition:]

    temp_21 = individual1[:partition]
    temp_22 = individual1[partition:]

    prob = random.random()

    # If prob is greater than the crossover_cutoff, then exchange the 
    # "chromosomes" of the two individuals, otherwise return the same individuals
    if prob > crossover_cutoff:
	    temp_11.extend(temp_22)
	    temp_12.extend(temp_21)
	    return (temp_11, temp_12)

    else:
	    return (individual1, individual2)


    

# Create mutations in an individual
def mutation(individual, mutation_cutoff):
    prob = random.random()
    index = random.randint(0,len(individual)-1)
    if prob > mutation_cutoff:
        individual[index] = random.randint(1,len(individual))

    return individual

# Individual is an non-repeating array of numbers from 1 to 8
def generate_individual(n):
    result = list(range(1, n + 1))
    np.random.shuffle(result)
    return result

class Genetic(object):

    def __init__(self, n ,pop_size):
        #initializing a random individuals with size of initial population entered by user
        self.queens = []
        for i in range(pop_size):
            self.queens.append(generate_individual(n))



    #generating individuals for a single iteration of algorithm
    def generate_population(self, random_selections=5):
        candid_parents = []
        candid_fitness = []
        #getting individuals from queens randomly for an iteration
        for i in range(random_selections):
            candid_parents.append(self.queens[random.randint(0, len(self.queens) - 1)])
            candid_fitness.append(fitness(candid_parents[i]))
        sorted_fitness = copy.deepcopy(candid_fitness)
        
        
        #sort the fitnesses of individuals
        sorted_fitness.sort()
        print(sorted_fitness)
        
        #getting 2 first individuals(min attackings)
        best_parent = []
        second_best_parent = []

        best_index = -1
        second_best_index = -1

        for i in range(len(candid_fitness)):
            if candid_fitness[i] == sorted_fitness[0]:
                best_parent = copy.deepcopy(candid_parents[i])
                best_index = i
                break

        # sorted_fitness.pop(0)
        # candid_fitness.pop(best_index)

        for i in range(len(candid_fitness)):
            if candid_fitness[i] == sorted_fitness[1]:
                second_best_parent = copy.deepcopy(candid_parents[i])
                second_best_index = i
                break

        # sorted_fitness.pop(0)
        # candid_fitness.pop(second_best_index)

         #getting 2 first individuals(min attackings)
        worst_parent = []
        second_worst_parent = []

        worst_index = -1
        second_worst_index = -1

        for i in range(len(candid_fitness)):
            if candid_fitness[i] == sorted_fitness[-1]:
                worst_parent = copy.deepcopy(candid_parents[i])
                worst_index = i
                break

        # sorted_fitness.pop(-1)
        # candid_fitness.pop(worst_index)

        for i in range(len(candid_fitness)):
            if candid_fitness[i] == sorted_fitness[-2]:
                second_worst_parent = copy.deepcopy(candid_parents[i])
                second_worst_index = i
                break



        #crossover the two parents
        crossover_cutoff = 0
        (child_1,child_2) = crossover(best_parent, second_best_parent, crossover_cutoff)

        
        # mutation
        mutation_cutoff = 1
        child_1 = mutation(child_1, mutation_cutoff)
        child_2 = mutation(child_2, mutation_cutoff)
        
        #in code below check if each child is better than each one of queens individuals, set that individual the new child

        if fitness(child_1) > fitness(child_2):
            temp = child_1
            child_1 = child_2
            child_2 = temp

        index = -1


        print('worst_parent:' + str(fitness(worst_parent)) + ' second_worst_parent:' + str(fitness(second_worst_parent)))
        print('child_1:' + str(fitness(child_1)) + ' child_2:' + str(fitness(child_2)))
        
        sorted_fitness[-1] = fitness(child_1)
        sorted_fitness[-2] = fitness(child_2)
            
        for i in range(len(self.queens)):
            if self.queens[i] == worst_parent:
                self.queens[i] = copy.deepcopy(child_1)
                
                index = i
                break

        for i in range(len(self.queens)):
            if self.queens[i] == second_worst_parent:
                self.queens[i] = copy.deepcopy(child_2)
                break

        print(sorted_fitness)

        for q in self.queens:
            print('Queen:' + str(q) + ': ' + str(fitness(q)))

        # if fitness(child_1) <= fitness(worst_parent):
        #     for i in range(len(self.queens)):
        #         if self.queens[i] == worst_parent:
        #             self.queens[i] = copy.deepcopy(child_1)
        #             index = i
        #             break

        #     if fitness(child_2) <= fitness(second_worst_parent):
        #         for i in range(len(self.queens)):
        #             if self.queens[i] == second_worst_parent:
        #                 self.queens[i] = copy.deepcopy(child_2)
        #                 index = i
        #                 break 

        # elif fitness(child_1) < fitness(second_worst_parent):
        #     for i in range(len(self.queens)):
        #         if self.queens[i] == second_worst_parent:
        #             self.queens[i] = copy.deepcopy(child_1)
        #             index = i
        #             break 
        

        # print('fitness of the best queen:' + str(fitness(self.queens[index])))
        

    def finished(self):
        for i in self.queens:
            if fitness(i) == 0:
                arr = []
                arr.append(True)
                arr.append(i)
                return arr
            #we check if for each queen there is no attacking(cause this algorithm should work for n queen,
            # it was easier to use attacking pairs for fitness instead of non-attacking)

        arr = []
        arr.append(False)
        return arr
            

    def start(self, random_selections=5):
        #generate new population and start algorithm until number of attacking pairs is zero

        #IMPORTANT: MAX_ITERATIONS IS A HYPERPARAMETER TO CONTROL THE NUMBER OF GENERATIONS
        MAX_ITERATIONS = 100
        iteration_count = 0

        while True:
            final_state = self.finished()
            if final_state[0] == True:  #if solution is found
                
                print(('Solution : ' + str(final_state[1])))
                break

            iteration_count += 1

            if iteration_count > MAX_ITERATIONS:   #solution not found in the given number of iterations
                print('Solution not found')
                break

            self.generate_population(random_selections)
        


# ******************** N-Queen Problem With GA Algorithm ***********************

n=(int)(input('Enter the value of N \n -'))
initial_population=(int)(input('Enter initial population size \n -'))

algorithm = Genetic(n=n,pop_size=initial_population)
algorithm.start()
