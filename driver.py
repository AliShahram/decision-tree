# Receive a dataset file and extract data from it.
import sys

def process_file():
    try:
        data_file = sys.argv[1]
        data_as_list = []
        with open(data_file, "r") as f:
            for line in f:
                data_as_list.append((line.split()))

        return data_as_list
    except Exception as e:
        print(e)
        print("The correct format is `python driver.py data_file.txt`")
if __name__ == '__main__':
    data = process_file()
    print(data)
