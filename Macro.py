import Drone
import Geo
import Math
import Farm
import List
import Pumpkin
import Sunflower
import Polyculture
import Maze
import MazeMaster
import Cactus
import Deno

def simple_grass(num):
	while num_items(Items.Hay) < num:
		while not can_harvest() and get_entity_type() == Entities.Grass:
			pass
		Farm.safe_plant(Entities.Grass)
		
def simple_bush(num):
	while num_items(Items.Wood) < num:
		while not can_harvest() and get_entity_type() == Entities.Bush:
			pass
		Farm.safe_plant(Entities.Bush)
		move(North)
		if get_pos_y() == 0 and num_unlocked(Unlocks.Expand) >= 2:
			move(East)

def simple_carrot(num):
	carrot_cost = get_cost(Entities.Carrot)
	hay, wood = carrot_cost[Items.Hay] * num * 1.25, carrot_cost[Items.Wood] * num * 1.25
	simple_grass(hay)
	if num_unlocked(Unlocks.Trees) > 0:
		simple_tree(wood)
	else:
		simple_bush(wood)
	while num_items(Items.Carrot) < num:
		while not can_harvest() and get_entity_type() == Entities.Carrot:
			pass
		Farm.safe_plant(Entities.Carrot)
		move(North)
		if get_pos_y() == 0:
			move(East)
			
def simple_tree(num):
	while num_items(Items.Wood) < num:
		x, y = get_pos_x(), get_pos_y()
		if (x + y) % 2 == 0:
			while not can_harvest() and get_entity_type() == Entities.Tree:
				pass
			Farm.safe_plant(Entities.Tree)
		else:
			harvest()
		move(North)
		if get_pos_y() == 0:
			move(East)

def simple_pumpkin(num):
	cost = get_cost(Entities.Pumpkin)
	carrot = cost[Items.Carrot] * num // 2
	if num_unlocked(Unlocks.Polyculture):
		polyculture(0, 0, carrot)
	else:
		simple_carrot(carrot)
	while num_items(Items.Pumpkin) < num:
		Pumpkin.run(((0, 0), (6, 6)))
		
def sunflower(num):
	cost = get_cost(Entities.Sunflower)
	diff = num - num_items(Items.Power) // 6
	carrot = cost[Items.Carrot] * diff
	if num_unlocked(Unlocks.Polyculture):
		polyculture(0, 0, carrot)
	else:
		simple_carrot(carrot)
	Sunflower.run_until_over(num)
	
def once_polyculture():
	ws = get_world_size()
	Sunflower.run_until_over(1000)
	Polyculture.run(((0, 0), (ws, ws)))
		
def single_polyculture(hay, wood, carrot):
	ws = get_world_size()
	while (
		num_items(Items.Hay) < hay or
		num_items(Items.Wood) < wood or
		num_items(Items.Carrot) < carrot
	):
		Sunflower.run_until_over(1000)
		Polyculture.run(((0, 0), (ws, ws)))
		
def parallel_polyculture(hay, wood, carrot):
	Sunflower.run_until_over(3000)
	def do_drone(rect):
		while (
			num_items(Items.Hay) < hay or
			num_items(Items.Wood) < wood or
			num_items(Items.Carrot) < carrot
		):
			Polyculture.run(rect)
	ws = get_world_size()
	drones = []
	size = ws // 2
	drones.append(spawn_drone(do_drone, ((0, 0), (size, size))))
	drones.append(spawn_drone(do_drone, ((size, 0), (size, size))))
	drones.append(spawn_drone(do_drone, ((0, size), (size, size))))
	do_drone(((size, size), (size, size)))
	for drone in drones:
		wait_for(drone)

def polyculture(hay, wood, carrot):
	if Drone.get_max_drones() < 4:
		single_polyculture(hay, wood, carrot)
	else:
		parallel_polyculture(hay, wood, carrot)

def get_gold(num):
	while num_items(Items.Gold) < num:
		Sunflower.run_until_over(3000)
		#substance = Maze._get_required_substance() * 300
		#get_substance(substance)
		Maze.run()
		
def get_gold_parallel(num):
	ws = get_world_size()
	while num_items(Items.Gold) < num:
		Sunflower.run_until_over(3000)
		substance = Maze._get_required_substance() * 300
		get_substance(substance)
		def do_drone(origin):
			MazeMaster.run(origin, ws // 2)
		drones = list()
		drones.append(spawn_drone(do_drone, (0, 0)))
		drones.append(spawn_drone(do_drone, (ws // 2, 0)))
		drones.append(spawn_drone(do_drone, (0, ws // 2)))
		do_drone((ws // 2, ws // 2))
		for drone in drones:
			wait_for(drone)
		
def get_cactus(num):
	cost = get_cost(Entities.Cactus)
	pumpkin = cost[Items.Pumpkin] * Math.sqrt(num * 2)
	simple_pumpkin(pumpkin)
	while num_items(Items.Cactus) < num:
		Sunflower.run_until_over(1000)
		Cactus.run()
		
def get_bone(num):
	cost = get_cost(Entities.Apple)
	cactus = cost[Items.Cactus] * Math.sqrt(num * 2)
	get_cactus(cactus)
	while num_items(Items.Bone) < num:
		Sunflower.run_until_over(1000)
		Deno.run(20)
		
def get_substance_(num):
	while num_items(Items.Weird_Substance) < num:
		use_item(Items.Fertilizer)
		while not can_harvest():
			pass
		harvest()

def get_substance(num):
	Sunflower.run_until_over(3000)
	def do_drone(rect):
		while num_items(Items.Weird_Substance) < num:
			Polyculture.run(rect)
	ws = get_world_size()
	drones = []
	size = ws // 2
	drones.append(spawn_drone(do_drone, ((0, 0), (size, size))))
	drones.append(spawn_drone(do_drone, ((size, 0), (size, size))))
	drones.append(spawn_drone(do_drone, ((0, size), (size, size))))
	do_drone(((size, size), (size, size)))
	for drone in drones:
		wait_for(drone)