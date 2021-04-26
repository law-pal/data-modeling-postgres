import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *


def process_song_file(cur, filepath):
    """ This function populates the 'artists' and 'songs'
    tables with their respective data from the datasets.
    Parameters
    ----------
    cur (psycopg2.cursor): python driver cursor.

    filepath (str) : file path containing the data.

    Raises
    ------
    NotImplementedError

    """
    # open song file
    df = pd.read_json(filepath, lines=True)

    # insert song record
    song_data = list(df[['song_id', 'title', 'artist_id',
                         'year', 'duration']].values[0])
    cur.execute(song_table_insert, song_data)

    # insert artist record
    artist_data = list(df[['artist_id', 'artist_name', 'artist_location',
                           'artist_latitude', 'artist_longitude']].values[0])

    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    """ This function inserts time information into the 'time' table and
    upserts information into the 'users' table, it also populates the
    Songplay information into the 'songplays' table.

    Parameters
    ----------
    cur (psycopg2.cursor): python driver cursor.

    filepath (str) : file path containing the data.

    Raises
    ------
    NotImplementedError

    """
    # open log file
    df = pd.read_json(filepath, lines=True)

    # filter by NextSong action
    df = df.loc[df['page'] == 'NextSong']

    # convert timestamp column to datetime
    t = pd.to_datetime(df['ts'], unit='ms')

    # insert time data records
    time_data = (
        df.ts.values,
        t.dt.hour,
        t.dt.day,
        t.dt.week,
        t.dt.month,
        t.dt.year,
        t.dt.weekday)
    column_labels = [
        'start_time',
        'hour',
        'day',
        'week',
        'month',
        'year',
        'weekday']
    time_df = pd.DataFrame(dict(zip(column_labels, time_data)))

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = df[['userId', 'firstName', 'lastName', 'gender', 'level']]

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    # insert songplay records
    for index, row in df.iterrows():

        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()

        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data = (
            row.ts,
            row.userId,
            row.level,
            songid,
            artistid,
            row.sessionId,
            row.location,
            row.userAgent)

        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    """ This function processeses JSON files for a data directory path.

    Valid function values can be 'process_song_file' or
    'process_log_file'.

    Args:

    cur (psycopg2.cursor): A database cursor
    conn (psycopg2.connection): A database connection
    filepath (str): A filepath of the directory to process
    func (function): The function to call for each found file

    """
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root, '*.json'))
        for f in files:
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    """ This function is the driver function it creates a database connection,
    and processes Song and Log information, and then
    closes the cursor and database connection.

    """
    conn = psycopg2.connect(
        "host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()
