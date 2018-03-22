import sys
import random

from dt import DecisionTree

def process_file():
    """Receive a dataset file and extract data from it."""
    try:
        data_file = sys.argv[1]
        data_as_list = []
        with open(data_file, "r") as f:
            for line in f:
                data_as_list.append((line.split()))

        return data_as_list, data_file
    except Exception as e:
        # print(e)
        print("To run the program, enter\n`python driver.py data_file.txt`")
        raise SystemExit

def accuracy_test(rows):
    """Performs cross-out-one validation methods on the dataset passed."""
    # Removing the label
    rows = rows[1:]

    total_accuracy = 0.0
    total_elements = len(rows)

    for i, row in enumerate(rows):
        singled_out = row
        rows.remove(row)
        remaining_rows = rows
        actual_label = row[-1]        
 
        dt = DecisionTree(remaining_rows)
        node = dt.build_tree()
        #node = build_tree(remaining_rows)
        result = dt.classify(singled_out, node)       
        
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
            else:
                incorrect_label = 'yes'
            prob_incorrect = result[incorrect_label]

            total_prob = prob_correct + prob_incorrect
            accuracy_for_this_test = prob_correct/total_prob
            
        total_accuracy += accuracy_for_this_test

        rows.append(singled_out)

    final_accuracy = (total_accuracy / total_elements)

    return final_accuracy

if __name__ == '__main__':
    data, filename = process_file()
    print("This is a decision tree classifier program")
    print("\nThe dataset you've chosen is {}".format(filename))
    print("\nIf you wanted to experiment with a different dataset,")
    print("please quit this program and enter:")
    print("`python driver.py data_file.txt`")
    print("You can choose from any files under the 'dataset/' directory.")

    t = DecisionTree(data)
    t.build_tree()


    print("\n\n...Successfully built a classifer based on the datset")
    print("\nIf you want to print the tree, hit 1. Otherwise, hit `enter`:\n")
    see_tree = input()
    if see_tree == '1':
        print("Classification Tree from {} data".format(filename))
        print("=============================================================")
        t.print_tree() 
        print("=============================================================")


    print("You can randomly choose a data point, and this program can classify")
    print("that data point for you. Hit 1 if you want to test a random example") 
    print("Hit any key to skip.")        
    will_rand = input()

    while True:
        if will_rand != '1':
            break

        chosen = random.randint(1, len(data)-1)
        print("\nExample we will classify ", data[chosen])
        actual = data[chosen][-1]
        print("Actual label on this example is **{}**".format(actual))
        c = t.classify(row=data[chosen])
        print("The prediction based on the classifier is: ") 
        print("Prediction: confidence % =", t._prediction(c))

        print("\n\nEnter 1 if you want to play again. Hit `enter` if you are done.")

        play_again = input()
        if play_again != '1':
            break
        
    print("To check the accuracy test using cross validation, hit 1")
    print("Hit `enter` to skip accuracy testing.")
    acc_test = input()
    if acc_test == '1':
        print("A large dataset takes a few minutes on this part")
        print("Please Wait...")
        result = accuracy_test(data)
        print("The accuracy of {} is: {}%".format(filename, round(result*100,2)))

    print("\nThat's all we have to offer")
    print("If you want to run another dataset, enter: ")
    print("`python driver.py data_file.txt`")
    print("Bye")
