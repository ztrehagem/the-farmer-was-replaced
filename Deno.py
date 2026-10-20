import Geo
import Math

_dir_map_x = { 1: East, -1: West }
_dir_map_y = { 1: North, -1: South }

def _move(dir, store):
	if not move(dir):
		return False
	if get_entity_type() == Entities.Apple:
		store["apple"] = measure()
		store["length"] += 1
	return True

def _move_to_x(x1, store):
	x0 = get_pos_x()
	dx = x1 - x0
	dir = _dir_map_x[Math.sign(dx)]
	for i in range(abs(dx)):
		if not _move(dir, store):
			return False
	return True

def _move_to_y(y1, store):
	y0 = get_pos_y()
	dy = y1 - y0
	dir = _dir_map_y[Math.sign(dy)]
	for i in range(abs(dy)):
		if not _move(dir, store):
			return False
	return True

def _enter(ws, store):
	w = Math.ceil(store["length"] // ws)
	for x in range(w):
		if x % 2 == 0:
			if not _move_to_y(ws - 1, store):
				return False
		else:
			if not _move_to_y(1, store):
				return False
		if not _move(East, store):
			return False
	return True

def _exit(ws, store):
	if not _move_to_x(ws - 1, store):
		return False
	if not _move_to_y(0, store):
		return False
	if not _move_to_x(0, store):
		return False
	return True
	
def _zigzag(ws, store):
	x = get_pos_x()
	while x < ws - 1:
		if x % 2 == 0:
			if not _move_to_y(ws - 1, store):
				return False
		else:
			if not _move_to_y(1, store):
				return False
		if not _move(East, store):
			return False
		x = get_pos_x()
	if not _move_to_y(0, store):
		return False
	if not _move_to_x(0, store):
		return False
	return True
			
def _main(ws):
	store = { "length": 1, "apple": measure() }
	
	while store["length"] < ws * ws / 3:
		if not _enter(ws, store):
			return
		if Geo.is_inside(store["apple"], ((ws - 1, 1), (1, ws - 1))):
			ax, ay = store["apple"]
			if not _move_to_y(ay, store):
				return
			if not _move_to_x(ax, store):
				return
		else:
			while True:
				x = get_pos_x()
				rect = ((x, 1), (ws - x - 1, ws - 1))
				if not Geo.is_inside(store["apple"], rect):
					break
				ax, ay = store["apple"]
				if not _move_to_y(ay, store):
					return
				if not _move_to_x(ax, store):
					return
				if not _move(East, store):
					return
		if not _exit(ws, store):
			return

	while True:
		if not _zigzag(ws, store):
			return
		
def run(ws = get_world_size()):
	clear()
	ws = min(ws, get_world_size())
	ws = ws - (ws % 2)
	set_world_size(ws)
	change_hat(Hats.Dinosaur_Hat)
	_main(ws)
	change_hat(Hats.Straw_Hat)