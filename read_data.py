import pandas as pd
import boto3

def main():
    # access public bucket 'majorly meteoric'
    s3 = boto3.resource('s3').Bucket('majorly-meteoric')

    # iterate through bucket files, turning each into a dataframe.
    # concatenate the results into a single dataframe
    df_list = []
    for file in s3.objects.all():
        df_list.append(pd.read_json("s3://majorly-meteoric/{}".format(file.key)))

    return pd.concat(df_list, axis=0)
