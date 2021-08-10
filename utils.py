from datetime import datetime as dt
import pandas as pd
import boto3
import re
import sys

def get_meteor_data(logf):
    """
    Ingest json files from the public s3 bucket 'majorly meteoric' as \
a DataFrame.

    Arguments:
    logf -- str of log file name
    """
    # access public bucket 'majorly meteoric'
    s3 = boto3.resource('s3').Bucket('majorly-meteoric')

    # iterate through bucket files, turning each into a dataframe.
    # concatenate the results into a single dataframe
    df_list = []
    for file in s3.objects.all():
        # if any of the files in s3 are malformed or provoke an
        # exception, log them
        try:
            df_list.append(pd.read_json("s3://majorly-meteoric/{}".format(file.key)))
        except Exception as e:
            with open(logf, 'a') as output:
                output.write('get_meteor_data | {0} | {1}\n'.format(file.key, e))
            pass

    # wrap in constructor to avoid caveat flag
    try:
        df = pd.DataFrame(pd.concat(df_list, axis=0))
        return df
    except Error as e:
        with open(logf, 'a') as output:
            output.write('get_meteor_data | Dataset could not be concatenated in DataFrame\n')
        sys.exit(1)


def find_avg_mass(mass_col, logf):
    """
    Determine the average mass of a meteor fall within the dataset.

    Arguments:
    mass_col -- pandas Series of mass (int) values
    """
    header = '\n########################\n\nQuestion 1: What is the \
average mass of a meteor fall?\n'
    # calculate number of null entries
    num_nulls = len(mass_col) - len(mass_col.dropna())
    with open(logf, 'a') as output:
        output.write('find_avg_mass | {0} entries with null year values removed\n'.format(num_nulls))

    # calculate average mass, round to nearest hundredth
    # NOTE: because pd.mean() excludes null values by default,
    # they do not require explicit handling
    avg_mass = round(mass_col['mass'].mean(), 2)

    # format and print results
    text = "{0}{1} null mass entries were detected\nAverage mass of non-null \
falls: {2}".format(header, num_nulls, avg_mass)
    print(text)
    return avg_mass


def find_year_with_most_falls(year_col, logf):
    """
    Determine the calendar year with the highest number of meteor falls.

    Arguments:
    year_col -- pandas DataFrame of id and year values
    """
    header = '\n########################\n\nQuestion 2: In what year \
did the highest number of meteors fall?\n'
    # calculate number of null entries and log it
    num_nulls = len(year_col) - len(year_col.dropna())
    with open(logf, 'a') as output:
        output.write('find_year_with_most_falls | {0} entries with null year values removed\n'.format(num_nulls))

    # wrap in constructor to avoid caveat flag when applying the
    # extract() function later
    year_col = pd.DataFrame(year_col.dropna())

    def extract_from_year_string(x):
        """
        Take an element of the 'year' column and, if it contains a
valid year string, return it

        Arguments:
        x -- string or bytes object
        """
        pattern = r'.*([0-3][0-9]{3})'
        # if x is a non-null value that can yield a match with
        # 'pattern', then return the matching substring. otherwise,
        # return a null value
        if x:
            m = re.match(pattern, str(x))
            if m:
                return m.group(1)
            else:
                return None
        else:
            return None

    # use the extract() function to return the most year-like
    # substring in every year entry
    year_col['extract_year'] = year_col['year'].apply(extract_from_year_string)

    # identify malformed or indeterminate year data
    #
    # 1) add a year length column for determining if the original year
    #    value follows the standard 23-char format
    year_col['len'] = year_col['year'].apply(lambda x: len(str(x)))
    # 2) isolate all entries with do not have the 23-char format
    defects = year_col.loc[year_col['len'] != 23]
    # 3) of the isolated entries, find all those with an extracted
    #    year value that is null (malformed) or represents a future
    #    year that should logically no be in the dataset
    defects = defects.loc[(pd.isnull(defects['extract_year'])) | (defects['extract_year'] > str(dt.now().year))]
    # 4) for each of the remaining defective entries that meet either
    #    of those criteria, log them with their id
    with open(logf, 'a') as output:
        if not defects.empty:
            for index, row in defects.iterrows():
                output.write('find_year_with_most_falls | malformed year value removed from dataset | id: {0} | val: {1}\n'.format(row['id'], row['extract_year']))

    # drop entries with malformed or indeterminate years from dataset
    defect_indices = defects.index.tolist()
    year_col = pd.DataFrame(year_col.drop(defect_indices, axis=0))

    # using the Series.value_counts() function, convert the
    # 'extract_year' column into a pd.Series where indices are
    # timestamps, and values are their frequency in the original
    # column. the default behavior is to sort them in descending order,
    # making the 0 index the most frequent. take the 0 index and
    # extract its year value.
    year_with_most_falls = year_col['extract_year'].value_counts().index[0]

    # format and print results
    text = "{0}{1} null year entries were detected\nYear with most \
documented meteor falls: {2}".format(header, num_nulls, year_with_most_falls)
    print(text)
    return year_with_most_falls
