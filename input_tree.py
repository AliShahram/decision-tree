"""
This is where the input data set is getting parsed
and turned into a binary tree that will be used for 
the decision tree
"""

def file_parsed(input_file):
	output_list = []

	open_input = open(input_file, "r")
	for line in open_input:				#Read each line
		line = line.split()
		output_list.append(line)


	header = ['size', 'color', 'earshape', 'tail', 'iscat']
	return output_list, header
		
