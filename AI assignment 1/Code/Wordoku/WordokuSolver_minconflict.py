import random
from itertools import combinations
import enchant
import time

def initialise_grid(grid,values):
	for row in range(len(grid[0])):
		for col in range(len(grid)):
			if grid[row][col] == '*':
				rand_index = random.randint(0,len(values)-1)   
				rand_value = values[rand_index]			#assign random value to any empty cell
				grid[row][col] = rand_value

	return grid

# count the conflicts in the row, column and box for one cell
def count_cell_conflicts(grid, row, col):
	count = 0

	for i in range(len(grid[0])):
		if i != col and grid[row][col] == grid[row][i]:
			count += 1

	for i in range(len(grid)):
		if i != row and grid[row][col] == grid[i][col]:
			count += 1

	box_start_row = row - (row % 3)
	box_start_col = col - (col % 3)

	for i in range(box_start_row,box_start_row+3):
		for j in range(box_start_col, box_start_col+3):
			if (i != row or j != col) and (grid[row][col] == grid[i][j]):
				count += 1

	return count


# count total conflicts in a grid
def count_total_conflicts(grid):
	count = 0

	for row in range(len(grid[0])):
		for col in range(len(grid)):
			count += count_cell_conflicts(grid,row,col)

	return int(count/2)  #each conflict has been counted twice


# Read file to create domain and the Wordoku from "input.txt"
def read_file():
	f = open("input.txt", "r")
	values = []
	grid = []
	for row in f:
		temp_ls = []
		for ch in row:
			if ch != ' ' and ord(ch) != 10 and ch != '*':
				if ch not in values:
					values.append(ch)

			if ch != ' ' and ord(ch) != 10:
				temp_ls.append(ch)

		if len(temp_ls) != 0:
			grid.append(temp_ls)

	return (values, grid)


# Write solution to "solution.txt"
def write_solution(solution):

	f = open('solution.txt', 'w')
	f.close()
	for i in range(len(solution[0])):
		f = open('solution.txt', 'a')
		row = ''
		for j in range(len(solution)):
			row += str(solution[i][j]) + ' '

		row += '\n'

		f.write(row)
		f.close()

# checks all meaningful substrings of a given row/column/diagnol
def check_all_substrings(test_str):
	all_subtrings = [test_str[x:y] for x, y in combinations(range(len(test_str) + 1), r = 2)]
	res = []
	d = enchant.Dict("en_US")

	for x in all_subtrings:
		if d.check(x):
			if x not in res:
				res.append(x)

	return res


# print all meaningful substrings given the entire grid
def print_all_meaningful_words(grid):
	result = []

	complete_string = ''
	for row in range(len(grid[0])):
		complete_string = ''
		for col in range(len(grid)):
			complete_string += grid[row][col]
		temp = check_all_substrings(complete_string)
		result.extend(temp)

	for col in range(len(grid)):
		complete_string = ''
		for row in range(len(grid[0])):
			complete_string += grid[row][col]
		temp = check_all_substrings(complete_string)
		result.extend(temp)


	complete_string = ''
	for i in range(len(grid)):
		complete_string += grid[i][i]
	temp = check_all_substrings(complete_string)
	result.extend(temp)

	complete_string = ''
	for i in range(len(grid)):
		complete_string += grid[i][8-i]
	temp = check_all_substrings(complete_string)
	result.extend(temp)



	print('The meaningful words found are:')
	if len(result) != 0:
		print(set(result))
	else:
		print('None')


# create a 2D array of boolean values to see which cells have already
# been assigned in the problem itself. These cells are not to be assigned
# any other value
def check_fixed_values(grid):
	fixed_values = []
	for row in range(len(grid[0])):
		temp_ls = []
		for col in range(len(grid)):
			if grid[row][col] == '*':
				temp_ls.append(False)
			else:
				temp_ls.append(True)

		fixed_values.append(temp_ls)
	return fixed_values


# code execution starts here
total_clock_time_start = time.time()
(values, grid) = read_file()
fixed_values = check_fixed_values(grid)

# print the grid read from "input.txt"
for i in range(len(grid[0])):
	for j in range(len(grid)):
		print(grid[i][j], end = ', ')

	print()


total_search_time_start = time.time()

(grid) = initialise_grid(grid,values)


# MAX_STEPS is a hyperparameter to control the total number of generations produced
MAX_STEPS = 1000
total_conflict = count_total_conflicts(grid)

print('initial total conflicts:' + str(total_conflict))
print('------------------------------------------------')


# Run the algorithm MAX_STEPS number of times
for step in range(MAX_STEPS):

	# If there are no conflicts, it means that the solution has been found
	if total_conflict == 0:
		print('Solution found!!')
		for i in range(len(grid[0])):
			for j in range(len(grid)):
				print(grid[i][j], end = ', ')

			print()
		break


	# Choosing a variable randomly means choosing a 
	# random row and column
	rand_row = random.randint(0,len(grid[0])-1)
	rand_col = random.randint(0,len(grid)-1)


	existing_conflicts = count_cell_conflicts(grid, rand_row, rand_col)

	
	# Having chosen a variable randomly, try all values and count the total conflicts with that assignment
	# Assign the value which minimizes the total number of conflicts
	if existing_conflicts != 0:
		for val in values:
			existing_val = grid[rand_row][rand_col]
			if not fixed_values[rand_row][rand_col]:
				grid[rand_row][rand_col] = val
			
			new_total_conflicts = count_total_conflicts(grid)
			if new_total_conflicts > total_conflict:
				grid[rand_row][rand_col] = existing_val
			else:
				total_conflict = new_total_conflicts

			

print('final total conflicts:' + str(total_conflict))
total_search_time_end = time.time()


# If a solution is possible, print it on the terminal, and write it to "solution.txt"
write_solution(grid)

for i in range(len(grid[0])):
	for j in range(len(grid)):
		print(grid[i][j], end = ', ')

	print()

print_all_meaningful_words(grid)

#Various statistics about the program
total_clock_time_end = time.time()
print('Total Clock Time:' + str(total_clock_time_end - total_clock_time_start))
print('Total Search Time:' + str(total_search_time_end - total_search_time_start))