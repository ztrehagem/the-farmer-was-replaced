import Polyculture
import Sunflower

clear()

while True:
	Sunflower.run_until_over(3000)
	#ws = get_world_size()
	#rect = ((0, 0), (ws, ws))
	#Polyculture.run(rect)
	def while_condition():
		return num_items(Items.Power) > 3000
	Polyculture.run_drones(while_condition)
