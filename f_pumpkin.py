import Pumpkin
import PumpkinMaster
import Math
import Sunflower

clear()

while True:
	Sunflower.run_until_over(3000)
	
	ws = get_world_size()
	size = Math.min(6, ws)
	rect = ((0, 0), (size, size))			
	#Pumpkin.run(rect)
	def while_condition():
		return num_items(Items.Power) > 3000
	#Pumpkin.run_drones(while_condition)
	PumpkinMaster.run_drones(while_condition)