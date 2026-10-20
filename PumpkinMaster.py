import Drone
import Farm
import Math

def _init(rect):
	mem = set()

	def do_tile():
		x, y = get_pos_x(), get_pos_y()
		if get_ground_type() != Grounds.Soil:
			till()
		if get_entity_type() != Entities.Pumpkin:
			harvest()
			plant(Entities.Pumpkin)
			Farm.watering(0.6)
		mem.add((x, y))
	
	Drone.do_in_rect(rect, do_tile)
	
	return mem
	
def _check(mem):
	ok = list()
	for pos in mem:
		Drone.move_to(pos)
		while get_entity_type() != Entities.Dead_Pumpkin and not can_harvest() and num_items(Items.Fertilizer) > 32:
			use_item(Items.Fertilizer)
		if get_entity_type() == Entities.Dead_Pumpkin:
			plant(Entities.Pumpkin)
		elif can_harvest():
			ok.append(pos)
	for pos in ok:
		mem.remove(pos)

def run(rect):
	origin, volume = rect
	x0, y0 = origin
	w, h = volume	
	rect1 = ((x0, y0), (w // 2, h))
	rect2 = ((x0 + w // 2, y0), (w // 2, h))

	def do_drone(rect):
		mem = _init(rect)
		while len(mem) != 0:
			_check(mem)
			
	drone = spawn_drone(do_drone, rect1)
	do_drone(rect2)
	wait_for(drone)
	harvest()

def _true():
	return True

def run_drones(while_condition = _true):
	ws = get_world_size()
	rects = []
	if ws < 12:
		size = Math.min(6, ws)
		rects.append(((0, 0), (size, size)))
	elif ws == 12:
		rects.append(((0, 0), (6, 6)))
		rects.append(((6, 6), (6, 6)))
	else:
		l = (ws + 1) // 7
		for i in range(l):
			for j in range(l):
				rects.append(((i * 7, j * 7), (6, 6)))
	
	def run_drone(rect):
		while while_condition():
			run(rect)
	
	drones = []	
	for i in range(min(len(rects), Drone.get_max_drones()) - 1, -1, -1):
		rect = rects[i]
		if i > 0:
			drone = spawn_drone(run_drone, rect)
			drones.append(drone)
		else:
			run_drone(rect)
	for drone in drones:
		wait_for(drone)