def a_star_search(start,end):
    open_list = []
    close_list = []
    open_list.append(start)
    while len(open_list) > 0:
        current_grid = find_min_gird(open_list)
        open_list.remove(current_grid)
        close_list.append(current_grid)
        neighbors = find_neighbors(current_grid,open_list,close_list)
        for grid in neighbors:
            if grid not in open_list:
                grid.init_grid(current_grid,end)
                open_list.append(grid)
        for grid in open_list:
            if (grid.x == end.x) and (grid.y == end.y):
                return grid
    return None
def find_min_gird(open_list=[]):
    temp_grid = open_list[0]
    for grid in open_list:
        if grid.f < temp_grid.f:
            temp_grid = grid
    return temp_grid
def find_neighbors(grid,open_list=[],close_list=[]):
    grid_list = []
    if is_valid_grid(grid.x,grid.y-1,open_list,close_list):
        grid_list.append(Grid(grid.x,grid.y-1))
    if is_valid_grid(grid.x,grid.y+1,open_list,close_list):
        grid_list.append(Grid(grid.x,grid.y+1))
    if is_valid_grid(grid.x-1,grid.y,open_list,close_list):
        grid_list.append(Grid(grid.x-1,grid.y))
    if is_valid_grid(grid.x+1,grid.y,open_list,close_list):
        grid_list.append(Grid(grid.x+1,grid.y))
    return grid_list
def is_valid_grid(x,y,open_list=[],close_list=[]):
    if y < 0 or y >= len(MAZE) or x < 0 or x >= len(MAZE[0]):
        return False
    if MAZE[y][x] == 1:
        return False
    if contain_grid(open_list,x,y):
        return False
    if contain_grid(close_list,x,y):
        return False
    return True
def contain_grid(grids,x,y):
    for grid in grids:
        if (grid.x == x) and (grid.y == y):
            return True
    return False
class Grid:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.f = 0
        self.g = 0
        self.h = 0
        self.parent = None
    def init_grid(self,parent,end):
        self.parent = parent
        if parent is not None:
            self.g = parent.g+1
        else:
            self.g = 1
        self.h = abs(self.x - end.x)+abs(self.y - end.y)
        self.f = self.g+self.h

import numpy as np
from random import randint, choice
from enum import Enum
class MAP_ENTRY_TYPE(Enum):
	MAP_EMPTY = 0,
	MAP_BLOCK = 1,

class WALL_DIRECTION(Enum):
	WALL_LEFT = 0,
	WALL_UP = 1,
	WALL_RIGHT = 2,
	WALL_DOWN = 3,
class Map():
	def __init__(self, width, height):
		self.width = width
		self.height = height
		self.map = [[0 for x in range(self.width)] for y in range(self.height)]
	def resetMap(self, value):
		for y in range(self.height):
			for x in range(self.width):
				self.setMap(x, y, value)
	def setMap(self, x, y, value):
		if value == MAP_ENTRY_TYPE.MAP_EMPTY:
			self.map[y][x] = 0
		elif value == MAP_ENTRY_TYPE.MAP_BLOCK:
			self.map[y][x] = 1
	def isVisited(self, x, y):
		return self.map[y][x] != 1
	def showMap(self):
		for row in self.map:
			s = ''
			for entry in row:
				if entry == 0:
					s += ' 0'
				elif entry == 1:
					s += ' 1'
				else:
					s += ' X'
			print(s)
def randomPrim(map1, width, height):
	startX, startY = (randint(0, width-1), randint(0, height-1))
	map1.setMap(2*startX+1, 2*startY+1, MAP_ENTRY_TYPE.MAP_EMPTY)
	checklist = []
	checklist.append((startX, startY))
	while len(checklist):
		entry = choice(checklist)	
		if not checkAdjacentPos(map1, entry[0], entry[1], width, height, checklist):
			checklist.remove(entry)
