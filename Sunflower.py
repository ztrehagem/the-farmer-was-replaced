import Drone
import Farm

def create_mem():
	mem = {}
	for size in range(7, 16, 1):
		mem[size] = list()
	return mem

def _init_single(rect, mem):
	def do_tile():
		pos = get_pos_x(), get_pos_y()
		if get_ground_type() != Grounds.Soil:
			till()
		if get_entity_type() != Entities.Sunflower:
			harvest()
			plant(Entities.Sunflower)
		size = measure()
		mem[size].append(pos)
	Drone.do_in_rect(rect, do_tile)

def _consume_single(mem, size):
	pos_list = mem[size]
	for pos in pos_list:
		Drone.move_to(pos)
		while not can_harvest():
			pass
		harvest()

def run(rect):
	mem = create_mem()
	_init_single(rect, mem)
	for size in range(15, 6, -1):
		_consume_single(mem, size)

def run_drones(rect):
	origin, volume = rect
	x0, y0 = origin
	w, h = volume
	md = Drone.get_max_drones()
	w_single = w // md

	def init_single(rect):
		def do_tile():
			if get_ground_type() != Grounds.Soil:
				till()
			if get_entity_type() != Entities.Sunflower:
				harvest()
				plant(Entities.Sunflower)
				Farm.watering(0.51)
		Drone.do_in_rect(rect, do_tile)

	drones = []
	for i in range(md):
		rect = ((0 + i * w_single, 0), (w_single, h))
		drone = spawn_drone(init_single, rect)
		if drone != None:
			drones.append(drone)
		else:
			init_single(rect)
	for drone in drones:
		wait_for(drone)
		
	def consume_single(rect, size):
		def do_tile():
			if measure() == size:
				while not can_harvest():
					pass
				harvest()
		Drone.do_in_rect(rect, do_tile)
	
	for size in range(15, 6, -1):
		drones = []
		for i in range(md):
			rect = ((0 + i * w_single, 0), (w_single, h))
			drone = spawn_drone(consume_single, rect, size)
			if drone != None:
				drones.append(drone)
			else:
				consume_single(rect, size)
		for drone in drones:
			wait_for(drone)

def run_until_over(num):
	while num_items(Items.Power) < num:
		ws = get_world_size()
		rect = ((0, 0), (ws, ws))
		if num_unlocked(Unlocks.Megafarm) == 0:
			run(rect)
		else:
			run_drones(rect)