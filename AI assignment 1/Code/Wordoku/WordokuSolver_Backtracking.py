from itertools import combinations
import enchant
import time

def initialise_dict(grid, row_alldiff, col_alldiff, box_alldiff):
	for row in range(len(grid[0])):
		for col in range(len(grid)):
			if grid[row][col] != '*':
				val = grid[row][col]
				row_alldiff[row][val] = True   # Set occurrence of a value in the row, column and box to reduce domain
				col_alldiff[col][val] = True
				box_alldiff[int(row/3)][int(col/3)][val] = True

	return (row_alldiff, col_alldiff, box_alldiff)

def backtrack(grid, row_alldiff, col_alldiff, box_alldiff, values, nodes_generated):

	row = -1
	col = -1
	flag = 0

	#Find an empty cell
	for i in range(len(grid[0])):
		for j in range(len(grid)):
			if grid[i][j] == '*':
				row = i
				col = j
				flag = 1
				break

		if flag == 1:
			break


	# If no empty cell is found, it means that the Wordoku has been solved
	if row == -1 or col == -1:
		return (grid, True, nodes_generated)

	for var in values:
		# Check if a particular value has already been assigned in the same row/column/box
		if row_alldiff[row][var] == False and col_alldiff[col][var] == False and box_alldiff[int(row/3)][int(col/3)][var] == False:

			# Mark that value as assigned temporarily
			grid[row][col] = var
			row_alldiff[row][var] = True
			col_alldiff[col][var] = True
			box_alldiff[int(row/3)][int(col/3)][var] = True

			# Recursive call on the same grid
			(new_grid, response, nodes_generated) = backtrack(grid, row_alldiff, col_alldiff, box_alldiff, values, nodes_generated + 1)


			# Response is true if a solution is found, meaning that the assignment was correct. So we can just return the same grid
			if response == True:
				return (new_grid, True, nodes_generated)

			# Means that the assignment was incorrect. Reverse the assignments, and check with a new value
			else:
				grid[row][col] = '*'
				row_alldiff[row][var] = False
				col_alldiff[col][var] = False
				box_alldiff[int(row/3)][int(col/3)][var] = False


	# If no solution exists for the Wordoku
	return ([],False, nodes_generated)


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

	f.close()

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


# print all meaningful substrings
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


#Code execution begins here
total_clock_time_start = time.time()
(values, grid) = read_file()    #read the file "input.txt" to determine the values in the domain and the wordoku itself


temp_dict = {}

for var in values:
	temp_dict[var] = False


row_alldiff = []
col_alldiff = []
box_alldiff = []


#Using a dictionary to maintian alldiff in all of the rows, columns and boxes
for i in range(len(values)):
	temp_dict = {}

	for var in values:
		temp_dict[var] = False   # Each value is initially set False, meaning it has not been seen yet. 

	row_alldiff.append(temp_dict)

for i in range(len(values)):
	temp_dict = {}

	for var in values:
		temp_dict[var] = False

	col_alldiff.append(temp_dict)


for i in range(3):
	box = []
	for j in range(3):
		temp_dict = {}

		for var in values:
			temp_dict[var] = False

		box.append(temp_dict)
	box_alldiff.append(box)



#print the initial unsolved grid
for i in range(len(grid[0])):
	for j in range(len(grid)):
		print(grid[i][j], end = ' ')

	print()

print('--------------------------------------------------------------')


#Intialising the dictionaries for rows, columns and boxes
#The values that are given in the beginning itself are marked as True, 
# i.e. they are not to be changed, and also reduce the domain for the
# respective row, column and box

(row_alldiff, col_alldiff, box_alldiff) = initialise_dict(grid, row_alldiff, col_alldiff, box_alldiff)



nodes_generated = 0
total_search_time_start = time.time()


# returns a 3-tuple
# solution is an N x N array if the wordoku can be solved, otherwise it is an empty array
# is_possible is a boolean variable which tells whether a solution is possible
# count of nodes generated is also returned
(solution, is_possible, nodes_generated) = backtrack(grid, row_alldiff, col_alldiff, box_alldiff, values, nodes_generated)

total_search_time_end = time.time()


# If a solution is possible, print it on the terminal, and write it to "solution.txt"
if is_possible:
	write_solution(solution)
	for i in range(len(solution[0])):
		for j in range(len(solution)):
			print(solution[i][j], end = ' ')

		print()

	print_all_meaningful_words(solution)
else:
	print("No solution exists")

total_clock_time_end = time.time()

#Various statistics about the program
print('nodes_generated:' + str(nodes_generated))
print('total_search_time:' + str(total_search_time_end - total_search_time_start))
print('total_clock_time:' + str(total_clock_time_end - total_clock_time_start))


