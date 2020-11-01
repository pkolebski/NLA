import logging
import multiprocessing
import os
import time
import xml.etree.ElementTree as ET
from collections import namedtuple
from functools import partial

import daiquiri
import pandas as pd
import tqdm

from NLA.tagger import ClarinTagger

daiquiri.setup(level=logging.INFO)
logger = daiquiri.getLogger(__name__)

Token = namedtuple('Token', ['text', 'tag'])

data_path = 'wiki_data'
train_path = os.path.join(data_path, 'wiki_train_34_categories_data')
test_path = os.path.join(data_path, 'wiki_test_34_categories_data')
processed_train_path = os.path.join(
    data_path, 'wiki_train_34_categories_data_processed')
processed_test_path = os.path.join(
    data_path, 'wiki_test_34_categories_data_processed')

N_JOBS = 50

if not os.path.exists(processed_train_path):
    os.makedirs(processed_train_path)

if not os.path.exists(processed_test_path):
    os.makedirs(processed_test_path)


def load_data(path):
    file_paths = []
    with os.scandir(path) as it:
        for entry in it:
            if not entry.name.startswith('.') and entry.is_file():
                file_paths.append({'path': entry.path, 'name': entry.name})
    return file_paths


def clean_data(data, text_col):
    data[text_col] = data[text_col].str.replace('\n', '')
    return data


def filter_processed(paths, processed_paths):
    processed_files = \
        [file_dict['name'].split('.')[0] for file_dict in processed_paths]
    return [el for el in paths
            if el['name'].split('.')[0] not in processed_files]


def get_tagged_token(token):
    try:
        return Token(text=token[1][0].text, tag=token[1][1].text)
    except IndexError:
        return None


def get_tagged_data(data, tagger):
    filename = data['filename']
    data = data['text']
    # logging.info(f"Parsing text {filename}...")
    start = time.time()
    parsed_data = tagger.tag(data)
    elapsed_parsing_time = time.time() - start
    tagged_data = []
    start = time.time()
    root = ET.fromstring(parsed_data)
    for chunk in root:
        for token in chunk[0]:
            tagged_token = get_tagged_token(token)
            if tagged_token:
                tagged_data.append(tagged_token)
    # logging.info(f"Parsed {filename}! Parsing time: {elapsed_parsing_time}, "
    #              f"tokenizing time: {time.time() - start}")
    return tagged_data


def process_file(entry, tagger):
    with open(entry['path'], encoding='utf-8') as f:
        text = f.read()
    df = pd.DataFrame.from_dict(
        {'text': [text],
         'cat': [entry['name'].split('_')[0]],
         'filename': [entry['name']]}
    )
    df = clean_data(df, 'text')
    df['tokens'] = df.apply(lambda x: get_tagged_data(x, tagger), axis=1)
    df.to_pickle(os.path.join(
        processed_train_path, df['filename'].iloc[0].replace('.txt', '.pkl')
    ))


def run_imap_multiprocessing(func, argument_list, num_processes):
    pool = multiprocessing.Pool(processes=num_processes)

    result_list_tqdm = []
    for result in tqdm.tqdm(pool.imap(func=func, iterable=argument_list),
                            total=len(argument_list)):
        result_list_tqdm.append(result)

    return result_list_tqdm


if __name__ == '__main__':
    clarin_tagger = ClarinTagger()

    train_path_list = load_data(train_path)
    processed_train_path_list = load_data(processed_train_path)
    filtered_train_path_list = \
        filter_processed(train_path_list, processed_train_path_list)

    run_imap_multiprocessing(
        func=partial(process_file, tagger=clarin_tagger),
        argument_list=filtered_train_path_list,
        num_processes=N_JOBS
    )

# with multiprocessing.Pool(N_JOBS) as pool:
#     pool.map(
#         partial(process_file, tagger=clarin_tagger),
#         filtered_train_path_list
#     )
