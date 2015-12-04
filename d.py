import math

__author__ = 'sam <vogelsangersamuel@hotmail.com>, piMoll'

import numpy as np
import matplotlib.pyplot as plt


# noinspection PyPep8Naming
class d(object):
	def __init__(self, *args, **kwargs):
		if len(args) == 0:
			self.data = np.array([[], []])
			self.length = 0
		elif len(args) == 1:
			faces = args[0]
			if faces > 0:
				self.data = np.array([np.arange(faces) + 1, np.ones(faces)])
				self.normalizeExpectancies()
				self.length = faces
			else:
				self.data = np.array([[0], [1]])
				self.length = 1
		elif len(args) == 2:
			self.data = args[0]
			self.length = args[1]
		elif len(args) == 3:
			self.data = np.vstack((args[0], args[1]))
			self.length = args[2]
		elif all(x in kwargs.keys() for x in ['values', 'length']):
			self.data = np.vstack((kwargs.get("values"), kwargs.get("length")))
			self.length = kwargs.get("length")

	def __add__(self, other):
		if isinstance(other, d):
			return self.__addDice(other)
		elif isinstance(other, (int, float)):
			return d(self.data[0] + other, self.data[1], self.length)

	def __radd__(self, other):
		return self + other

	def __mul__(self, other):
		if isinstance(other, int):
			return self.times(other)

	def __rmul__(self, other):
		return self * other

	def __iter__(self):
		return iter(np.swapaxes(self.data, 0, 1))

	def __lt__(self, other):      # TODO
		if isinstance(other, (int, float)):
			return np.where(self.data[0] > other, True, False)
		else:
			raise TypeError

	def __gt__(self, other):
		return      # TODO

	def __le__(self, other):
		return      # TODO

	def __ge__(self, other):
		return      # TODO

	def __str__(self):
		return "dice: " + str(self.data[0])

	def __addDice(self, other):
		newLength = self.length + other.length - 1
		newValues = np.arange(self.values()[0] + other.values()[0], self.values()[-1] + other.values()[-1] + 1)

		newExpectancies = np.zeros((newLength,))
		for i in np.arange(self.length):
			newExpectancies[i:i + other.length] += (self.data[1, i] * other.data[1])
		# newExpectancies = d.normalize(newExpectancies)

		return d(newValues, newExpectancies, newLength)

	def times(self, factor):
		if factor == 0:
			return d(0)
		elif factor == 1:
			return self
		else:
			return self.__addDice(self.times(factor - 1))

	@DeprecationWarning  # Currently not used
	def meanValueWeighted(self):
		return np.average(self.data[0], weights=self.data[1])

	def meanValueAndExpectancy(self):
		index = self.meanIndex()
		index_int = np.floor(index)

		values = self.data[0]
		valueBounds = values[index_int:index_int + 2]
		value = valueBounds[0] + (index % 1) * (valueBounds[1] - valueBounds[0])

		expectancies = self.data[1]
		expectancyBounds = expectancies[index_int:index_int + 2]
		expectancy = expectancyBounds[0] + (index % 1) * (expectancyBounds[1] - expectancyBounds[0])

		return value, expectancy

	def meanAndStdDev(self):
		"""
		Return the weighted average and standard deviation.

		values, weights -- Numpy ndarrays with the same shape.
		"""
		values = self.values()
		weights = self.expectancies()
		average = np.average(values, weights=weights)
		variance = np.average((values - average) ** 2, weights=weights)  # Fast and numerically precise
		return average, math.sqrt(variance)

	def meanIndex(self):
		return np.average(np.arange(self.length), weights=self.data[1])

	def normalizeExpectancies(self):
		self.data[1] = d.normalize(self.data[1])

	@staticmethod
	def normalize(expectancies):
		return expectancies / np.sum(expectancies)

	def plot(self):
		plot(self)

	def values(self):
		return self.data[0]

	def expectancies(self):
		return self.data[1]

	def layer(self, other, weight=1):
		if not isinstance(other, d):
			raise TypeError("Can only layer other dice")

		if self.length > 0:
			minVal = np.min([self.values().min(), other.values().min()])
			maxVal = np.max([self.values().max(), other.values().max()])
		else:
			minVal = np.min(other.values())
			maxVal = np.max(other.values())

		newValues = np.arange(minVal, maxVal + 1)
		newLength = np.max(newValues.shape)
		newExpectancies = np.zeros(newLength)

		if self.length > 0:
			selfIndex = np.where(newValues == self.data[0][0])[0][0]
		otherIndex = np.where(newValues == other.data[0][0])[0][0]

		if self.length > 0:
			newExpectancies[selfIndex:self.length + selfIndex] += (self.expectancies() * weight)
		newExpectancies[otherIndex:other.length + otherIndex] += (other.expectancies() * weight)

		newData = np.vstack((newValues, newExpectancies))
		self.data = newData
		self.length = newLength


def plot(dice):
	xdata = dice.values()
	ydata = dice.expectancies() * 100

	meanVal, meanExp = dice.meanValueAndExpectancy()

	plt.plot(meanVal, meanExp * 100, 'ro')

	plt.plot(xdata, ydata)

	plt.xlabel('dice rolls')
	plt.ylabel('likelihood (in percent)')
	plt.title('DnDice')
	plt.grid(True)

	# plt.savefig("test.png")
	plt.show()


def advantage(dice=d(20)):
	"""
	@:param d dice
	@:return d advantage
	"""
	if isinstance(dice, int):
		dice = d(dice)
	v = dice.expectancies()
	arr = np.ones((dice.length, dice.length)) * v
	arr = np.triu(arr, 0) + np.triu(arr, 1)
	sol = np.dot(v, arr)

	return d(dice.values(), sol, dice.length)

# TODO all this
# def highestNOf(n, dice):
# 	if isinstance(dice, int):
# 		dice = d(dice)
# 	dv = dice.values()
# 	values = n + np.arange(n * dv[0], n * dv[-1] + 1)
# 	for combination in permutation(dv[-1], n):
# 		pass
#
#
# def permutation(m, n):
# 	inds = np.indices((m,) * n)
# 	return inds.reshape(n, -1).T
