import Drone
import Sunflower

clear()

def do_hay():
	while not can_harvest():
		pass
	harvest()
	
def do_bush():
	while not can_harvest():
		pass
	harvest()
	plant(Entities.Bush)
	
def do_carrot():
	while not can_harvest():
		pass
	harvest()
	if get_ground_type() != Grounds.Soil:
		till()
	plant(Entities.Carrot)
	
def do_haytree():
	while not can_harvest():
		pass
	harvest()
	x, y = get_pos_x(), get_pos_y()
	if (x + y) % 2 == 0:
		plant(Entities.Tree)
	
	
while True:
	Sunflower.run_until_over(3000)
	ws = get_world_size()
	Drone.do_in_rect(((0, 0), (2 * ws // 3, ws)), do_haytree)
	Drone.do_in_rect(((2 * ws // 3, 0), (ws // 3, ws)), do_carrot)