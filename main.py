# fold all - ctrl + K + 1
# unfold all - ctrl + K + J

# import only system from os 
import os
import copy
import random
import math
import sys
import time
  
# format: (col, row)
STANDARD = [

	[-1, -1], [0, -1], [1, -1], 

	[-1, 0],		   [1, 0],

	[-1, 1],  [0, 1],  [1, 1], 

]

SIDES = [

			[0, -1],

	[-1, 0],		[1, 0],

			[0, 1],

]

CORNERS = [

	[-1, -1], 		  [1, -1], 



	[-1, 1],  		  [1, 1], 

]

history = []	# record of previous generations

# costumes
ALIVE = '[]'
DEAD = 	'  '

# grid size
size = os.get_terminal_size()
ROW = size.lines - 3						# -3 accounts for border and the extra "input" row
COL = (size.columns // len(ALIVE)) - 2		# -2 accounts for border; division is if the cell occupies >2 characters

# settings
# default is (Born 3; Survive 2, 3) or (B3S23)
# [min, max]
BORN = [3, 3]
SURVIVE = [2, 3]
NEIGHBOR = STANDARD
HISTORY_CAP = 2						# max number of elements in history
GENERATION_INCREMENT = 500			# maximum number of times it updates before pausing
REFRESH = 0.05						# refresh rate in seconds
  
def list_to_string(l):

	# convert everything to a string
	# join it to an empty string
	return ''.join(map(str, l))

# clear the display and update it
def update_display(grid):

	# adjust the number based on how far right you want it
	tab = '\t' * 0#4

	# based on the cell's costume, determine the length of the horizontal border
	# + 2 accounts for the vertical border
	border = '-' * ((len(grid[0]) * len(ALIVE)) + 2)

	string = tab + border

	for row in grid:
		substring = ''
		for col in row:

			if col == 1:
				substring = substring + ALIVE
			else:
				substring = substring + DEAD

		string = '%s\n%s|%s|' %(string, tab, substring)

	string = '%s\n%s%s\n' %(string, tab, border)

	# use this instead of print() so that the frames don't act choppy
	sys.stdout.write(string)
	sys.stdout.flush()

# create a 10 x 10 display
def init(rowNum, colNum):	

	grid = []

	for row_index in range(rowNum):

		lst = []

		for col_index in range(colNum):

			# 1/4 chance to be alive
			lst.append(1 * (random.randint(1, 4) == 1))

		# add to the grid
		grid.append(lst)
		
	update_display(grid)
	return grid

# changes the grid based on the rules
def generation(grid, history):	

	start = time.time()

	# keep track of the original for reference
	old_grid = copy.deepcopy(grid)

	history.insert(1, old_grid)

	if len(history) > HISTORY_CAP:
		history = history[0:HISTORY_CAP + 1]

	# for every cell in the grid
	# row and col are the coordinates
	for row_index in range(len(grid)):
		for col_index in range(len(grid[row_index])):

			# allow changing of row and column index without affecting the loop
			row = row_index
			col = col_index

			# use this to determine if the cell should be ALIVE or DEAD
			neighbor_count = 0

			# check for neighbors
			for lst in NEIGHBOR:
				n_row = lst[0]
				n_col = lst[1]

				# this is a grid that uses negative indexing, so cross-screen teleport style
				# however, we must fix the positive bounds
				# note ">=" sign is because of zero indexing
				if row + n_row >= len(grid):
					row = -1
				
				if col + n_col >= len(grid[0]):
					col = -1

				# check if the neighbor is ALIVE
				if old_grid[row + n_row][col + n_col] == 1:
					neighbor_count += 1						

			#print(neighbor_count)

			#----------RULES----------#
			# Survive - "Any live cell with two or three live neighbours survives"
			if (old_grid[row][col] == 1) and (neighbor_count < SURVIVE[0] or neighbor_count > SURVIVE[1]):

				grid[row][col] = 0				

			# Born - "Any dead cell with three live neighbours becomes a live cell"
			elif (old_grid[row][col] == 0) and (neighbor_count >= BORN[0] and neighbor_count <= BORN[1]):

				grid[row][col] = 1


	# end script if nothing changed
	for generation in history:

		if grid == generation:

			return False

	update_display(grid)

	# maintain stable framerate
	finish = time.time()
	lag = finish - start
	delay = REFRESH - lag
	time.sleep(delay * (delay > 0))

	return (grid != old_grid)


def loop():

	grid = init(ROW, COL)						# game display	
	i = 0										# iterator
	generation_limit = GENERATION_INCREMENT		# every x generations, asks to resume or quit

	time.sleep(1)

	def prompt_restart():

		restart = 'Done! Try again? (y/n)'
		if input(restart).lower() == 'n':

			print('Alright! Have a nice day :)')

		else:

			loop()	

	init_time = time.time()

	while True:

		# restart simulation prompt
		if not generation(grid, history):
			
			print('%s generations!' %i)

			endTime = time.time()
			duration = endTime - init_time
			fps = i / duration
			print('%s fps' %fps)

			prompt_restart()
			return

		# prompt to resume or quite every x generations
		if not i < generation_limit:

			resume = '%s generations! Keep going? (y/n)' %generation_limit
			if input(resume).lower() == 'n':

				print('%s generations!' %i)
				prompt_restart()
				return

			else:

				generation_limit += GENERATION_INCREMENT		

		i += 1

# main loop
loop()