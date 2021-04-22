import sys
import time
import numpy as np
import tkinter as Mazegame
from termcolor import colored
from PIL import ImageTk, Image
from tkinter import ttk, Canvas, Label

import time

#This function initializes lion and meat positions
def startend_postion(n):
    start = 0
    end = n*n-1
    return start, end

#This function randomly create walls in maze
def randomize(n):
    limit = np.random.randint(n*n/4,n*n/2)
    checklist = list()

    for i in range(limit):
        hold = np.random.randint(n*n-1)
        chk = 0
        for j in range(len(checklist)):
            if checklist[j] == hold or hold == 0:
                chk = 1
        if chk == 0:
            checklist.append(hold)
    return checklist

#This function prepares full maze layout
def prepare_maze(n, checklist, start, end):
    maze = [[0 for i in range(n)] for j in range(n)]
    for i in range(len(checklist)):
        maze[checklist[i]//n][checklist[i]%n] = 1

    maze[start//n][start%n] = 0
    maze[end//n][end%n] = 0

    return maze

#
def display_maze(n, maze, pos):
    print("")
    for i in range(n):
        for j in range(n):
            if pos == i*n+j:
                print(colored("[8]", "blue"), end="")
            elif maze[i][j] == 0:
                print(colored("[0]", "green"), end="")
            elif maze[i][j] == 1:
                print(colored("[1]", "red"), end="")
            elif maze[i][j] == -1:
                print(colored("[3]", "yellow"), end="")
            elif maze[i][j] == 2:
                print(colored("[3]", "cyan"), end="")
        print("")

def make_screen(n):
    if n in range(2,9):
       size = 300
    elif n in range(9,43):
       size = 640
    elif n in range(43, 75):
       size = 750
    else:
        print("Invalid Maze size")
        sys.exit()

    cell_width = int(size/n)
    cell_height = int(size/n)

    screen = Mazegame.Tk()
    screen.title("Will lion find meat??")
    grid = Canvas(screen, width = cell_width*n, height = cell_height*n, highlightthickness=0)
    grid.pack(side="top", fill="both", expand="true")

    rect = {}
    for col in range(n):
        for row in range(n):
            x1 = col * cell_width
            y1 = row * cell_height
            x2 = x1 + cell_width
            y2 = y1 + cell_height
            rect[row, col] = grid.create_rectangle(x1,y1,x2,y2, fill="red", tags="rect")
    return grid, rect, screen, cell_width

def load_img(size, path, end):
    xcod = end//n
    ycod = end%n
    load = Image.open(path)
    load = load.resize((size, size), Image.ANTIALIAS)
    render = ImageTk.PhotoImage(load)
    img = Label(image=render)
    img.image = render
    img.place(x = ycod*size, y = xcod*size)
    return img

# This function redraws maze and updates the maze according to the traversal at 'delay' time interval
def redraw_maze(grid, rect, screen, n, maze, pos, delay, size, end):
    grid.itemconfig("rect", fill="green")
    path2 = "./meat.png"
    for i in range(n):
        for j in range(n):
            item_id = rect[i,j]
            if pos == i*n+j:
                grid.itemconfig(item_id, fill="blue")
            elif maze[i][j] == 0:                       # positions where lion can move
                grid.itemconfig(item_id, fill="salmon")
            elif maze[i][j] == 1:                       # blocked positions/walls
                grid.itemconfig(item_id, fill="black")
            elif maze[i][j] == -1:                      # positions visited    
                grid.itemconfig(item_id, fill="DeepSkyBlue2")
            elif maze[i][j] == 2:
                grid.itemconfig(item_id, fill="SpringGreen2")

    load_img(size, path2, end)
    screen.update_idletasks()
    screen.update()
    time.sleep(delay)
    return

def button(text, win, window):
    b = ttk.Button(window, text=text, command = win.destroy)
    b.pack()

def popup_win(msg, title, path ,screen):
    popup = Mazegame.Tk()
    popup.wm_title(title)
    label = ttk.Label(popup, text = msg, font=("Times", 20))
    label.pack(side="top", fill="x", pady=50, padx=50)
    button("Close Maze", screen, popup)
    button("Close popup", popup, popup)
    popup.mainloop()

#This functions check neighbours of current position i.e. current row and col    
def check_pos(row, col, n, maze):
    if row in range(n) and col+1 in range(n) and maze[row][col+1] == 0:
        return 1
    elif row+1 in range(n) and col in range(n) and maze[row+1][col] == 0:
        return 1
    elif row in range(n) and col-1 in range(n) and maze[row][col-1] == 0:
        return 1
    elif row-1 in range(n) and col in range(n) and maze[row-1][col] == 0:
        return 1
    return 0    

# Node class to represent the state, parent and path cost
class node:
	def __init__(self,current_position,parent,cost):
		self.state = current_position
		self.parent = parent
		self.path_cost = cost

# check if a node with the same state is already present in the frontier
def check_frontier(position, frontier_queue):
	for current_node in frontier_queue:
		if position == current_node.state:
			return False

	return True

# Comparator function to maintain frontier as a priority queue w.r.t path cost
def cost_comparator(node):
	return node.path_cost

# This function will contain all your search algorithms
# maze[row][col] should be used to refer to any position of maze
# pos is the starting position of maze and end is ending position
# pos//n will give row index and pos%n will give col index
# you can use list as stack or any other data structure to traverse the positions of the maze.
def search_algo(n, maze, start, end):
	start_time = time.time()

	pos = start  
	delay = 0.1
	grid, rect, screen, wid = make_screen(n)

	frontier_queue = []
	root_node = node(start,-1,0)

	frontier_queue.append(root_node)

	explored_set = [[False for j in range(n)] for i in range(n)]	#intialize explored set with all False
	
	row = int(pos/10)
	col = int(pos%10)

	explored_set[row][col] = True  #mark start node as visited

	max_memory = 0
	search_cost = 0
    
	while len(frontier_queue) != 0:
		max_memory = max(max_memory, sys.getsizeof(frontier_queue))

		# Pop the front of the frontier, and maintain the priority queue w.r.t the cost
		current_node = frontier_queue.pop(0)
		frontier_queue.sort(key = cost_comparator)

		# Calculate search cost for each node expansion
		if current_node.state != start:
			if current_node.state - current_node.parent.state == 1:		# Right movement
				search_cost += 2
			if current_node.state - current_node.parent.state == -1:	# Left movement
				search_cost += 2
			if current_node.state - current_node.parent.state == 10:	# Down movement
				search_cost += 3
			if current_node.state - current_node.parent.state == -10:	# Up movement
				search_cost += 2

		if current_node.state == end:
			end_time = time.time()
			break

		pos = current_node.state
		row = int(pos/10)
		col = pos%10

		explored_set[row][col] = True 	#mark this node as visited

		# Check for various cases of the maze. Row = 0 means topmost row, row = n-1 means bottom row.
		# Similarly, col = 0 means leftmost column, col = n-1 means rightmost column
		# For the topmost row, col = 0 and col = n-1 can only have two neighbors, and three otherwise. Same applies to the bottom row.
		# For all other rows, col = 0 and col = n-1 can have three neighbors, and four otherwise.

		# For each cell the above conditions are checked, and then its valid neighbors are checked
		# If those neighbors have not been visited, and not already in the frontier, then they are added to the frontier

		# While creating a new node, the path cost of the new node is the path cost of the existing node + step cost
		# Step cost is 3 for downward movement, and 2 for all other cases

		# Also, frontier maintains a priority queue w.r.t cost 

		if row == 0:
			if col == 0:
				if maze[row][col+1] == 0: 	#check only for valid neighbors
					if explored_set[row][col+1] == False and check_frontier(pos+1,frontier_queue): 	#check for unvisited node
						frontier_queue.append(node(pos+1,current_node,current_node.path_cost + 2))
						frontier_queue.sort(key = cost_comparator)

				if maze[row+1][col] == 0: 	
					if explored_set[row+1][col] == False and check_frontier(pos+10,frontier_queue): 	
						frontier_queue.append(node(pos+10,current_node,current_node.path_cost + 3))
						frontier_queue.sort(key = cost_comparator)


			elif col == n-1:
				if maze[row][col-1] == 0: 	
					if explored_set[row][col-1] == False and check_frontier(pos-1,frontier_queue): 	
						frontier_queue.append(node(pos-1,current_node,current_node.path_cost + 2))
						frontier_queue.sort(key = cost_comparator)

				if maze[row+1][col] == 0: 	
					if explored_set[row+1][col] == False and check_frontier(pos+10,frontier_queue): 	
						frontier_queue.append(node(pos+10,current_node,current_node.path_cost + 3))
						frontier_queue.sort(key = cost_comparator)
			else:
				if maze[row][col+1] == 0: 	
					if explored_set[row][col+1] == False and check_frontier(pos+1,frontier_queue): 	
						frontier_queue.append(node(pos+1,current_node,current_node.path_cost + 2))
						frontier_queue.sort(key = cost_comparator)

				if maze[row+1][col] == 0: 	
					if explored_set[row+1][col] == False and check_frontier(pos+10,frontier_queue): 	
						frontier_queue.append(node(pos+10,current_node,current_node.path_cost + 3))
						frontier_queue.sort(key = cost_comparator)

				if maze[row][col-1] == 0: 	
					if explored_set[row][col-1] == False and check_frontier(pos-1,frontier_queue): 	
						frontier_queue.append(node(pos-1,current_node,current_node.path_cost + 2))
						frontier_queue.sort(key = cost_comparator)

		elif row == n-1:
			if col == 0:
				if maze[row][col+1] == 0: 	
					if explored_set[row][col+1] == False and check_frontier(pos+1,frontier_queue): 	
						frontier_queue.append(node(pos+1,current_node,current_node.path_cost + 2))
						frontier_queue.sort(key = cost_comparator)

				if maze[row-1][col] == 0: 	
					if explored_set[row-1][col] == False and check_frontier(pos-10,frontier_queue): 	
						frontier_queue.append(node(pos-10,current_node,current_node.path_cost + 2))
						frontier_queue.sort(key = cost_comparator)


			elif col == n-1:
				if maze[row][col-1] == 0: 	
					if explored_set[row][col-1] == False and check_frontier(pos-1,frontier_queue): 	
						frontier_queue.append(node(pos-1,current_node,current_node.path_cost + 2))
						frontier_queue.sort(key = cost_comparator)

				if maze[row-1][col] == 0: 	
					if explored_set[row-1][col] == False and check_frontier(pos-10,frontier_queue): 	
						frontier_queue.append(node(pos-10,current_node,current_node.path_cost + 2))
						frontier_queue.sort(key = cost_comparator)
			else:
				if maze[row][col+1] == 0: 	
					if explored_set[row][col+1] == False and check_frontier(pos+1,frontier_queue): 	
						frontier_queue.append(node(pos+1,current_node,current_node.path_cost + 2))
						frontier_queue.sort(key = cost_comparator)

				if maze[row][col-1] == 0: 	
					if explored_set[row][col-1] == False and check_frontier(pos-1,frontier_queue): 	
						frontier_queue.append(node(pos-1,current_node,current_node.path_cost + 2))
						frontier_queue.sort(key = cost_comparator)

				if maze[row-1][col] == 0: 	
					if explored_set[row-1][col] == False and check_frontier(pos-10,frontier_queue): 	
						frontier_queue.append(node(pos-10,current_node,current_node.path_cost + 2))
						frontier_queue.sort(key = cost_comparator)
		else:
			if col == 0:
				if maze[row][col+1] == 0: 	#check only for valid neighbors
					if explored_set[row][col+1] == False and check_frontier(pos+1,frontier_queue): 	#check for unvisited node
						frontier_queue.append(node(pos+1,current_node,current_node.path_cost + 2))
						frontier_queue.sort(key = cost_comparator)

				if maze[row+1][col] == 0: 	
					if explored_set[row+1][col] == False and check_frontier(pos+10,frontier_queue): 	
						frontier_queue.append(node(pos+10,current_node,current_node.path_cost + 3))
						frontier_queue.sort(key = cost_comparator)

				if maze[row-1][col] == 0: 	
					if explored_set[row-1][col] == False and check_frontier(pos-10,frontier_queue): 	
						frontier_queue.append(node(pos-10,current_node,current_node.path_cost + 2))
						frontier_queue.sort(key = cost_comparator)


			elif col == n-1:
				if maze[row+1][col] == 0: 	
					if explored_set[row+1][col] == False and check_frontier(pos+10,frontier_queue): 	
						frontier_queue.append(node(pos+10,current_node,current_node.path_cost + 3))
						frontier_queue.sort(key = cost_comparator)

				if maze[row][col-1] == 0: 	
					if explored_set[row][col-1] == False and check_frontier(pos-1,frontier_queue): 	
						frontier_queue.append(node(pos-1,current_node,current_node.path_cost + 2))
						frontier_queue.sort(key = cost_comparator)


				if maze[row-1][col] == 0: 	
					if explored_set[row-1][col] == False and check_frontier(pos-10,frontier_queue): 	
						frontier_queue.append(node(pos-10,current_node,current_node.path_cost + 2))
						frontier_queue.sort(key = cost_comparator)

			else:
				if maze[row][col+1] == 0: 	
					if explored_set[row][col+1] == False and check_frontier(pos+1,frontier_queue): 	
						frontier_queue.append(node(pos+1,current_node,current_node.path_cost + 2))
						frontier_queue.sort(key = cost_comparator)

				if maze[row+1][col] == 0: 	
					if explored_set[row+1][col] == False and check_frontier(pos+10,frontier_queue): 	
						frontier_queue.append(node(pos+10,current_node,current_node.path_cost + 3))
						frontier_queue.sort(key = cost_comparator)

				if maze[row][col-1] == 0: 	
					if explored_set[row][col-1] == False and check_frontier(pos-1,frontier_queue): 	
						frontier_queue.append(node(pos-1,current_node,current_node.path_cost + 2))
						frontier_queue.sort(key = cost_comparator)


				if maze[row-1][col] == 0: 	
					if explored_set[row-1][col] == False and check_frontier(pos-10,frontier_queue): 	
						frontier_queue.append(node(pos-10,current_node,current_node.path_cost + 2))
						frontier_queue.sort(key = cost_comparator)


# =============================================================================        
#         Enter your code here
# =============================================================================
		
		redraw_maze(grid, rect, screen, n, maze, pos, delay, wid, end)

	# Once end is found, create a path by retracing the parents of the node, and then print the path
	if current_node.state == end:
		print('Meat found!!')

		path = []
		temp = current_node
		path.append(temp.state)

		while temp.state != start:
			path.append(temp.parent.state)
			temp = temp.parent

		path.reverse()	
		print(path)

		print('Path from start is:')

		total_cost = 0
		for i in range(len(path)-1):
			if path[i+1] - path[i] == 1:
				print('From:' + str([int(path[i]/10), int(path[i]%10)]) + ' go Right to ' + str([int(path[i+1]/10), int(path[i+1]%10)]))
			elif path[i+1] - path[i] == -1:
				print('From:' + str([int(path[i]/10), int(path[i]%10)]) + ' go Left to ' + str([int(path[i+1]/10), int(path[i+1]%10)]))
			elif path[i+1] - path[i] == 10:
				print('From:' + str([int(path[i]/10), int(path[i]%10)]) + ' go Down to ' + str([int(path[i+1]/10), int(path[i+1]%10)]))
			elif path[i+1] - path[i] == -10:
				print('From:' + str([int(path[i]/10), int(path[i]%10)]) + ' go Up to ' + str([int(path[i+1]/10), int(path[i+1]%10)]))

		# Various runtime statistics
		print('Total path cost is:' + str(current_node.path_cost))
		print('Search Cost:' + str(search_cost))
		print('Time taken:' + str(end_time - start_time))
		print('Max memory used:' + str(max_memory))

	else:
		print('Meat is unreachable')

	popup_win("   ", "   ", "./final.png" , screen)



if __name__ == "__main__":
    n = 10 # size of maze
    start, end = startend_postion(n)
    randno = randomize(n)
    maze = prepare_maze(n, randno, start, end)
    search_algo(n, maze, start, end)
