import Macro

hay = (
	get_cost(Unlocks.Speed)[Items.Hay] +
	get_cost(Unlocks.Expand)[Items.Hay] +
	get_cost(Unlocks.Plant)[Items.Hay]
)
Macro.simple_grass(hay)
unlock(Unlocks.Speed)
unlock(Unlocks.Expand)
unlock(Unlocks.Plant)

wood = get_cost(Unlocks.Expand)[Items.Wood]
Macro.simple_bush(wood)
unlock(Unlocks.Expand)
wood = get_cost(Unlocks.Speed)[Items.Wood]
Macro.simple_bush(wood)
unlock(Unlocks.Speed)
wood = get_cost(Unlocks.Carrots)[Items.Wood]
Macro.simple_bush(wood)
unlock(Unlocks.Carrots)

cost = get_cost(Unlocks.Speed)
Macro.simple_carrot(cost[Items.Carrot])
Macro.simple_bush(cost[Items.Wood])
unlock(Unlocks.Speed)

cost = get_cost(Unlocks.Expand)
Macro.simple_carrot(cost[Items.Carrot])
Macro.simple_bush(cost[Items.Wood])
unlock(Unlocks.Expand)

cost = get_cost(Unlocks.Trees)
Macro.simple_carrot(cost[Items.Carrot])
Macro.simple_bush(cost[Items.Wood])
unlock(Unlocks.Trees)

cost = get_cost(Unlocks.Expand)
Macro.simple_carrot(cost[Items.Carrot])
Macro.simple_tree(cost[Items.Wood])
unlock(Unlocks.Expand)

cost = get_cost(Unlocks.Watering)
Macro.simple_tree(cost[Items.Wood])
unlock(Unlocks.Watering)

cost = get_cost(Unlocks.Sunflowers)
Macro.simple_carrot(cost[Items.Carrot])
unlock(Unlocks.Sunflowers)

Macro.sunflower(1000)

cost = get_cost(Unlocks.Fertilizer)
Macro.simple_tree(cost[Items.Wood])
unlock(Unlocks.Fertilizer)

cost = get_cost(Unlocks.Pumpkins)
Macro.simple_carrot(cost[Items.Carrot])
Macro.simple_tree(cost[Items.Wood])
unlock(Unlocks.Pumpkins)

cost = get_cost(Unlocks.Expand)
Macro.simple_pumpkin(cost[Items.Pumpkin])
unlock(Unlocks.Expand)

cost = get_cost(Unlocks.Polyculture)
Macro.simple_pumpkin(cost[Items.Pumpkin])
unlock(Unlocks.Polyculture)

Macro.sunflower(1000)

cost = get_cost(Unlocks.Speed)
Macro.single_polyculture(0, 0, cost[Items.Carrot])
unlock(Unlocks.Speed)

cost = get_cost(Unlocks.Watering)
Macro.single_polyculture(0, 0, cost[Items.Wood])
unlock(Unlocks.Watering)

cost = get_cost(Unlocks.Speed)
Macro.single_polyculture(0, 0, cost[Items.Carrot])
unlock(Unlocks.Speed)

while (
	num_unlocked(Unlocks.Grass) < 5 or
	num_unlocked(Unlocks.Trees) < 5 or
	num_unlocked(Unlocks.Carrots) < 5 or
	num_unlocked(Unlocks.Pumpkins) < 5
):
	Macro.once_polyculture()
	unlock(Unlocks.Carrots)
	unlock(Unlocks.Grass)
	unlock(Unlocks.Trees)
	unlock(Unlocks.Pumpkins)
	unlock(Unlocks.Watering)

for i in range(3):
	cost = get_cost(Unlocks.Fertilizer)
	Macro.single_polyculture(0, cost[Items.Wood], 0)
	unlock(Unlocks.Fertilizer)
unlock(Unlocks.Mazes)

for i in range(2):
	cost = get_cost(Unlocks.Expand)
	Macro.simple_pumpkin(cost[Items.Pumpkin])
	unlock(Unlocks.Expand)

for i in range(9):
	unlock(Unlocks.Carrots)
	unlock(Unlocks.Grass)
	unlock(Unlocks.Trees)
	unlock(Unlocks.Pumpkins)
	unlock(Unlocks.Watering)
	
cost = get_cost(Unlocks.Cactus)
Macro.simple_pumpkin(cost[Items.Pumpkin])
unlock(Unlocks.Cactus)

cost = get_cost(Unlocks.Megafarm)
Macro.get_gold(cost[Items.Gold])
unlock(Unlocks.Megafarm)
unlock(Unlocks.Megafarm)

for i in range(3):
	cost = get_cost(Unlocks.Dinosaurs)
	Macro.get_cactus(cost[Items.Cactus])
	unlock(Unlocks.Dinosaurs)

for i in range(2):
	cost = get_cost(Unlocks.Polyculture)
	Macro.get_bone(cost[Items.Bone])
	unlock(Unlocks.Polyculture)

for i in range(2):
	cost = get_cost(Unlocks.Mazes)
	Macro.get_cactus(cost[Items.Cactus])
	unlock(Unlocks.Mazes)

cost = get_cost(Unlocks.Leaderboard)
Macro.get_bone(cost[Items.Bone])
Macro.get_gold_parallel(cost[Items.Gold])
unlock(Unlocks.Leaderboard)

