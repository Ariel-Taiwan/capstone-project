import pandas as pd
import os
import sys
from glob import glob


def main():
    input_directory = os.path.dirname(os.path.abspath(__file__)) + '/' + sys.argv[1]
    output_directory = os.path.dirname(os.path.abspath(__file__)) + '/' + sys.argv[2]

    files = glob(input_directory + '/*.csv')
    df = pd.concat((pd.read_csv(file) for file in files), ignore_index=True)

    
    # Read a image info
    df.to_csv(output_directory, index=False)


  


if __name__ == "__main__":
    main()