import math
from input_tree import *




def val_freq (rows):
	"""
	This function counts the number of types of 
	examples in a dataset
	"""

	count = {}   #Stores label as key and the count as value
	for row in rows:
		label = row[-1]
		
		if label not in count:
			count[label] = 0 
		count[label] += 1
	return count



def entropy(rows):

	"""
	Calculate the impurity in a given dataset
	"""

	counts = val_freq(rows)

	data_entropy = 0.0

	for freq in counts.values():
		data_entropy += (-freq/len(rows)) * math.log(freq/len(rows), 2)

	return data_entropy



def information_gain(left, right, cur_uncertaintly):
	"""
	Calculates the uncertainty of a given node, minus the 
	weighted impurity of two child nodes
	"""

	p = flot(len(left)) / (len(left) + len(right))
	gain = cur_uncertaintly - p * entropy(left) - (1 - p) * entropy(right)
	return gain
		



def best_query(rows):
	"""
	This function finds the best label to branch the tree
	based on. It uses information gain and entropy to evaluate
	how much the uncertainty is with each division. 
	"""

	final_gain = 0
	final_query = None
	num_labels = len(rows[0]) - 1


	for column in range(num_labels):

		samples = set([row[column] for row in rows])
		print(samples)
			


		









if __name__ == "__main__":
	rows, header = file_parsed("pets.txt")


	best_query(rows)
