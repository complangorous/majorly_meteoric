# top-level script

import pandas as pd
from read_data import get_meteor_data

def main():
    # ingest meteor data
    df = get_meteor_data()
    

if __name__ == '__main__':
    main()
