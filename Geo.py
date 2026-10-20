def is_inside(pos, rect):
	origin, volume = rect
	x0, y0 = origin
	w, h = volume
	x, y = pos
	
	return (
		x0 <= x and
		x < x0 + w and
		y0 <= y and
		y < y0 + h
	)

def center_of(rect):
	origin, volume = rect
	x0, y0 = origin
	w, h = volume
	
	return (
		x0 + w // 2,
		y0 + h // 2
	)

_next_map = {
	North: (0, 1),
	East: (1, 0),
	South: (0, -1),
	West: (-1, 0)
}

def next_of(pos, dir):
	x, y = pos
	dx, dy = _next_map[dir]
	return x + dx, y + dy
	
_reverse_map = {
	North: South,
	East: West,
	South: North,
	West: East
}
	
def reverse_of(dir):
	return _reverse_map[dir]