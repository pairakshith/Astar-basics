import pygame
import math
from queue import PriorityQueue
WIDTH=800
WIN = pygame.display.set_mode((WIDTH,WIDTH))
pygame.display.set_caption("A star path finding algorithm")
RED=(255,0,0)
green=(0,255,0)
blue=(0,0,255)
yellow=(255,255,0)
white=(255,255,255)
black=(0,0,0)
purple=(128,0,128)
orange=(255,165,0)
grey=(128,128,128)
turquoise=(64,224,208)

class Spot:
	def __init__(self,row,col,width,total_rows):
		self.row=row
		self.col=col
		self.x=row*width
		self.y=col*width
		self.color=white
		self.n=[]
		self.width=width
		self.total_rows=total_rows

	def get_pos(self):
		return self.row, self.col

	def is_closed(self):
		return self.color==RED

	def is_open(self):
		return self.color==green

	def is_barrier(self):
		return self.color==black

	def is_start(self):
		return self.color == orange

	def is_finish(self):
		return self.color == turquoise

	def reset(self):
		self.color = white


	def make_closed(self):
		self.color=RED

	def make_open(self):
		self.color=green

	def make_barrier(self):
		self.color=black

	def make_start(self):
		self.color = orange

	def make_finish(self):
		self.color = turquoise

	def make_path(self):
		self.color = purple

	def draw(self, win):
		pygame.draw.rect(win,self.color,(self.x, self.y, self.width, self.width))	

	def update_n(self,grid):
		self.n=[]
		if self.row<self.total_rows-1 and not grid[self.row+1][self.col].is_barrier(): #down
			self.n.append(grid[self.row+1][self.col])

		if self.row>0 and not grid[self.row-1][self.col].is_barrier(): #up
			self.n.append(grid[self.row-1][self.col])

		if self.col<self.total_rows-1 and not grid[self.row][self.col+1].is_barrier(): #right
			self.n.append(grid[self.row][self.col+1])

		if self.col>0 and not grid[self.row][self.col-1].is_barrier(): #left
			self.n.append(grid[self.row][self.col-1])

	def __lt__(self,other):
		return False

def h(p1,p2):
	x1,y1=p1
	x2,y2=p2
	return abs(x1-x2)+abs(y1-y2)

def reconstruct_path(came_from,current,draw):
	while current in came_from:
		current=came_from[current]
		current.make_path()
		draw()

def algorithm(draw,grid,start,finish):
	count = 0
	open_set=PriorityQueue()
	open_set.put((0,count,start))
	came_from={}
	g_score={spot:float("inf") for row in grid for spot in row}
	g_score[start]=0
	f_score={spot:float("inf") for row in grid for spot in row}
	f_score[start]=h(start.get_pos(),finish.get_pos())

	open_set_hash = {start}

	while not open_set.empty():
		for event in pygame.event.get():
			if event.type==pygame.QUIT:
				pygame.quit()

		current=open_set.get()[2]
		open_set_hash.remove(current)

		if current==finish:
			reconstruct_path(came_from,finish,draw)
			finish.make_finish()
			return True

		for ns in current.n:
			temp_g_score=g_score[current]+1

			if temp_g_score<g_score[ns]:
				came_from[ns]=current
				g_score[ns]=temp_g_score
				f_score[ns]=temp_g_score+h(ns.get_pos(),finish.get_pos())
				if ns not in open_set_hash:
					count+=1
					open_set.put((f_score[ns],count,ns))
					open_set_hash.add(ns)
					ns.make_open()
		draw()

		if current != start:
			current.make_closed()
	return False



def make_grid(rows,width):
	grid=[]
	gap=width//rows
	for i in range(rows):
		grid.append([])
		for j in range(rows):
			spot=Spot(i,j,gap,rows)
			grid[i].append(spot)
	return grid

def draw_grid(win,rows,width):
	gap=width//rows
	for i in range(rows):
		pygame.draw.line(win,grey,(0,i*gap),(width,i*gap))
		for j in range(rows):
			pygame.draw.line(win,grey,(j*gap,0),(j*gap,width))

def draw(win,grid,rows,width):
	win.fill(white)

	for row in grid:
		for spot in row:
			spot.draw(win)

	draw_grid(win,rows,width)
	pygame.display.update()

def get_clicked_pos(pos,rows,width):
	gap=width//rows
	y,x =pos

	row=y//gap
	col=x//gap
	return row,col

def main(win,width):
	ROWS = 40
	grid=make_grid(ROWS,width)

	start = None
	finish = None

	run=True 
	started=False
	while run:
		draw(win,grid,ROWS,width)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run=False

			if pygame.mouse.get_pressed()[0]:
				pos=pygame.mouse.get_pos()
				row,col =get_clicked_pos(pos,ROWS, width)
				spot=grid[row][col]
				if not start and spot !=finish:
					start =spot
					start.make_start()
				elif not finish and spot != start:
					finish =spot
					finish.make_finish()
				elif spot != finish and spot != start:
					spot.make_barrier()

			elif pygame.mouse.get_pressed()[2]:
				pos=pygame.mouse.get_pos()
				row,col =get_clicked_pos(pos,ROWS, width)
				spot=grid[row][col]
				spot.reset()
				if spot == start:
					start = None
				elif spot == finish:
					finish = None

			if event.type == pygame.KEYDOWN:
				if event.key== pygame.K_SPACE and start and finish:
					for row in grid:
						for spot in row:
							spot.update_n(grid)
					algorithm(lambda: draw(win,grid,ROWS,width),grid,start,finish)

				if event.key == pygame.K_c:
					start=None
					finish=None
					grid=make_grid(ROWS,width)

	pygame.quit()
main(WIN,WIDTH)