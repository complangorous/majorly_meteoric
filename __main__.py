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


def find_year_with_most_falls(year_col):
    header = '\n########################\n\n'
    # calculate number of null entries
    num_nulls = len(year_col) - len(year_col.dropna())

    # grab year components of timestamps. since the dataset contains
    # years which fall outside of pandas' nanosecond resolution,
    # this is bypassed by treating the elements as strings rather than
    # proper timestamps

    # drop NaTs from series
    years_col = years_col.dropna()
    # extract YYYY value from timestamp string
    extracted_years = pd.Series([x[0:4] for x in years_col])
    # turn extracted_years into pandas Series of fall counts with
    # fall years as indices, and grab the first index, which is
    # the one with the most frequent value
    year_with_most_falls = extracted_years.value_counts().index[0]

    # format and print results
    text = "{0}{1} null entries were detected\nYear with most documented meteor falls: {2}".format(header, num_nulls, year_with_most_falls)
    print(text)
    return year_with_most_falls


def main():
    # ingest meteor data
    df = get_meteor_data()

    # caulcate and display, and retrieve the average mass
    avg_mass = find_avg_mass(df['mass'])

    # determine the year with the highest number of falls
    

if __name__ == '__main__':
    main()
