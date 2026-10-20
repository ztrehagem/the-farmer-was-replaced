import Maze
import MazeMaster
import Sunflower

clear()

while True:
	Sunflower.run_until_over(12000)
	#Maze.run()
	ws = get_world_size()
	def do_drone(origin):
		MazeMaster.run(origin, 16)
	drones = list()
	drones.append(spawn_drone(do_drone, (0, 0)))
	drones.append(spawn_drone(do_drone, (ws // 2, 0)))
	drones.append(spawn_drone(do_drone, (0, ws // 2)))
	drones.append(spawn_drone(do_drone, (ws // 2, ws // 2)))
	for drone in drones:
		wait_for(drone)