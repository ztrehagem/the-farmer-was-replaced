import PolycultureMaster
import Sunflower

clear()

while True:
	Sunflower.run_until_over(5000)

	def while_condition():
		return num_items(Items.Power) > 5000

	PolycultureMaster.run_drones(Entities.Tree, while_condition)