class ArrayStack:
	def __init__(self):
		self._data = []

	def __len__(self):
		return len(self._data)

	def __str__(self):
		return '[%s]' % ', '.join(map(str, self._data)) 

	def is_empty(self):
		return len(self._data) == 0

	def push(self, e):
		self._data.append(e)

	def top(self):
		if self.is_empty():
			raise Exception('Stack is empty')
		return self._data[-1]

	def pop(self):
		if self.is_empty():
                        raise Exception('Stack is empty')
                return self._data.pop()

if __name__ == '__main__':
	s = ArrayStack()
	s.push(10)
	s.push(20)
	print s
	print s.top()
	s.push(30)
	print s
	print s.pop()
	print s
