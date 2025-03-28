# get the eeg and fnirs paths from the cli call
# get the eeg and fnirs file types from the cli call
# scan the paths for folders with identical subject ids
# return the found pairs and ids with missing files
# get the ids that should be included from cli
# begin the selection of first pair from first id by navigating and selecting to the eeg file/folder
# select the matching fnis by navigating
# add description of pair (can use standard descritions from config file TODO)
# save pair to raw_eeg_fnirs_pairs.txt in config

def scan_for_matching_ids(path_eeg, path_fnirs, id_pattern=None):
    """
    Scan for matching IDs of subfolders in the EEG and fNIRS folders.
    
    Parameters
    ----------
    path_eeg : str
        Path to the EEG data directory
    path_fnirs : str
        Path to the fNIRS data directory
    id_pattern : str, optional
        Regular expression pattern to extract subject IDs.
        If None, uses any alphanumeric sequence as ID.
        
    Returns
    -------
    tuple
        (matching_ids_dict, missing_eeg_ids, missing_fnirs_ids)
        matching_ids_dict: {id: {'eeg': eeg_folder_path, 'fnirs': fnirs_folder_path}}
    """
    import os
    import re
    
    # Check if the paths exist
    if not os.path.exists(path_eeg):
        raise FileNotFoundError(f"EEG path not found: {path_eeg}")
    if not os.path.exists(path_fnirs):
        raise FileNotFoundError(f"fNIRS path not found: {path_fnirs}")
    
    # Get all subfolders in both directories
    eeg_items = os.listdir(path_eeg)
    fnirs_items = os.listdir(path_fnirs)
    
    # Filter to keep only directories
    eeg_folders = [item for item in eeg_items if os.path.isdir(os.path.join(path_eeg, item))]
    fnirs_folders = [item for item in fnirs_items if os.path.isdir(os.path.join(path_fnirs, item))]
    
    # Use default pattern if none provided (any sequence of digits or letters)
    if id_pattern is None:
        id_pattern = r'([a-zA-Z0-9]+)'
    
    # Extract subject IDs and store with their folder paths
    eeg_ids_to_folders = {}
    for folder in eeg_folders:
        match = re.search(id_pattern, folder)
        if match:
            subject_id = match.group(1)
            eeg_ids_to_folders[subject_id] = os.path.join(path_eeg, folder)
    
    fnirs_ids_to_folders = {}
    for folder in fnirs_folders:
        match = re.search(id_pattern, folder)
        if match:
            subject_id = match.group(1)
            fnirs_ids_to_folders[subject_id] = os.path.join(path_fnirs, folder)
    
    # Find matching and missing IDs
    eeg_ids = set(eeg_ids_to_folders.keys())
    fnirs_ids = set(fnirs_ids_to_folders.keys())
    
    matching_ids = sorted(list(eeg_ids.intersection(fnirs_ids)))
    missing_eeg_ids = sorted(list(fnirs_ids - eeg_ids))
    missing_fnirs_ids = sorted(list(eeg_ids - fnirs_ids))
    
    # Create dictionary with matching IDs as keys and folder paths as values
    matching_ids_dict = {}
    for subject_id in matching_ids:
        matching_ids_dict[subject_id] = {
            'eeg': eeg_ids_to_folders[subject_id],
            'fnirs': fnirs_ids_to_folders[subject_id]
        }
    
    print(f"Found {len(matching_ids)} matching subject IDs: {', '.join(matching_ids)}")
    if missing_eeg_ids:
        print(f"Missing EEG data for {len(missing_eeg_ids)} subjects: {', '.join(missing_eeg_ids)}")
    if missing_fnirs_ids:
        print(f"Missing fNIRS data for {len(missing_fnirs_ids)} subjects: {', '.join(missing_fnirs_ids)}")
    
    return matching_ids_dict, missing_eeg_ids, missing_fnirs_ids

