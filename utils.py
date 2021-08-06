import pandas as pd
import boto3

def get_meteor_data():
    """
    Ingest json files from the public s3 bucket 'majorly meteoric' as \
a DataFrame.

    Arguments:
    """
    # access public bucket 'majorly meteoric'
    s3 = boto3.resource('s3').Bucket('majorly-meteoric')

    # iterate through bucket files, turning each into a dataframe.
    # concatenate the results into a single dataframe
    df_list = []
    for file in s3.objects.all():
        df_list.append(pd.read_json("s3://majorly-meteoric/{}".format(file.key)))

    return pd.concat(df_list, axis=0)


def find_avg_mass(mass_col):
    """
    Determine the average mass of a meteor fall within the dataset.

    Arguments:
    mass_col -- pandas Series of mass (int) values
    """
    header = '\n########################\n\nQuestion 1: What is the \
average mass of a meteor fall?\n'
    # calculate number of null entries
    num_nulls = len(mass_col) - len(mass_col.dropna())
    # calculate average mass, round to nearest hundredth
    # NOTE: because pd.mean() excludes null values by default,
    # they do not require explicit handling
    avg_mass = round(mass_col.mean(), 2)

    # format and print results
    text = "{0}{1} null mass entries were detected\nAverage mass of non-null \
falls: {2}".format(header, num_nulls, avg_mass)
    print(text)
    return avg_mass


def find_year_with_most_falls(year_col):
    """
    Determine the calendar year with the highest number of meteor falls.

    Arguments:
    year_col -- pandas Series of year values, formatted as Jan 1st of \
the fall incident's year.
    """
    header = '\n########################\n\nQuestion 2: In what year \
did the highest number of meteors fall?\n'
    # calculate number of null entries
    num_nulls = len(year_col) - len(year_col.dropna())

    # NOTE: given that the original dataset encodes years as full
    # timestamps on the same month/day (Jan 1st of that year), they are
    # logically equivalent to the year in isolation, thus making the
    # following methodology viable

    # using the Series.value_counts() function, convert the 'year'
    # column into a pd.Series where indices are timestamps, and values
    # are their frequency in the original column. the default behavior
    # is to sort them in descending order, making the 0 index the most
    # frequent. take the 0 index and extract its year value.
    year_with_most_falls = year_col.value_counts().index[0][0:4]

    # format and print results
    text = "{0}{1} null year entries were detected\nYear with most \
documented meteor falls: {2}".format(header, num_nulls, year_with_most_falls)
    print(text)
    return year_with_most_falls