# Module that holds the functions and classes to build the tree
from driver import process_file
import operator

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

    def __init__(self, column, eval_method, threshold="=="):
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

if __name__ == '__main__':
    # data = process_file()[1:]   # omitting the column headers
    # t_rows, f_rows = partition(data, 1, 'high')
    q = Query(2, "==", 'high')
    # If column 2 == 'high'?
    test_data = [[1 ,0.5, 'high', 'False'],
                 [2 , 0.7, 'low', 'True'],
                 [3 ,0.4, 'mdeium', 'False'],
                 [4 , 0.8, 'high','True']
                ]
    for i in test_data:
        print(i)
        print(q.perform(i))

    #print(partition(test_data, q))
