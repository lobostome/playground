from stack import ArrayStack

def is_matched(expr):
	lefty = '({['
	righty = ')}]'
	S = ArrayStack()
	for c in expr:
		if c in lefty:
			S.push(c)
		elif c in righty:
			if S.is_empty():
				return False
			if righty.index(c) != lefty.index(S.pop()):
				return False
	return S.is_empty()

if __name__ == '__main__':
	a = "[(5+x)-(y+z)]"
	print is_matched(a)
	b = "[(5+x)-(y+z]"
	print is_matched(b)
