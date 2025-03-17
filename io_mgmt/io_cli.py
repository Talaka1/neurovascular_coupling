"""
1. Match eeg and fnirs filed of ids, write pairs to file with added description
2. combine data and save internal with description
3. change annots to standard
"""

#1. match eeg and fnirs
# get the eeg and fnirs paths from the cli call
# get the eeg and fnirs file types from the cli call
# scan the paths for folders with identical subject ids
# return the found pairs and ids with missing files
# get the ids that should be included from cli
# begin the selection of first pair from first id by navigating and selecting to the eeg file/folder
# select the matching fnis by navigating
# add description of pair (can use standard descritions from config file TODO)
# save pair to raw_eeg_fnirs_pairs.txt in config

def match_ids_datasets(path_eeg, path_fnirs, type_eeg, type_fnirs, matching_ids):
    # navigate within the id's eeg folder and select file,
    # then navigate in fnirs folder and select file.
    # navigate using selection of listed folders and files
    return