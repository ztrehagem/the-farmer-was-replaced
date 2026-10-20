def every(list, fn):
	result = True
	for e in list:
		if not fn(e):
			result = False
	return result