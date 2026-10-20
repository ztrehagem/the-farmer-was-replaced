def sign(n):
	if n < 0:
		return -1
	return 1
		
def abs(n):
	if n < 0:
		return -1 * n
	return n

def max(a, b):
	if a > b:
		return a
	return b
	
def min(a, b):
	if a > b:
		return b
	return a

def floor(n):
	return n // 1

def ceil(n):
	fl = floor(n)
	fraction = n - fl
	if fraction == 0:
		return fl
	return fl + 1
	
def sqrt(n):
	a = 1
	while a ** 2 < n:
		a += 1
	return a + (1 / (2 * a))