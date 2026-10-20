import Drone
import Geo
import Farm

def run(center, target):
	Drone.move_to(center)
	Farm.safe_plant(target)
	Farm.watering(1)

	entity, pos = get_companion()
	Drone.move_to(pos)
	Farm.safe_plant(entity)

	Drone.move_to(center)
	feritilized = False
	while not can_harvest():
		if num_items(Items.Fertilizer) > 32:
			use_item(Items.Fertilizer)
			feritilized = True
	if feritilized:
		use_item(Items.Weird_Substance)
	harvest()
	
def _true():
	return True

def run_drones(target, while_condition = _true):
	ws = get_world_size()
	w, h = ws // 4, ws // 4
	origins = []
	for i in range(4):
		for j in range(4):
			origins.append((i * w, j * h))
			origins.append((i * w + 4, j * h + 4))
	
	def run_drone(rect):
		while while_condition():
			run(rect, target)
	
	drones = []
	for i in range(min(len(origins), Drone.get_max_drones())):
		origin = origins[i]
		drone = spawn_drone(run_drone, origin)
		if drone != None:
			drones.append(drone)
		else:
			run_drone(origin)
	for drone in drones:
		wait_for(drone)