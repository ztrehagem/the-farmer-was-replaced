import Math

def watering(threthold):
	diff = max(0, threthold - get_water())
	required = Math.ceil(diff / 0.25)
	num = num_items(Items.Water)
	use = Math.min(num, required)
	if use > 0:
		use_item(Items.Water, use)

def _plant_grass():
	harvest()
	if get_ground_type() != Grounds.Grassland:
		till()
		
def _plant_bush():
	harvest()
	if get_ground_type() != Grounds.Grassland:
		till()
	plant(Entities.Bush)

def _plant_tree():
	harvest()
	if get_ground_type() != Grounds.Grassland:
		till()
	plant(Entities.Tree)

def _plant_carrot():
	harvest()
	if get_ground_type() != Grounds.Soil:
		till()
	plant(Entities.Carrot)

_planter_map = {
	Entities.Grass: _plant_grass,
	Entities.Bush: _plant_bush,
	Entities.Tree: _plant_tree,
	Entities.Carrot: _plant_carrot
}
	
def safe_plant(entity):
	_planter_map[entity]()