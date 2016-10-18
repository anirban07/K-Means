import numpy as np
import random as r
import matplotlib.pyplot as plt

X = np.genfromtxt('digit.txt')
Y = np.genfromtxt('labels.txt', dtype=int)

def main(k, data, labels):
	centers = np.copy(data[np.random.choice(data.shape[0], k, replace=False),:])
	# centers = []
	# for i in range(k):
	# 	centers.append(np.copy(data[i]))
	
	old_point_to_cluster_map = {}
	index_map = None
	cluster_map = None
	i = 0
	while i < 20:
		i += 1
		cluster_map, new_point_to_cluster_map, index_map = assign_cluster(data, centers)
		if old_point_to_cluster_map == new_point_to_cluster_map:
			break
		old_point_to_cluster_map = new_point_to_cluster_map
		centers = update_centers(cluster_map)
	s = sum_of_squares(cluster_map)
	m = mistake_rate(cluster_map, index_map, labels)
	print "number of iterations completed for k = ", k, " is ", i
	print "sum of squares for k = ",k, " is ", s
	print "mistake rate for k = ",k, " is ", m
	print
	return 	s, m


def sum_of_squares(cluster_map):
	s_sum = 0
	for key in cluster_map:
		mu = np.mean(cluster_map[key], axis=0)
		for point in cluster_map[key]:
			# print sum(pow(point - mu))
			s_sum += sum(pow(point - mu, 2))
	return s_sum

def mistake_rate(cluster_map, index_map, labels):
	mistakes = 0
	observation = 0
	for cluster in index_map.keys():
		label_count = {1:0, 3:0, 5:0, 7:0}
		#get label counts
		for point_idx in index_map[cluster]:
			observation += 1
			label_count[labels[point_idx]] += 1
		max_label = 1
		max_count = label_count[1]
		# get max label
		for label in label_count:
			if label_count[label] > max_count:
				max_label = label
				max_count = label_count[label]
		#get mistakes
		for point_idx in index_map[cluster]:
			if labels[point_idx] != max_label:
				mistakes += 1
	return 1.0 * mistakes / observation

def assign_cluster(data, centers):
	cluster_map = {}
	index_cluster_map = {}
	point_to_cluster_map = {}  # stores the index of a point to the cluster it belongs

	for i in range(len(centers)):
		index_cluster_map[i] = []
		cluster_map[i] = []

	for d in range(len(data)):
		closest_center = min([(i[0], np.linalg.norm(data[d]-centers[i[0]])) \
                           			for i in enumerate(centers)], key=lambda t:t[1])[0]
		#closest_center = find_closest_center(data[d], centers)
		point_to_cluster_map[d] = closest_center
		cluster_map[closest_center].append(data[d]) 
		index_cluster_map[closest_center].append(d) # index of the point added to cluster_map
	return cluster_map, point_to_cluster_map, index_cluster_map

def update_centers(cluster_map):
	new_centers = []
	keys = sorted(cluster_map.keys())
	for k in keys:
		new_centers.append(np.mean(cluster_map[k], axis=0))
	return new_centers

# main(2, X, Y)
# main(4, X, Y)
# main(6, X, Y)

s = list()
m = list()
for i in range(1, 11):
	curr_s, curr_m = main(i, X, Y)
	s.append(curr_s)
	m.append(curr_m)
plt.figure(0)
plt.plot(range(1, 11), list(np.array(s)/100000000))
plt.xlabel("K")
plt.ylabel("sum of within group sum of squares 10^8")
plt.figure(1)
plt.plot(range(1, 11), list(np.array(m)))
plt.xlabel("K")
plt.ylabel("mistake rate")
plt.show()