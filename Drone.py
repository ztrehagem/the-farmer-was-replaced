import Math

def get_max_drones():
	if num_unlocked(Unlocks.Megafarm) == 0:
		return 1
	return max_drones()

def move_to(pos):
	to_x, to_y = pos
	x, y = get_pos_x(), get_pos_y()
	dx, dy = to_x - x, to_y - y
	ws = get_world_size()
	
	if Math.abs(dx) <= ws // 2:
		sign = Math.sign(dx)
		for i in range(0, dx, sign):
			if sign > 0:
				if not move(East):
					return False
			else:
				if not move(West):
					return False
	else:
		sign = Math.sign(dx) * -1
		dx = (ws - Math.abs(dx)) * sign
		for i in range(0, dx, sign):
			if sign > 0:
				if not move(East):
					return False
			else:
				if not move(West):
					return False
	if Math.abs(dy) <= ws // 2:
		sign = Math.sign(dy)
		for i in range(0, dy, sign):
			if sign > 0:
				if not move(North):
					return False
			else:
				if not move(South):
					return False
	else:
		sign = Math.sign(dy) * -1
		dy = (ws - Math.abs(dy)) * sign
		for i in range(0, dy, sign):
			if sign > 0:
				if not move(North):
					return False
			else:
				if not move(South):
					return False
	return True

def do_in_rect(rect, fn):
	origin, volume = rect
	x0, y0 = origin
	w, h = volume
	
	move_to(origin)
	
	for dx in range(w):
		for dy in range(h):
			fn()
			if dy == h - 1:
				continue
			if dx % 2 == 0:
				move(North)
			else:
				move(South)
		if dx == w - 1:
			continue
		move(East)
