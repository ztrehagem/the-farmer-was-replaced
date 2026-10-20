import Geo
import Math

def _move_to_y(y, store):
	apple_pos, length = store

	y0 = get_pos_y()
	dy = y - y0
	dir = {1: North, -1: South}[Math.sign(dy)]

	for _ in range(abs(dy)):
		if not move(dir):
			return None
		if get_entity_type() == Entities.Apple:
			apple_pos = measure()
			length += 1

	return apple_pos, length

def _move_to_x(x, store):
	apple_pos, length = store

	x0 = get_pos_x()
	dx = x - x0
	dir = {1: East, -1: West}[Math.sign(dx)]

	for _ in range(abs(dx)):
		if not move(dir):
			return None
		if get_entity_type() == Entities.Apple:
			apple_pos = measure()
			length += 1

	return apple_pos, length

def _main():
	ws = get_world_size()
	bandwidth = ws - 1

	store = measure(), 1

	while True:
		while True:
			x = get_pos_x()

			if x < (ws // 2):
				_, length = store
				# if (max(0, length - ws) // bandwidth) <= x:
				if max(0, (length // bandwidth) - 1) <= x:
					break
			elif x == ws - 1:
				break

			store = _move_to_y([ws - 1, 1][x % 2], store)
			if not store:
				return

			store = _move_to_x(x + 1, store)
			if not store:
				return

		# to get apple
		while True:
			apple_pos, length = store
			apple_pos_x, apple_pos_y = apple_pos
			x = get_pos_x()
			if not Geo.is_inside(apple_pos, ((x, 1), (ws - x - 1, ws - 1))):
				break
			store = _move_to_y(apple_pos_y, store)
			if not store:
				return
			store = _move_to_x(apple_pos_x, store)
			if not store:
				return
			if ws - 2 <= apple_pos_x:
				break
			store = _move_to_x(apple_pos_x + 1, store)
			if not store:
				return

		# exit
		apple_pos, length = store
		apple_pos_x, apple_pos_y = apple_pos
		if (apple_pos_x == ws - 1) and (get_pos_x() < ws - 2):
			if get_pos_y() == 0:
				store = _move_to_y(apple_pos_y, store)
			store = _move_to_x(ws - 2, store)
			store = _move_to_y(apple_pos_y, store)
		store = _move_to_x(ws - 1, store)
		if not store:
			return
		store = _move_to_y(0, store)
		if not store:
			return
		store = _move_to_x(0, store)
		if not store:
			return

def run():
	clear()
	change_hat(Hats.Dinosaur_Hat)
	_main()
	change_hat(Hats.Straw_Hat)
	