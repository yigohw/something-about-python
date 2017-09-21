import random as rd
import math as mt

def randomop(domain, costfunc, times = 1000, sol = []):
	v = sol
	if len(v) == 0:
		v = [rd.randint(domain[i][0], domain[i][1]) for i in range(len(domain))]

	ret = v
	best = costfunc(v)

	for i in range(times-1):
		v = [rd.randint(domain[i][0], domain[i][1]) for i in range(len(domain))]
		cost = costfunc(v)
		if cost < best:
			best = cost
			ret = v

	return ret

def hillclimbop(domain, costfunc, step = 1, sol = []):
	v = sol
	if len(v) == 0:
		v = [rd.randint(domain[i][0], domain[i][1]) for i in range(len(domain))]

	best = costfunc(v)

	while True:
		neigh = []
		for i in range(len(v)):
			if v[i] - step >= domain[i][0]:
				neigh.append(v[:i] + [v[i] - step] + v[i+1:])
			if v[i] + step <= domain[i][1]:
				neigh.append(v[:i] + [v[i] + step] + v[i+1:])
		
		cost = costfunc(v)
		for i in neigh:
			cur = costfunc(i)
			if cur < cost:
				cost = cur
				v = i

		if cost < best:
			best = cost
		elif cost == best:
			break

	return v

def annealingop(domain, costfunc, T = 1000, cool = 0.99, step = 1, sol = []):
	v = sol
	if len(v) == 0:
		v = [rd.randint(domain[i][0], domain[i][1]) for i in range(len(domain))]

	while T > (1-cool)*step:
		vb = v[:]
		i = rd.randint(0, len(v)-1)
		if rd.random() < 0.5 and vb[i] - step >= domain[i][0]:
			vb[i] -= step
		elif vb[i] + step <= domain[i][1]:
			vb[i] += step

		c = costfunc(v)
		cb = costfunc(vb)

		if cb < c or rd.random() < pow(mt.e, (c-cb)/T):
			v = vb

		T *= cool

	return v

def geneticop(domain, costfunc, size = 50, elite = 0.2, mutprob = 0.2, maxiter = 100, step = 1, sol = []):
	def mutate(v):
		i = rd.randint(0, len(v)-1)
		vec = v[:]
		if rd.random() < 0.5 and vec[i] - step >= domain[i][0]:
			vec[i] -= step
		elif vec[i] + step <= domain[i][1]:
			vec[i] += step

		return v

	def cross(v1, v2):
		i = rd.randint(0, len(v1)-1)
		return v1[:i] + v2[i:]

	pop = []
	for i in range(size):
		v = [rd.randint(domain[i][0], domain[i][1]) for i in range(len(domain))]
		pop.append(v)

	if len(sol) != 0:
		pop[0] = sol

	topelite = int(size * elite)

	for i in range(maxiter):
		scores = [(costfunc(v), v) for v in pop]
		scores.sort()
		ssorted = [v for (c, v) in scores]
		
		pop = ssorted[:topelite]

		while len(pop) < size:
			if rd.random() < mutprob:
				i = rd.randint(0, topelite-1)
				pop.append(mutate(ssorted[i]))

			else:
				i1 = rd.randint(0, topelite-1)
				i2 = rd.randint(0, topelite-1)
				pop.append(cross(ssorted[i1], ssorted[i2]))

	return pop[0]
