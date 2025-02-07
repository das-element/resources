import csv
import os

from daselement_api import api


def load_ingest_log(path: str):
    # Open the CSV file and read its contents
    with open(path, 'r', newline='') as f:
        reader = csv.reader(f, delimiter=';')
        rows = list(reader)
    header = rows[0]
    data_dicts = []
    for row in rows[1:]:
        data_dicts.append(dict(zip(header, row)))
    return data_dicts


def load_ingest_logs(folder_path: str):
    # Load and combine ingest logs from CSV files in the specified folder.
    combined_data = []
    for file_name in sorted(os.listdir(folder_path)):
        if not file_name.endswith('.csv'):
            continue
        csv_path = os.path.join(folder_path, file_name)
        combined_data.extend(load_ingest_log(csv_path))
    return combined_data


def ingest(library_path: str, mapping: str, item: dict[str,
                                                       str]) -> dict[str, any]:
    """
    ingest log structure:
        - path' (str): The path of the item
        - category (str): The category of the item
        - colorspace (str, optional): Colorspace name
        - metadata (str, optional): A string of metadata in the format 'key1|value1,key2|value2'
        - additionals (str, optional): A string of additional information in the format 'path|type|name'
        - tags (str, optional): A string of tags separated by commas
        - media_type (str, optional): The media type of the item
    """

    metadata = {}
    # split metadata string into key-value pairs
    # example: 'key1|value1,key2|value2' -> {'key1': 'value1', 'key2': 'value2'}
    if item.get('metadata'):
        metadata = dict(
            kv.split('|') for kv in item.get('metadata').split(','))

    additionals = []
    # split additionals string into path, type, name
    # example: 'foo|bar|baz' -> {'path': 'foo', 'type': 'bar', 'name': 'baz'}
    if item.get('additionals'):
        additionals.append(
            dict(
                zip(['path', 'type', 'name'],
                    item.get('additionals').split('|'))))
    # tags  are a string of tags separated by commas
    tags = item.get('tags', '').split(',')

    return api.ingest(library_path,
                      mapping,
                      item.get('path'),
                      item.get('category'),
                      tags=tags,
                      media_type=item.get('media_type', ''),
                      metadata=metadata,
                      additionals=additionals)


def main():

    ingest_logs_folder = '/path/to/library/.config/ingest_logs'
    library_path = '/path/to/library/.config/das-element.lib'
    mapping = 'copy & rename'

    ingest_logs = load_ingest_logs(ingest_logs_folder)

    for ingest_log in ingest_logs:
        new_entity = ingest(library_path, mapping, ingest_log)
        print('Created new element:')
        print(new_entity)


main()
