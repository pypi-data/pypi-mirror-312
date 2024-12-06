import json
import os

import importlib.resources

def load_download():
    with importlib.resources.open_text('subdata.resources', 'download_dict.json') as file:
        download_dict = json.load(file)
    return download_dict

def load_instruction():
    with importlib.resources.open_text('subdata.resources', 'instruction_dict.json') as file:
        instruction_dict = json.load(file)
    return instruction_dict

def load_process():
    with importlib.resources.open_text('subdata.resources', 'process_dict.json') as file:
        process_dict = json.load(file)
    return process_dict

def load_overview(overview_name):

    if overview_name == 'original':
        with importlib.resources.open_text('subdata.resources', 'overview_dict_original.json') as file:
            overview_dict = json.load(file)
        print('Using original overview.')
    else:
        if os.path.exists(f'modified_resources/overview_dict_{overview_name}.json'):
            with open(f'modified_resources/overview_dict_{overview_name}.json') as file:
                overview_dict = json.load(file)
            print(f'Using {overview_name} overview.')
        else:
            with importlib.resources.open_text('subdata.resources', 'overview_dict_original.json') as file:
                overview_dict = json.load(file)
            print(f'Overview with name {overview_name} does not exist. Using original overview instead.')

    return overview_dict


def load_mapping(mapping_name):

    if mapping_name == 'original':
        with importlib.resources.open_text('subdata.resources', 'mapping_original.json') as file:
            mapping_dict = json.load(file)
        print('Using original mapping.')
    else:
        if os.path.exists(f'modified_resources/mapping_{mapping_name}.json'):
            with open(f'modified_resources/mapping_{mapping_name}.json') as file:
                mapping_dict = json.load(file)
            print(f'Using {mapping_name} mapping.')
        else:
            with importlib.resources.open_text('subdata.resources', 'mapping_original.json') as file:
                mapping_dict = json.load(file)
            print(f'Mapping with name {mapping_name} does not exist. Using original mapping instead.')

    return mapping_dict


def load_taxonomy(taxonomy_name):

    if taxonomy_name == 'original':
        with importlib.resources.open_text('subdata.resources', 'taxonomy_original.json') as file:
            taxonomy_dict = json.load(file)
        print('Using original taxonomy.')
    else:
        if os.path.exists(f'modified_resources/taxonomy_{taxonomy_name}.json'):
            with open(f'modified_resources/taxonomy_{taxonomy_name}.json') as file:
                taxonomy_dict = json.load(file)
            print(f'Using {taxonomy_name} taxonomy.')
        else:
            with importlib.resources.open_text('subdata.resources', 'taxonomy_original.json') as file:
                taxonomy_dict = json.load(file)
            print(f'Taxonomy with name {taxonomy_name} does not exist. Using original taxonomy instead.')

    return taxonomy_dict
    
