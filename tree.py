# Module that holds the functions and classes to build the tree
from driver import process_file
import operator
import math
from input_tree import *

def build_tree():
    pass

class Tree:
    def __init__(self):
        pass

class Query():
    """Query is the criteria we use to partition a dataset.

    This class is initiated with a column number, evaluation method
    (i.e., ==, >, <, etc), and the threshold value that
    is used for that query. For example, if the data set looks like the
    following:
        +-------------------+
        |radius|color|label |
        +------+-----+------+
        | 7.0  |green|tennis|
        +------+-----+------+
    and we want to evaluate whether the radius is >=5.0, we will need a Query
    object in the form of Query(0,>=,5.0). This class has a method that will
    evaluate the question for a given row
    """

    def __init__(self, column, threshold, eval_method = "=="):
        self.column = column
        self.eval_method = eval_method
        self.threshold = threshold
    
    def perform(self, sample):
        """Perform the evaluation on this sample based on the query
`       
        Parameters:
        sample: a row in the dataset
        
        Returns:
        result: a boolean indicating whether the sample evaluated the query to
        false or true
        """
        if isinstance(sample[self.column], str):
            # Can't have any >, < operators
            if self.eval_method in [">", "<", ">=", "<="]:
                raise TypeError("Can not evaluate inequality for strings.")
        
        ops = {
            ">":operator.gt,
            "<":operator.lt,
            ">=":operator.ge,
            "<=":operator.le,
            "==":operator.eq
            }
        # Evaluating the (in)equality in the form of sample ? threshold
        if ops[self.eval_method](sample[self.column], self.threshold):
            return True
        else:
            return False

    def __repr__(self):
        print("reprsnt")
        pass



def partition(dataset, query):
    """Partition the dataset into true and false based on the query passed
    
    Parameters:
    dataset: a list of rows to be partitioned
    query: the question/critieria we will evaluate on, a Query() object

    Return:
    two lists containing the true rows and false rows
    """
    true_rows, false_rows = [], []

    for row in dataset:
        if query.perform(row):
            true_rows.append(row)
        else:
            false_rows.append(row)

    return true_rows, false_rows





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

    p = float(len(left)) / (len(left) + len(right))
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
    cur_uncertaintly = entropy(rows)
    num_labels = len(rows[0]) - 1


    for column in range(num_labels):

        samples = set([row[column] for row in rows])        #Finding the unique vals
                                                            #in each column

        for value in samples:
            question = Query(column, value)

            #split the data set

            true_rows, false_rows = partition(rows, question)

            #If the partition doesn't work 
            if len(true_rows) == 0 or len(false_rows) == 0:
                continue
            
            #calculate the information gain of the split
            gain = information_gain(true_rows, false_rows, cur_uncertaintly)
            if gain >= final_gain:
                final_gain = gain
                final_query = question

    return final_gain, final_query




if __name__ == "__main__":
    rows, header = file_parsed("pets.txt")

        
   
    






"""
if __name__ == '__main__':
    # data = process_file()[1:]   # omitting the column headers
    # t_rows, f_rows = partition(data, 1, 'high')
    q = Query(1, ">", 0.6)
    test_data = [[1,0.5, 'False'],
                 [2, 0.7, 'True'],
                [3,0.4, 'False'],
                [4, 0.8, 'True']
                ]
    for i in test_data:
        print(i)
        print(q.perform(i))

    print(partition(test_data, q))

    """
