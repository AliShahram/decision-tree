# Module that holds the functions and classes to build the tree
from driver import process_file
import operator
import math
from input_tree import *

class Leaf:
    def __init__(self, rows):
        self.predictions = val_freq(rows)

class DecisionNode:
    def __init__(self, query, true_branch, false_branch):
        self.query = query
        self.true_branch = true_branch
        self.false_branch = false_branch

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
        return("Is {} {} {}".format(
                            header[self.column], 
                            self.eval_method,
                            self.threshold))

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

def build_tree(rows):
    gain, query = best_query(rows)

    # base case
    if gain == 0:
        return Leaf(rows)

    true_rows, false_rows = partition(rows, query)
    
    true_branch = build_tree(true_rows)
    false_branch = build_tree(false_rows)

    return DecisionNode(query, true_branch, false_branch)

def build_tree_alt(rows):
    # consider one column
    # get all the decision
    # if the info
    pass 

def classify(row, node):
    if isinstance(node, Leaf):
        return node.predictions

    if node.query.perform(row):
        return classify(row, node.true_branch)
    else:
        return classify(row, node.false_branch)

def print_tree(node, spacing=""):
    
    if isinstance(node, Leaf):
        print(spacing+ "Predict", node.predictions)
        return

    print(spacing+str(node.query))

    print(spacing+ "|--> True:")
    print_tree(node.true_branch, spacing +"  ")

    print(spacing+ "|--> False:")
    print_tree(node.false_branch, spacing+"  ")

def accuracy_test(rows):

    total_accuracy = 0.0
    total_elements = len(rows)

    for i, row in enumerate(rows):
        singled_out = row
        rows.remove(row)
        remaining_rows = rows
        actual_label = row[-1]        
 
        node = build_tree(remaining_rows)
        result = classify(singled_out, node)       
        
        print(result)
        # either 'yes' or 'no' prediction
        if len(result) == 1:
            if actual_label in result:
                total_accuracy += 1
                continue
            else:
                total_accuracy += 0
                continue
        # both 'yes' and 'no' prediction
        else:
            prob_correct = result[actual_label]
            if actual_label == 'yes':
                incorrect_label = 'no'            
                #prob_incorrect = result[incorrect_label]
            else:
                incorrect_label = 'yes'
            prob_incorrect = result[incorrect_label]

            total_prob = prob_correct + prob_incorrect
            accuracy_for_this_test = prob_correct/total_prob
            
        total_accuracy += accuracy_for_this_test

        rows.append(singled_out)

    final_accuracy = (total_accuracy / total_elements)

    return final_accuracy
 
    
if __name__ == "__main__":
    rows, header = file_parsed("dataset/titanic2.txt") 

    accuracy = accuracy_test(rows)
    print("accuracy ", accuracy * 100, "%.")
    
    
