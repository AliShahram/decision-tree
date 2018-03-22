import math 
from data_structures import Query, Leaf, DecisionNode

class DecisionTree(object):
    """A Decision tree object builds the classification tree"""
   
    def __init__(self, dataset):
        self.dataset = dataset
        # Assume the first row represents attribute name
        self.header = dataset[0]
        # The remaining dataset w/o the first row
        self.rows = dataset[1:]
        self.tree = self.build_tree(self.rows)

    def partition(self, dataset, query):
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


    def val_freq(self, rows):
        """This function counts the number of types of 
        examples in a dataset
        """

        count = {}   #Stores label as key and the count as value
        for row in rows:
            label = row[-1]
            
            if label not in count:
                count[label] = 0 
            count[label] += 1
        return count

    def entropy(self, rows): 
        """Calculate the impurity in a given dataset"""
        counts = self.val_freq(rows)
        data_entropy = 0.0

        for freq in counts.values():
            data_entropy += (-freq/len(rows)) * math.log(freq/len(rows), 2)

        return data_entropy

    def information_gain(self, left, right, cur_uncertaintly):
        """Calculates the uncertainty of a given node, minus the 
        weighted impurity of two child nodes
        """

        p = float(len(left)) / (len(left) + len(right))
        gain = cur_uncertaintly - p * self.entropy(left) - (1 - p) * self.entropy(right)
        return gain
            
    def best_query(self, rows):
        """
        This function finds the best label to branch the tree
        based on. It uses information gain and entropy to evaluate
        how much the uncertainty is with each division. 
        """

        final_gain = 0
        final_query = None
        cur_uncertaintly = self.entropy(rows)
        num_labels = len(rows[0]) - 1


        for column in range(num_labels):

            samples = set([row[column] for row in rows])        #Finding the unique vals
                                                                #in each column

            for value in samples:
                question = Query(column, value)

                #split the data set

                true_rows, false_rows = self.partition(rows, question)

                #If the partition doesn't work 
                if len(true_rows) == 0 or len(false_rows) == 0:
                    continue
                
                #calculate the information gain of the split
                gain = self.information_gain(true_rows, false_rows, cur_uncertaintly)
                if gain >= final_gain:
                    final_gain = gain
                    final_query = question

        return final_gain, final_query

    def build_tree(self, rows=None):
        """Recursively build the tree, using the best query at each
        level"""        
        rows = rows if rows is not None else self.rows

        gain, query = self.best_query(rows)

        # base case
        if gain == 0:
            return Leaf(rows)

        true_rows, false_rows = self.partition(rows, query)
        
        true_branch = self.build_tree(true_rows)
        false_branch = self.build_tree(false_rows)

        return DecisionNode(query, true_branch, false_branch)

    def classify(self, row, node=None):
        node = node if node is not None else self.tree
        if isinstance(node, Leaf):
            return node.predictions

        if node.query.perform(row):
            return self.classify(row, node.true_branch)
        else:
            return self.classify(row, node.false_branch)

    def _prediction(self, result):
        """Provides the prediction confidence in percentage
        
        Parameters: a dict containing the yes and/or no counts

        Returns: yes and/or no percentage
        """
        if len(result) == 2:
            total = result['yes'] + result['no']
            yes_acc = round(float((result['yes'] / total) * 100),2)
            no_acc = round(float((result['no'] / total) * 100),2)
        
            return {'yes':yes_acc, 'no':no_acc}
        
        elif len(result) == 1:
            try:
                if result['yes']:
                    return {'yes': 100}
            except KeyError:
                return {'no': 100}
        
        else:
            return {}

    def print_tree(self, node=None, spacing=""):
        """Prints the tree in a readable format"""

        node = node if node is not None else self.tree
        
        if isinstance(node, Leaf):
            percents = self._prediction(node.predictions)
            print(spacing+ "Confidence(%) ", percents)
            return
       
        un_query = repr(node.query)
        col_num = int(un_query[-1])
        attr = self.header[col_num]
        to_present = un_query[:-1]
        print(spacing+(to_present % attr) + "?")

        print(spacing+ "|--> True:")
        self.print_tree(node.true_branch, spacing +"    ")

        print(spacing+ "|--> False:")
        self.print_tree(node.false_branch, spacing+"    ")

