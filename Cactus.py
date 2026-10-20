import Drone
import Geo

def _init_drone(rect):
	store = {}
	def init_tile():
		pos = get_pos_x(), get_pos_y()
		if get_ground_type() != Grounds.Soil:
			till()
		if get_entity_type() != Entities.Cactus:
			harvest()
			plant(Entities.Cactus)
		store[pos] = measure()
	Drone.do_in_rect(rect, init_tile)
	return store

def _init():
	ws = get_world_size()
	md = Drone.get_max_drones()
	w = ws // md
	drones = []
	stores = []
	for i in range(md):
		rect = ((0 + i * w, 0), (w, ws))
		drone = spawn_drone(_init_drone, rect)
		if drone != None:
			drones.append(drone)
		else:
			stores.append(_init_drone(rect))
	for drone in drones:
		stores.append(wait_for(drone))
	store = {}
	for child_store in stores:
		for pos in child_store:
			store[pos] = child_store[pos]
	return store
	
def _sort_row(y, store):
	Drone.move_to((0, y))
	ws = get_world_size()
	for i in range(ws - 1):
		for x in range(ws - 1 - i):
			pos = (x, y)
			next = Geo.next_of(pos, East)
			if store[pos] > store[next]:
				Drone.move_to(pos)
				swap(East)
				store[pos], store[next] = store[next], store[pos]
	result = {}
	for x in range(ws):
		pos = x, y
		result[pos] = store[pos]
	return result

def _sort_rows(store):
	ws = get_world_size()
	md = Drone.get_max_drones()
	h = ws // md
	
	def run_drone(y, h):
		results = []
		for dy in range(h):
			results.append(_sort_row(y + dy, store))
		return results
		
	results = []
	drones = []
	for i in range(md):
		drone = spawn_drone(run_drone, i * h, h)
		if drone != None:
			drones.append(drone)
		else:
			child_results = run_drone(i * h, h)
			for result in child_results:
				results.append(result)
	for drone in drones:
		child_results = wait_for(drone)
		for result in child_results:
			results.append(result)
	for result in results:
		for pos in result:
			store[pos] = result[pos]

def _sort_col(x, store):
	Drone.move_to((x, 0))
	ws = get_world_size()
	for i in range(ws - 1):
		for y in range(ws - 1 - i):
			pos = (x, y)
			next = Geo.next_of(pos, North)
			if store[pos] > store[next]:
				Drone.move_to(pos)
				swap(North)
				store[pos], store[next] = store[next], store[pos]
	result = {}
	for y in range(ws):
		pos = x, y
		result[pos] = store[pos]
	return result

def _sort_cols(store):
	ws = get_world_size()
	md = Drone.get_max_drones()
	w = ws // md
	
	def run_drone(x, w):
		results = []
		for dx in range(w):
			results.append(_sort_col(x + dx, store))
		return results
		
	results = []
	drones = []
	for i in range(md):
		drone = spawn_drone(run_drone, i * w, w)
		if drone != None:
			drones.append(drone)
		else:
			child_results = run_drone(i * w, w)
			for result in child_results:
				results.append(result)
	for drone in drones:
		child_results = wait_for(drone)
		for result in child_results:
			results.append(result)
	for result in results:
		for pos in result:
			store[pos] = result[pos]
			
def run():
	store = _init()
	_sort_rows(store)
	_sort_cols(store)
	while not can_harvest():
		pass
	harvest()