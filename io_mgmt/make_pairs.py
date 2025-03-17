# get the eeg and fnirs paths from the cli call
# get the eeg and fnirs file types from the cli call
# scan the paths for folders with identical subject ids
# return the found pairs and ids with missing files
# get the ids that should be included from cli
# begin the selection of first pair from first id by navigating and selecting to the eeg file/folder
# select the matching fnis by navigating
# add description of pair (can use standard descritions from config file TODO)
# save pair to raw_eeg_fnirs_pairs.txt in config

def scan_for_matching_ids(path_eeg, path_fnirs):
    #scan for matching ids of subfolders

    matching_ids = {}

    missing_ids = {}

    return matching_ids, missing_ids

def list_datasets_per_id(path_eeg, path_fnirs, type_eeg, type_fnirs, matching_ids):
    # check how many subfolders aka datasets, if more than one, return and list all fnirs and eeg 
    # datasets for the id
    return 

def write_pair_loc_description(path_eeg_file, path_fnirs_file, type_eeg, type_fnirs, description):
    # write path to eeg and fnirs file and description to raw_eeg_fnirs_pairs.txt
    return



    

