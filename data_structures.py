import operator
import math

def val_freq(rows):
    """This function counts the number of types of 
    examples in a dataset"""
    count = {}
    for row in rows:
        label = row[-1]
            
        if label not in count:
            count[label] = 0 
        count[label] += 1
    return count

class Leaf:
    """A terminal node, contains the occurances of the labels"""
    def __init__(self, rows):
        self.predictions = val_freq(rows)

class DecisionNode:
    """A non-terminal node of the tree, contains true and false 
    childs, and the query"""
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
        init_string = "{} {}".format(self.eval_method, self.threshold)
        final_string = "Is %s "+init_string + str(self.column)

        return final_string
        #return (self.column, "{} {}".format(
        #                    #header[self.column], 
        #                    self.eval_method,
        #                    self.threshold))
