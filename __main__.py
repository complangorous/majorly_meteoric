# top-level script
from datetime import datetime as dt
import pandas as pd
from utils import get_meteor_data, find_avg_mass, find_year_with_most_falls

def main():
    # beginning of execution time
    start = dt.now()
    print('\n------------------------\nStarted executing at {}\n'.format(start))


    # ingest meteor data
    df = get_meteor_data()

    # caulcate and display, and retrieve the average mass
    avg_mass = find_avg_mass(df['mass'])

    # determine the year with the highest number of falls
    year_with_most_falls = find_year_with_most_falls(df[['id','year']])

    # save results
    results = pd.DataFrame({'answer': [avg_mass, year_with_most_falls],
                            'question': ['average mass', 'year with most falls']})

    results.to_csv('results.csv',sep=',',index=False)

    # end of execution
    end = dt.now()
    print('\n------------------------\nFinished executing at {}\n'.format(end))

    # runtime
    print('Execution time: {}'.format(end - start))

if __name__ == '__main__':
    main()