def doRandomPrim(map1):
	map1.resetMap(MAP_ENTRY_TYPE.MAP_BLOCK)	
	randomPrim(map1, (map1.width-1)//2, (map1.height-1)//2)
def checkAdjacentPos(map, x, y, width, height, checklist):
	directions = []
	if x > 0:
		if not map.isVisited(2*(x-1)+1, 2*y+1):
			directions.append(WALL_DIRECTION.WALL_LEFT)
				
	if y > 0:
		if not map.isVisited(2*x+1, 2*(y-1)+1):
			directions.append(WALL_DIRECTION.WALL_UP)

	if x < width -1:
		if not map.isVisited(2*(x+1)+1, 2*y+1):
			directions.append(WALL_DIRECTION.WALL_RIGHT)
		
	if y < height -1:
		if not map.isVisited(2*x+1, 2*(y+1)+1):
			directions.append(WALL_DIRECTION.WALL_DOWN)
		
	if len(directions):
		direction = choice(directions)
		#print("(%d, %d) => %s" % (x, y, str(direction)))
		if direction == WALL_DIRECTION.WALL_LEFT:
				map.setMap(2*(x-1)+1, 2*y+1, MAP_ENTRY_TYPE.MAP_EMPTY)
				map.setMap(2*x, 2*y+1, MAP_ENTRY_TYPE.MAP_EMPTY)
				checklist.append((x-1, y))
		elif direction == WALL_DIRECTION.WALL_UP:
				map.setMap(2*x+1, 2*(y-1)+1, MAP_ENTRY_TYPE.MAP_EMPTY)
				map.setMap(2*x+1, 2*y, MAP_ENTRY_TYPE.MAP_EMPTY)
				checklist.append((x, y-1))
		elif direction == WALL_DIRECTION.WALL_RIGHT:
				map.setMap(2*(x+1)+1, 2*y+1, MAP_ENTRY_TYPE.MAP_EMPTY)
				map.setMap(2*x+2, 2*y+1, MAP_ENTRY_TYPE.MAP_EMPTY)
				checklist.append((x+1, y))
		elif direction == WALL_DIRECTION.WALL_DOWN:
			map.setMap(2*x+1, 2*(y+1)+1, MAP_ENTRY_TYPE.MAP_EMPTY)
			map.setMap(2*x+1, 2*y+2, MAP_ENTRY_TYPE.MAP_EMPTY)
			checklist.append((x, y+1))
		return True
	else:
		# if not find any unvisited adjacent entry
		return False
def run(WIDTH,HEIGHT):
	map1 = Map(WIDTH, HEIGHT)
	doRandomPrim(map1)
	asd = map1.map
	asd[0][0] = 0
	asd[1][0] = 0
	asd[-1][-1] = 0
	asd[-2][-1] = 0
	return asd

import matplotlib.pyplot as plt
import tqdm

import imageio
import os
R,C = int(input("MAZE SIZE(x-odd):")),int(input("MAZE SIZE(y-odd):"))
MAZE = run(R,C)
start_grid = Grid(0,0)
end_grid = Grid(len(MAZE[0])-1,len(MAZE)-1)
result_grid = a_star_search(start_grid,end_grid)
path = []
while result_grid is not None:
    path.append(Grid(result_grid.x,result_grid.y))
    result_grid = result_grid.parent
MAZA = MAZE.copy()
i0 = 0
if not os.path.exists('images'):
	os.mkdir('images')
for i in tqdm.tqdm(path):
    MAZA[i.y][i.x] = 0.5
    plt.imshow(MAZA)
    plt.savefig(f"images/{i0}.jpg")
    i0 += 1
	
def create_gif(image_list, gif_name,duration=0.1):
    frames = []
    for image_name in image_list:
        frames.append(imageio.imread(image_name))
    imageio.mimsave(gif_name, frames, 'GIF', duration=duration)
    return
image_list = [f"images/{i}.jpg" for i in range(len(path))]
gif_name = 'go.gif'
duration = 0.1
create_gif(image_list, gif_name, duration)
def del_files(dir_path):
    if os.path.isfile(dir_path):
        try:
            os.remove(dir_path)
        except BaseException as e:
            print(e)
    elif os.path.isdir(dir_path):
        file_lis = os.listdir(dir_path)
        for file_name in file_lis:
            tf = os.path.join(dir_path, file_name)
            del_files(tf)
del_files('images')
os.rmdir('images')