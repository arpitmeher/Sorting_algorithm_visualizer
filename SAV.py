import pygame
import random
import math
import pyautogui

pygame.init()          # initializes pygame 

class DrawInformation:
	BLACK = "Black"
	GREEN = "Green"
	RED = "Red"
	BACKGROUND_COLOR = "White"

        # uses three different shades of grey to represent the bars for data 
	GRADIENTS = [
		(100, 100, 100),
		(150, 150, 150),
		(200, 200, 200)
	]

        # selects font for pygame window
	FONT = pygame.font.SysFont("New Roman", 30)     
	LARGE_FONT = pygame.font.SysFont("New Roman", 40)

        # Padding for the pygame window
	SIDE_PAD = 50
	TOP_PAD = 150

        # funtion to beused for pygame
	def __init__(self, width, height, lst):
		self.width = width
		self.height = height

		self.window = pygame.display.set_mode((width, height))
		pygame.display.set_caption("Sorting Algorithm Visualization")
		self.set_list(lst)

        # function to decide the height and width of the bars used to represent different dat values
	def set_list(self, lst):
		self.lst = lst
		self.min_val = min(lst)
		self.max_val = max(lst)
		
                # block width is decided depending upon the no. of data points
		self.block_width = round((self.width - 2*self.SIDE_PAD) / len(lst))

		# height is decided depending upon maximum and minimum value in data
		self.block_height = math.floor((self.height - self.TOP_PAD) / (self.max_val - self.min_val))
		self.start_x = self.SIDE_PAD


# type the static content of the window 
def draw(draw_info, algo_name, ascending):
        # fills the background of window with white color
	draw_info.window.fill(draw_info.BACKGROUND_COLOR)

        # dynamically prints the name of algorithm in use and the order  
	title = draw_info.LARGE_FONT.render(f"{algo_name} - {'Ascending' if ascending else 'Descending'}", 1, draw_info.GREEN)
	draw_info.window.blit(title, (draw_info.width/2 - title.get_width()/2 , 5))

        # prints rest of the static content
	controls = draw_info.FONT.render("R - Reset | SPACE - Start Sorting | A - Ascending | D - Descending", 1, draw_info.BLACK)
	draw_info.window.blit(controls, (draw_info.width/2 - controls.get_width()/2 , 45))

	sorting = draw_info.FONT.render("I - Insertion Sort | B - Bubble Sort | S - Selection Sort", 1, draw_info.BLACK)
	draw_info.window.blit(sorting, (draw_info.width/2 - sorting.get_width()/2 , 75))

	draw_list(draw_info)
	pygame.display.update()


# draw the blocks to represent the data on pygame window
def draw_list(draw_info, color_positions={}, clear_bg=False):
	lst = draw_info.lst

        # clears the background by filling it with white color
	if clear_bg:
		clear_rect = (draw_info.SIDE_PAD, draw_info.TOP_PAD, 
						draw_info.width - draw_info.SIDE_PAD*2, draw_info.height - draw_info.TOP_PAD)
		pygame.draw.rect(draw_info.window, draw_info.BACKGROUND_COLOR, clear_rect)

        # drws the blocks
	for i, val in enumerate(lst):
		x = draw_info.start_x + i * draw_info.block_width
		y = draw_info.height - (val - draw_info.min_val) * draw_info.block_height

                # makes sure that three adjacent block are of different color then the color repeats
		color = draw_info.GRADIENTS[i % 3]

		if i in color_positions:
			color = color_positions[i] 

		pygame.draw.rect(draw_info.window, color, (x, y, draw_info.block_width, draw_info.height))

	if clear_bg:
		pygame.display.update()


# function to generate random data for the list
def generate_starting_list(n, min_val, max_val):
	lst = []

	for _ in range(n):
		val = random.randint(min_val, max_val)
		lst.append(val)

	return lst


# function implementing bubble sort
def bubble_sort(draw_info, ascending=True):
	lst = draw_info.lst

	for i in range(len(lst) - 1):
		for j in range(len(lst) - 1 - i):
			num1 = lst[j]
			num2 = lst[j + 1]

                        # 
			if (num1 > num2 and ascending) or (num1 < num2 and not ascending):
                                # swaps the  j and j+1 elements 
				lst[j], lst[j + 1] = lst[j + 1], lst[j]
				draw_list(draw_info, {j: draw_info.GREEN, j + 1: draw_info.RED}, True)
				yield True

	return lst


# function implementing insertion sort
def insertion_sort(draw_info, ascending=True):
	lst = draw_info.lst

	for i in range(1, len(lst)):
		current = lst[i]

		while True:
			ascending_sort = i > 0 and lst[i - 1] > current and ascending
			descending_sort = i > 0 and lst[i - 1] < current and not ascending

			if not ascending_sort and not descending_sort:
				break

                        # swaps the i and i-1 elements                        
			lst[i] = lst[i - 1]
			i = i - 1
			lst[i] = current
			draw_list(draw_info, {i - 1: draw_info.GREEN, i: draw_info.RED}, True)
			yield True

	return lst


# function implementing selection sort
def selection_sort(draw_info, ascending=True):
        lst = draw_info.lst

        for i in range(len(lst)):
  
                 # Find the minimum element in remaining unsorted array
                 min_idx = i
                 for j in range(i+1, len(lst)):
                         if lst[min_idx] > lst[j] and ascending or lst[min_idx] < lst[j] and not ascending:
                                 min_idx = j
                                 yield True
                                 
                 # Swap the found minimum element withthe first element  
                 lst[i], lst[min_idx] = lst[min_idx], lst[i]
                 draw_list(draw_info, {i: draw_info.GREEN, j: draw_info.RED}, True)
                 
                 

        return lst                   


def main():
	run = True
	clock = pygame.time.Clock()

	# variables to generate a random list
	n = 100
	min_val = 0
	max_val = 100

        # generates the random data for list
	lst = generate_starting_list(n, min_val, max_val)
	
	# selects the size of pygame window according to size of device
	draw_info = DrawInformation(pyautogui.size()[0]*8/10, pyautogui.size()[1]*9/10 - 200, lst)
	
	sorting = False
	ascending = True

        # default sorting algo is set to bubble sort
	sorting_algorithm = bubble_sort
	sorting_algo_name = "Bubble Sort"
	sorting_algorithm_generator = None

	while run:
		clock.tick(240)

		if sorting:
			try:
				next(sorting_algorithm_generator)
			except StopIteration:
				sorting = False
		else:
			draw(draw_info, sorting_algo_name, ascending)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

			if event.type != pygame.KEYDOWN:
				continue

                        # handles all the key down events according to the key pressed
			if event.key == pygame.K_r:
				lst = generate_starting_list(n, min_val, max_val)
				draw_info.set_list(lst)
				sorting = False
			elif event.key == pygame.K_SPACE and sorting == False:
				sorting = True
				sorting_algorithm_generator = sorting_algorithm(draw_info, ascending)
			elif event.key == pygame.K_a and not sorting:
				ascending = True
			elif event.key == pygame.K_d and not sorting:
				ascending = False
			elif event.key == pygame.K_i and not sorting:
				sorting_algorithm = insertion_sort
				sorting_algo_name = "Insertion Sort"
			elif event.key == pygame.K_b and not sorting:
				sorting_algorithm = bubble_sort
				sorting_algo_name = "Bubble Sort"
			elif event.key == pygame.K_s and not sorting:
				sorting_algorithm = selection_sort
				sorting_algo_name = "Selection Sort"	


	pygame.quit()


if __name__ == "__main__":
	main()
