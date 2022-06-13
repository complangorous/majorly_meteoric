# top-level script
import os
import time
from datetime import datetime as dt
import pandas as pd
from utils import get_meteor_data, find_avg_mass, find_year_with_most_falls


def main():

    while True:
        # beginning of execution time
        start = dt.now()
        print('\n------------------------\nStarted executing at {}\n'.format(start))

        # create log directory if it does not already exist
        # instantiate empty log file
        if not os.path.exists('logs'):
            os.mkdir('logs')
        logf = 'logs/{}.log'.format(str(start).replace(' ','_').replace('.','_').replace(':', '_'))
        f = open(logf, mode='x')
        f.close()

        # ingest meteor data
        df = get_meteor_data(logf)

        avg_mass = find_avg_mass(df[['id', 'mass']], logf)

        year_with_most_falls = find_year_with_most_falls(df[['id','year']], logf)

        # save results
        results = pd.DataFrame({'answer': [avg_mass, year_with_most_falls],
                                'question': ['average mass', 'year with most falls']})

        results.to_csv('spring_boot_api/complete/results.csv',sep=',',index=False)

        # end of execution
        end = dt.now()
        print('\n------------------------\nFinished executing at {}\n'.format(end))

        # runtime
        print('Logs located in {0}\nExecution time: {1}\n'.format(logf, end - start))

        print('\n------------------------\n')
        # refresh in 24hrs
        # use cron for linux implementation
        time.sleep(86400)


if __name__ == '__main__':
    main()
