import Pumpkin
import PumpkinMaster
import Math
import Sunflower

clear()

while True:
	Sunflower.run_until_over(3000)
	
	ws = get_world_size()
	rect = ((0, 0), (ws, ws))
	Pumpkin.run(rect)