# top-level script

import pandas as pd
from utils import get_meteor_data, find_avg_mass, find_year_with_most_falls

def main():

    # ingest meteor data
    df = get_meteor_data()
 
    # caulcate and display, and retrieve the average mass
    avg_mass = find_avg_mass(df['mass'])

    # determine the year with the highest number of falls
    year_with_most_falls = find_year_with_most_falls(df['year'])

    # save results
    results = pd.DataFrame({'answer': [avg_mass, year_with_most_falls],
                            'question': ['average mass', 'year with most falls']})

    results.to_csv('results.csv',sep=',',index=False)


if __name__ == '__main__':
    main()
