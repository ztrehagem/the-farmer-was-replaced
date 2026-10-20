import Drone
import Geo
import Farm

def run(rect):
	tiles = {}
	order = list()

	center = Geo.center_of(rect)
	Drone.move_to(center)
	Farm.safe_plant(Entities.Grass)
	tiles[center] = Entities.Grass
	order.append(center)

	retries = 0
	last_entity = Entities.Grass
	while retries < 3:
		companion = get_companion()
		if companion == None:
			break
		entity, pos = companion
		if (
			Geo.is_inside(pos, rect) and
			not pos in tiles
		):
			Drone.move_to(pos)
			Farm.safe_plant(entity)
			Farm.watering(0.51)
			tiles[pos] = entity
			order.append(pos)
			last_entity = entity
			retries = 0
		else:
			Farm.safe_plant(last_entity)
			retries += 1
	
	for pos in order:
		Drone.move_to(pos)
		while not can_harvest():
			if num_items(Items.Fertilizer):
				use_item(Items.Fertilizer)
		harvest()
		
def _true():
	return True

_l_map = {
	0: (1, 1),
	1: (2, 1),
	2: (2, 2),
	3: (3, 3),
	4: (4, 4),
	5: (4, 4),
	6: (4, 4),
}	

def run_drones(while_condition = _true):
	ws = get_world_size()
	lx, ly = _l_map[num_unlocked(Unlocks.Megafarm)]
	w, h = ws // lx, ws // ly
	rects = []
	for i in range(lx):
		for j in range(ly):
			rects.append(((i * w, j * h), (w, h)))
	
	def run_drone(rect):
		while while_condition():
			run(rect)
	
	drones = []
	for i in range(min(len(rects), Drone.get_max_drones())):
		rect = rects[i]
		drone = spawn_drone(run_drone, rect)
		if drone != None:
			drones.append(drone)
		else:
			run_drone(rect)
	for drone in drones:
		wait_for(drone)