def list_datasets_per_id(id_paths, type_eeg=None, type_fnirs=None, recursive=False, return_folders_eeg=False, return_folders_fnirs=False):
    """
    List all EEG and fNIRS datasets for a specific subject ID.
    
    Parameters
    ----------
    id_paths : dict
        Dictionary with 'eeg' and 'fnirs' paths for a specific subject ID
        Format: {'eeg': '/path/to/eeg_folder', 'fnirs': '/path/to/fnirs_folder'}
    type_eeg : str, optional
        File extension for EEG files (e.g., '.fif')
    type_fnirs : str, optional
        File extension for fNIRS files (e.g., '.snirf')
    recursive : bool, optional
        Whether to search recursively in subdirectories
    return_folders_eeg : bool, optional
        If True, return the parent folder of the found files instead of the files for EEG
    return_folders_fnirs : bool, optional
        If True, return the parent folder of the found files instead of the files for fNIRS
        
    Returns
    -------
    dict
        Dictionary with 'eeg' and 'fnirs' keys, each containing lists of:
        - If return_folders_*=False: {'filename': 'name', 'path': 'full/path'}
        - If return_folders_*=True:  {'folder': 'name', 'path': 'folder/path'}
    """
    import os
    import glob
    
    datasets = {'eeg': [], 'fnirs': []}
    
    # Process EEG data path
    eeg_path = id_paths['eeg']
    if type_eeg:
        # Use ** for recursive search if needed
        pattern = os.path.join(eeg_path, '**', f'*{type_eeg}') if recursive else os.path.join(eeg_path, f'*{type_eeg}')
        eeg_files = glob.glob(pattern, recursive=recursive)
    else:
        # If no type specified, get all files
        pattern = os.path.join(eeg_path, '**', '*') if recursive else os.path.join(eeg_path, '*')
        eeg_files = [f for f in glob.glob(pattern, recursive=recursive) if os.path.isfile(f)]
    
    # Process fNIRS data path
    fnirs_path = id_paths['fnirs']
    if type_fnirs:
        pattern = os.path.join(fnirs_path, '**', f'*{type_fnirs}') if recursive else os.path.join(fnirs_path, f'*{type_fnirs}')
        fnirs_files = glob.glob(pattern, recursive=recursive)
    else:
        pattern = os.path.join(fnirs_path, '**', '*') if recursive else os.path.join(fnirs_path, '*')
        fnirs_files = [f for f in glob.glob(pattern, recursive=recursive) if os.path.isfile(f)]
    
    # Handle the return format for EEG (files or their parent folders)
    if return_folders_eeg:
        # For EEG: Get unique parent folders
        eeg_folders = set()
        for file in eeg_files:
            parent_folder = os.path.dirname(file)
            eeg_folders.add(parent_folder)
        
        for folder in sorted(eeg_folders):
            folder_name = os.path.basename(folder)
            datasets['eeg'].append({'folder': folder_name, 'path': folder})
    else:
        # Return the EEG files directly
        for file in sorted(eeg_files):
            file_name = os.path.basename(file)
            datasets['eeg'].append({'filename': file_name, 'path': file})
    
    # Handle the return format for fNIRS (files or their parent folders)
    if return_folders_fnirs:
        # For fNIRS: Get unique parent folders
        fnirs_folders = set()
        for file in fnirs_files:
            parent_folder = os.path.dirname(file)
            fnirs_folders.add(parent_folder)
        
        for folder in sorted(fnirs_folders):
            folder_name = os.path.basename(folder)
            datasets['fnirs'].append({'folder': folder_name, 'path': folder})
    else:
        # Return the fNIRS files directly
        for file in sorted(fnirs_files):
            file_name = os.path.basename(file)
            datasets['fnirs'].append({'filename': file_name, 'path': file})
    
    # Print summary
    print(f"\nFound datasets for subject:")
    print(f"  EEG: {len(datasets['eeg'])} {'folders' if return_folders_eeg else 'files'}")
    print(f"  fNIRS: {len(datasets['fnirs'])} {'folders' if return_folders_fnirs else 'files'}")
    
    # Print details of what was found
    if datasets['eeg']:
        print("\nEEG datasets:")
        for i, item in enumerate(datasets['eeg'], 1):
            name = item.get('folder', item.get('filename', 'unknown'))
            print(f"  {i}: {name}")
    
    if datasets['fnirs']:
        print("\nfNIRS datasets:")
        for i, item in enumerate(datasets['fnirs'], 1):
            name = item.get('folder', item.get('filename', 'unknown'))
            print(f"  {i}: {name}")
    
    return datasets

