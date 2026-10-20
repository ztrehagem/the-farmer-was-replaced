import Drone
import Geo
import List

def _get_required_substance(ws):
	return ws * 2**(num_unlocked(Unlocks.Mazes) - 1)

def _init(substance):
	plant(Entities.Bush)
	use_item(Items.Weird_Substance, substance)

def _walk(maze, drones, from_dir = None):
	pos = get_pos_x(), get_pos_y()
	maze[pos] = {}
	dirs = [North, East, South, West]
	next_dirs = []
	for dir in dirs:
		if dir == from_dir:
			maze[pos][dir] = Geo.next_of(pos, dir)
			continue
		if not can_move(dir):
			continue
		next_pos = Geo.next_of(pos, dir)
		maze[pos][dir] = next_pos
		next_dirs.append(dir)

	def walk_fork(dir):
		child_maze = {}
		child_drones = []
		move(dir)
		reverse_dir = Geo.reverse_of(dir)
		_walk(child_maze, child_drones, reverse_dir)
		move(reverse_dir)
		return child_maze, child_drones

	def walk_self(dir):
		move(dir)
		reverse_dir = Geo.reverse_of(dir)
		_walk(maze, drones, reverse_dir)
		move(reverse_dir)
				
	for i in range(len(next_dirs) - 1, -1, -1):
		dir = next_dirs[i]
		if not num_unlocked(Unlocks.Megafarm):
			walk_self(dir)
		elif i == 0:
			walk_self(dir)
		else:
			drone = spawn_drone(walk_fork, dir)
			if drone != None:
				drones.append(drone)
			else:
				walk_self(dir)

def _merge_maze(dist, source):
	for pos in source:
		dist[pos] = source[pos]

def _merge_drones(maze, drones):
	if num_unlocked(Unlocks.Megafarm) > 0:
		def finished(drone):
			return has_finished(drone)
		while not List.every(drones, finished):
			pass
	while len(drones) > 0:
		next_drones = []
		for drone in drones:
			child_maze, child_drones = wait_for(drone)
			_merge_maze(maze, child_maze)
			for child_drone in child_drones:
				next_drones.append(child_drone)
		drones = next_drones

def _get_cost(start, goal):
	x0, y0 = start
	x1, y1 = goal
	return abs(x1 - x0) + abs(y1 - y0)
	
def _find_insert_index(heads, next_cost):
	length = len(heads)
	for i in range(length):
		pos, cost, chain = heads[i]
		if cost <= next_cost:
			return i
	return length

def _resolve(maze, start, goal):
	heads = list()
	heads.append((start, 0, None))
	walked = set()
	walked.add(start)
	
	while True:
		head = heads.pop()
		pos, cost, chain = head
		for dir in maze[pos]:
			next_pos = maze[pos][dir]
			if next_pos == goal:
				return (next_pos, 0, head)
			if next_pos in walked:
				continue
			walked.add(next_pos)
			next_cost = _get_cost(next_pos, goal)
			index = _find_insert_index(heads, next_cost)
			heads.insert(index, (next_pos, next_cost, head))
		
	return heads[0]

def _update_maze(maze, pos):
	map = maze[pos]
	for dir in [North, East, South, West]:
		if not dir in map and can_move(dir):
			map[dir] = Geo.next_of(pos, dir)

def run(origin, ws = get_world_size(), count = 300):
	x0, y0 = origin
	substance = _get_required_substance(ws)
	if num_items(Items.Weird_Substance) < substance:
		return
	Drone.move_to((x0 + ws // 2, y0 + ws // 2))
	_init(substance)
	
	maze = {}
	drones = []
	_walk(maze, drones)
	_merge_drones(maze, drones)

	for i in range(count, -1, -1):
		goal = measure()
		start = get_pos_x(), get_pos_y()
		chain = _resolve(maze, start, goal)
		path = list()
		while chain != None:
			pos, cost, trailing = chain
			path.append(pos)
			chain = trailing
		for j in range(len(path) - 1, -1, -1):
			pos = path[j]
			Drone.move_to(pos)
			_update_maze(maze, pos)
		if i == 0:
			harvest()
		else:
			use_item(Items.Weird_Substance, substance)