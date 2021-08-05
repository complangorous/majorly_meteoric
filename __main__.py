# top-level script

import pandas as pd
from read_data import get_meteor_data

def find_avg_mass(mass_col):
    header = '\n########################\n\n'
    # calculate number of null entries
    num_nulls = len(mass_col) - len(mass_col.dropna())
    # calculate average mass, round to nearest hundredth
    avg_mass = round(mass_col.mean(), 2)
    text = "{0}{1} null entries were detected\nAverage mass of non-null falls: {2}".format(header, num_nulls, avg_mass)
    print(text)
    return avg_mass


def main():
    # ingest meteor data
    df = get_meteor_data()

    # caulcate and display, and retrieve the average mass
    avg_mass = find_avg_mass(df['mass'])

    # determine the year with the highest number of falls
    

if __name__ == '__main__':
    main()