def make_pairs(datasets, auto_match_single=False):
    """
    Create pairs of EEG and fNIRS datasets using batch input of index combinations.
    
    Parameters
    ----------
    datasets : dict
        Dictionary with 'eeg' and 'fnirs' lists of datasets
    auto_match_single : bool, optional
        If True, automatically match datasets when only one of each type exists
        If False, ask the user for confirmation before matching single datasets
        
    Returns
    -------
    list
        List of dictionaries with paired EEG and fNIRS paths
    """
    # Check if we have any datasets to pair
    if not datasets['eeg']:
        print("No EEG datasets found. Cannot create pairs.")
        return []
    
    if not datasets['fnirs']:
        print("No fNIRS datasets found. Cannot create pairs.")
        return []
    
    # List to store created pairs
    created_pairs = []
    
    # Check if we have exactly one dataset of each type
    if len(datasets['eeg']) == 1 and len(datasets['fnirs']) == 1:
        eeg_dataset = datasets['eeg'][0]
        fnirs_dataset = datasets['fnirs'][0]
        eeg_name = eeg_dataset.get('folder', eeg_dataset.get('filename', 'unknown'))
        fnirs_name = fnirs_dataset.get('folder', fnirs_dataset.get('filename', 'unknown'))
        
        # Either automatically match or ask for confirmation
        if auto_match_single:
            created_pair = {
                'eeg_path': eeg_dataset['path'],
                'fnirs_path': fnirs_dataset['path']
            }
            created_pairs.append(created_pair)
            print(f"\nAutomatically matched the only available datasets:")
            print(f"  {eeg_name} + {fnirs_name}")
            return created_pairs
        else:
            print(f"\nOnly one EEG and one fNIRS dataset found.")
            print(f"EEG: {eeg_name}")
            print(f"fNIRS: {fnirs_name}")
            print("\nAutomatically match these datasets? (y/n):")
            
            confirm = input("> ").strip().lower()
            if confirm == 'y':
                created_pair = {
                    'eeg_path': eeg_dataset['path'],
                    'fnirs_path': fnirs_dataset['path']
                }
                created_pairs.append(created_pair)
                print("Datasets matched.")
                return created_pairs
    
    # If we have multiple datasets or the user declined automatic matching,
    # proceed with manual pairing
    
    # Display summary of available datasets
    print("\n===== Create Pairs =====")
    
    print("\nAvailable EEG datasets:")
    for i, item in enumerate(datasets['eeg'], 1):
        name = item.get('folder', item.get('filename', 'unknown'))
        print(f"  {i}: {name}")
    
    print("\nAvailable fNIRS datasets:")
    for i, item in enumerate(datasets['fnirs'], 1):
        name = item.get('folder', item.get('filename', 'unknown'))
        print(f"  {i}: {name}")
    
    # Get user input for pairs
    while True:
        print("\nEnter pairs as \"EEG_index+fNIRS_index\" separated by commas:")
        print("(e.g., \"1+3, 2+2, 3+1\" or \"q\" to quit)")
        
        user_input = input("> ").strip()
        
        # Check if user wants to quit
        if user_input.lower() == 'q':
            break
        
        # Parse the input to get pairs
        pair_strs = [p.strip() for p in user_input.split(',')]
        valid_pairs = []
        invalid_pairs = []
        
        for pair_str in pair_strs:
            # Skip empty entries
            if not pair_str:
                continue
                
            # Check if the format is correct (e.g., "1+3")
            if '+' not in pair_str:
                invalid_pairs.append((pair_str, "Missing '+' separator"))
                continue
            
            # Split the pair into EEG and fNIRS indices
            try:
                eeg_idx_str, fnirs_idx_str = pair_str.split('+')
                eeg_idx = int(eeg_idx_str.strip())
                fnirs_idx = int(fnirs_idx_str.strip())
                
                # Check if the indices are valid
                if eeg_idx < 1 or eeg_idx > len(datasets['eeg']):
                    invalid_pairs.append((pair_str, f"EEG index {eeg_idx} out of range"))
                    continue
                
                if fnirs_idx < 1 or fnirs_idx > len(datasets['fnirs']):
                    invalid_pairs.append((pair_str, f"fNIRS index {fnirs_idx} out of range"))
                    continue
                
                # Get the actual dataset entries
                eeg_dataset = datasets['eeg'][eeg_idx - 1]
                fnirs_dataset = datasets['fnirs'][fnirs_idx - 1]
                
                # Add to valid pairs
                valid_pairs.append({
                    'eeg_idx': eeg_idx,
                    'fnirs_idx': fnirs_idx,
                    'eeg_info': eeg_dataset,
                    'fnirs_info': fnirs_dataset
                })
                
            except ValueError:
                invalid_pairs.append((pair_str, "Invalid format - use numbers only"))
                continue
        
        # Report any invalid entries
        if invalid_pairs:
            print("\nThe following entries were invalid:")
            for pair, reason in invalid_pairs:
                print(f"  - {pair}: {reason}")
            
            if not valid_pairs:
                print("No valid pairs found. Please try again.")
                continue
        
        # Show the valid pairs for confirmation
        if valid_pairs:
            print("\nYou've selected the following pairs:")
            for i, pair in enumerate(valid_pairs, 1):
                eeg_name = pair['eeg_info'].get('folder', pair['eeg_info'].get('filename', 'unknown'))
                fnirs_name = pair['fnirs_info'].get('folder', pair['fnirs_info'].get('filename', 'unknown'))
                print(f"  {i}. {eeg_name} + {fnirs_name}")
            
            # Ask for confirmation
            print("\nConfirm these pairs? (y/n):")
            confirm = input("> ").strip().lower()
            
            if confirm == 'y':
                # Add the confirmed pairs to our results
                for pair in valid_pairs:
                    created_pair = {
                        'eeg_path': pair['eeg_info']['path'],
                        'fnirs_path': pair['fnirs_info']['path']
                    }
                    created_pairs.append(created_pair)
                
                print(f"\n{len(valid_pairs)} pairs created.")
                break  # Exit after creating pairs
            else:
                print("Pairs not confirmed. Please try again.")
    
    # Return all created pairs
    return created_pairs

def write_pair_loc_description(path_eeg_file, path_fnirs_file, type_eeg, type_fnirs, description):
    # write path to eeg and fnirs file and description to raw_eeg_fnirs_pairs.txt
    return


matching_ids, missing_eeg_ids, missing_fnirs_ids = scan_for_matching_ids(path_eeg = '/home/lennart/Desktop/Motor Task Subjects/EEG', path_fnirs = '/home/lennart/Desktop/Motor Task Subjects/fNIRS/NIRX', id_pattern=None)
#print(matching_ids, missing_eeg_ids, missing_fnirs_ids)
# Get the first ID from the matching_ids dictionary
first_id = list(matching_ids.keys())[0]
datasets = list_datasets_per_id(matching_ids[first_id], type_eeg='.fif', type_fnirs='.wl1', recursive=True, return_folders_eeg=False, return_folders_fnirs=True)
#print(datasets)
pairs = make_pairs(datasets)
print(pairs)

