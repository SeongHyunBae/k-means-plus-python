import numpy as np
import matplotlib.pyplot as plt

def data_generator():
	x_data = []
	y_data = []

	for i in range(100):
		x = np.random.randn()*100
		y = np.random.randn()*100
		x_data.append(x)
		y_data.append(y)

	return x_data, y_data


class K_means_plus:
	def __init__(self, x_data, y_data, k):
		self.x_data = x_data
		self.y_data = y_data
		self.k = k
		self.clusters = {}
		self.centroid = []

	def get_random_centroid(self):
		return np.random.randint(len(self.x_data))

	def get_distance(self, pt1, pt2):
		return np.sqrt((pt1[0]-pt2[0])**2 + (pt1[1]-pt2[1])**2)

	def select_the_others_centroid(self, first_cen):
		self.centroid.append((self.x_data[first_cen], self.y_data[first_cen]))

		for i in range(self.k-1):
			dis_max = 0
			index_max = 0
			for j in range(len(self.x_data)):
				if j != first_cen and (self.x_data[j], self.y_data[j]) not in self.centroid:
					dis_temp = 0
					for k in self.centroid:
						pt1 = k
						pt2 = (self.x_data[j], self.y_data[j])
						dis_temp += self.get_distance(pt1, pt2)
					if dis_temp > dis_max:
						dis_max = dis_temp
						index_max = j
			self.centroid.append((self.x_data[index_max], self.y_data[index_max]))

	def classify(self):
		for n in range(self.k):
			self.clusters[n] = []

		for i in range(len(self.x_data)):
			dis_min = 999999
			index_min = 0
			if i not in self.centroid:
				for k, j in enumerate(self.centroid):
					pt1 = (self.x_data[i], self.y_data[i])
					pt2 = j
					dis_temp = self.get_distance(pt1, pt2)
					if dis_temp < dis_min:
						dis_min = dis_temp
						index_min = k
				self.clusters[index_min].append(i)

	def reposition_centroid(self):
		for n in range(self.k):
			sum_x = 0
			sum_y = 0
			for i in self.clusters[n]:
				sum_x += self.x_data[i]
				sum_y += self.y_data[i]
			avr_x = sum_x / len(self.clusters[n])
			avr_y = sum_y / len(self.clusters[n])
			self.centroid[n] = (avr_x, avr_y) 


	def execute(self):
		first_cen = self.get_random_centroid()
		self.select_the_others_centroid(first_cen)
		self.classify()
		while True:
			pre_centroid = self.centroid
			self.reposition_centroid()
			self.classify()
			if pre_centroid == self.centroid:
				break
		
if __name__ == '__main__':
	# make data
	x_data, y_data = data_generator()

	k_means_plus = K_means_plus(x_data, y_data, 3)
	k_means_plus.execute()
	
	x_cluster_1 = []
	x_cluster_2 = []
	x_cluster_3 = []
	y_cluster_1 = []
	y_cluster_2 = []
	y_cluster_3 = []
	
	for i in k_means_plus.clusters[0]:
		x_cluster_1.append(x_data[i])
		y_cluster_1.append(y_data[i])

	for i in k_means_plus.clusters[1]:
		x_cluster_2.append(x_data[i])
		y_cluster_2.append(y_data[i])

	for i in k_means_plus.clusters[2]:
		x_cluster_3.append(x_data[i])
		y_cluster_3.append(y_data[i])

	# show clustered data by scatter type
	plt.scatter(x_cluster_1, y_cluster_1, c='blue', marker='o', label='data')
	plt.scatter(x_cluster_2, y_cluster_2, c='red', marker='o', label='data')
	plt.scatter(x_cluster_3, y_cluster_3, c='green', marker='o', label='data')

	plt.tight_layout()
	plt.show()