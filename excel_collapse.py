#!/usr/bin/env python3

"""A simple python script template.
"""

import os
import glob
import sys
import argparse
import pandas as pd


def main(arguments):
    # parse arguments to get folder path that we need to run on
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('folder_path', help="Folder Path")

    args = parser.parse_args(arguments)

    # grab the folder path
    path = args.folder_path

    # create list to hold all the dataframes we create
    total_dataframes = []

    # iterate over all files in the given folder path
    for filename in glob.glob(os.path.join(path, '*.csv')):
        # read specific columns of csv file using Pandas
        df = pd.read_csv(filename, usecols = ['condition', "BlockList.Cycle", "BlockList2.Cycle", "BlockList.Sample", "BlockList2.Sample", "EmoStim.ACC", 'EmoStim.RT'])

        # dropping all na values in the condition column
        df = df.dropna(subset=['condition'])

        # changing all values in the BlockList2.Cycle Column to 2 if it was 1
        df.loc[df["BlockList2.Cycle"] == 1, "BlockList2.Cycle"] = 2

        # merge both blocklist cycle columns into one
        df["BlockList.Cycle"] = df['BlockList.Cycle'].combine_first(df['BlockList2.Cycle'])

        # drop BlockList2.Cycle column
        df = df.drop('BlockList2.Cycle', axis=1)

        # merge both blocklist sample columns into one
        df["BlockList.Sample"] = df['BlockList.Sample'].combine_first(df['BlockList2.Sample'])

        # drop BlockList2.Sample column
        df = df.drop('BlockList2.Sample', axis=1)

        # rename columns
        df = df.rename(columns={'BlockList.Cycle': 'BlockNum', 'BlockList.Sample': 'TrialNum', 'EmoStim.ACC': 'trial_acc', 'EmoStim.RT':'trial_rt'})

        # append to the total dataframe list
        total_dataframes.append(df)
    
    # create final dataframe with all the data
    final_dataframe = pd.concat(total_dataframes)

    # convert and export the final dataframe to a csv file
    final_dataframe.to_csv('participant_condition.csv')

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
