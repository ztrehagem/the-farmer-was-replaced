import Drone
import Geo

def _get_required_substance():
	return get_world_size() * 2**(num_unlocked(Unlocks.Mazes) - 1)

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
		while num_drones() > 1:
			pass
	while len(drones) > 0:
		next_drones = []
		for drone in drones:
			child_maze, child_drones = wait_for(drone)
			_merge_maze(maze, child_maze)
			for child_drone in child_drones:
				next_drones.append(child_drone)
		drones = next_drones
		
def _resolve(maze, pos, goal, path, from_dir = None):
	x, y = pos
	gx, gy = goal
	if gx == x and gy == y:
		return True
	
	dirs = maze[pos]
	for dir in dirs:
		if dir == from_dir:
			continue
		found = _resolve(maze, dirs[dir], goal, path, Geo.reverse_of(dir))
		if found:
			path.append(dir)
			return True
	return False

def run(count = 300):
	substance = _get_required_substance()
	if num_items(Items.Weird_Substance) < substance:
		return
	ws = get_world_size()
	Drone.move_to((ws // 2, ws // 2))
	_init(substance)
	
	maze = {}
	drones = []
	_walk(maze, drones)
	_merge_drones(maze, drones)

	for i in range(count, -1, -1):
		goal = measure()
		path = list()
		pos = get_pos_x(), get_pos_y()	
		_resolve(maze, pos, goal, path)
		for j in range(len(path) - 1, -1, -1):
			move(path[j])
		if i == 0:
			harvest()
		else:
			use_item(Items.Weird_Substance, substance)