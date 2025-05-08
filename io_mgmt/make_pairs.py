# get the eeg and fnirs paths from the cli call
# get the eeg and fnirs file types from the cli call
# scan the paths for folders with identical subject ids
# return the found pairs and ids with missing files
# get the ids that should be included from cli
# begin the selection of first pair from first id by navigating and selecting to the eeg file/folder
# select the matching fnis by navigating
# add description of pair (can use standard descritions from config file TODO)
# save pair to raw_eeg_fnirs_pairs.txt in config

from config.data_paths_and_config import PROJECT_ROOT

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

def write_pair_loc_description(pairs, subject_id=None, output_file=None, manual_inputs=None):
    """
    Add descriptions to EEG-fNIRS pairs and save them to the raw_pairs_db.json database.
    
    Parameters
    ----------
    pairs : list
        List of dictionaries with paired EEG and fNIRS paths
        Format: [{'eeg_path': '/path/to/eeg', 'fnirs_path': '/path/to/fnirs'}, ...]
    subject_id : str, optional
        Subject ID for these pairs. If None, attempts to extract from filenames.
    output_file : str, optional
        Path to the JSON database file. If None, uses default location.
    manual_inputs : list, optional
        List of previously used manual settings, each a complete settings dict
        Format: [{'type': 'motor tapping', 'fields': {'hand': 'L', ...}}, ...]
        
    Returns
    -------
    list
        The manual inputs used, as a flat list for reuse in future calls
    """
    import os
    import json
    import re
    from datetime import datetime
    
    # Set up output file path
    try:
        from config.data_paths_and_config import PROJECT_ROOT
        output_file = output_file or os.path.join(PROJECT_ROOT, "config", "raw_pairs_db.json")
        print("found config file")
    except ImportError:
        if output_file is None:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            output_file = os.path.join(script_dir, '..', 'config', 'raw_pairs_db.json')
        print("could not find config file")

    print(f"Output file for pairs: {output_file}")
    
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    # Load templates
    try:
        # Add workspace root to Python path so "config" can be found
        import sys
        import os
        
        script_dir = os.path.dirname(os.path.abspath(__file__))
        workspace_root = os.path.dirname(script_dir) 
        
        if workspace_root not in sys.path:
            sys.path.insert(0, workspace_root)
            print(f"Added workspace root to Python path: {workspace_root}")
        
        import config.data_descriptions as desc_config
        print("Loaded metadata templates from data_descriptions.py")
        
        templates = {}
        for name in dir(desc_config):
            if name.endswith('_METADATA') and isinstance(getattr(desc_config, name), dict):
                obj = getattr(desc_config, name)
                if all(k in obj for k in ['type', 'auto', 'manual']):
                    type_value = obj['type'] 
                    if not isinstance(type_value, str):
                        print(f"Warning: Template '{name}' has a 'type' field that is not a string. Skipping.")
                        continue
                    templates[type_value] = obj
                    print(f"Found template: {type_value}")
        
        if not templates:
            print("Warning: No valid metadata templates found in data_descriptions.py")
            templates = {
                'default': {
                    'type': 'default',
                    'auto': {'subject': '', 'date_added_to_db': ''}, # Ensure these are present for fallback
                    'manual': {'description': ''}
                }
            }
    except ImportError:
        print("Could not import metadata templates. Using a basic template.")
        templates = {
            'default': {
                'type': 'default',
                'auto': {'subject': '', 'date_added_to_db': ''}, # Ensure these are present for fallback
                'manual': {'description': ''}
            }
        }
    
    # Load existing database if it exists
    existing_pairs = []
    if os.path.exists(output_file):
        try:
            with open(output_file, 'r') as f:
                data = json.load(f)
                existing_pairs = data.get('pairs', [])
                print(f"Loaded {len(existing_pairs)} existing pairs from database")
        except (json.JSONDecodeError, FileNotFoundError):
            print(f"Warning: Could not read existing file {output_file}, starting with empty database")
    
    # Check for duplicates
    used_eeg_paths = set()
    used_fnirs_paths = set()
    
    # First, collect all previously used paths from the database
    for existing_pair in existing_pairs:
        used_eeg_paths.add(existing_pair.get('eeg_path'))
        used_fnirs_paths.add(existing_pair.get('fnirs_path'))
    
    # Now check for duplicates in the current batch itself
    duplicate_check = {}
    for i, pair in enumerate(pairs):
        eeg_path = pair['eeg_path']
        fnirs_path = pair['fnirs_path']
        
        # Check if already used in existing database
        if eeg_path in used_eeg_paths:
            print(f"\nWARNING: EEG file already exists in database: {os.path.basename(eeg_path)}")
            duplicate_check[i] = True
        
        if fnirs_path in used_fnirs_paths:
            print(f"\nWARNING: fNIRS file already exists in database: {os.path.basename(fnirs_path)}")
            duplicate_check[i] = True
        
        # Also check if used multiple times in current batch
        for j, other_pair in enumerate(pairs):
            if i != j:  # Don't compare with self
                if eeg_path == other_pair['eeg_path']:
                    print(f"\nWARNING: EEG file used multiple times in current batch: {os.path.basename(eeg_path)}")
                    duplicate_check[i] = True
                
                if fnirs_path == other_pair['fnirs_path']:
                    print(f"\nWARNING: fNIRS file used multiple times in current batch: {os.path.basename(fnirs_path)}")
                    duplicate_check[i] = True
    
    # If any duplicates were found, ask user whether to continue
    if duplicate_check:
        print(f"\nFound {len(duplicate_check)} pairs with duplicate files.")
        print("Do you want to continue and add descriptions for non-duplicated pairs? (y/n)")
        response = input("> ").strip().lower()
        if response != 'y':
            print("Operation cancelled by user.")
            return manual_inputs or []
    
    # Initialize manual_inputs if not provided
    if manual_inputs is None:
        manual_inputs = []
    
    # Keep track of processed pairs
    pairs_with_descriptions = []
    
    # Process each valid pair
    for i, pair in enumerate(pairs):
        # Skip duplicates
        if duplicate_check.get(i):
            continue
            
        eeg_path = pair['eeg_path']
        fnirs_path = pair['fnirs_path']
        eeg_name = os.path.basename(eeg_path)
        fnirs_name = os.path.basename(fnirs_path)
        
        print(f"\nProcessing Pair {i+1}:")
        print(f"  EEG: {eeg_name}")
        print(f"  fNIRS: {fnirs_name}")
        
        # Always let user select the task type
        print("\nSelect task type:")
        task_types = list(templates.keys())
        for idx, task_name in enumerate(task_types, 1):
            # task_name is already the string type identifier (e.g., 'motor tapping')
            print(f"  {idx}: {task_name}")
        
        # Get task type selection
        while True:
            choice = input("> ").strip()
            try:
                index = int(choice) - 1
                if 0 <= index < len(task_types):
                    selected_task_type_key = task_types[index] # This is the key for the templates dict
                    metadata_template = templates[selected_task_type_key]
                    break
                else:
                    print(f"Please enter a number between 1 and {len(task_types)}")
            except ValueError:
                print("Invalid input. Please enter a number.")
        
        # Get the actual type name from the template (it's just the 'type' field value)
        type_name = metadata_template['type'] 
        
        # Check if we have previous manual inputs to offer
        use_previous = False
        selected_setting = None
        
        if manual_inputs:
            print("\nPrevious settings available:")
            for idx, setting in enumerate(manual_inputs, 1):
                # Show the task type and a summary of the settings
                print(f"  {idx}: {setting['type']} - ", end="")
                # Display a summary of fields (e.g., "hand: L, device: button")
                field_preview = ", ".join([f"{k}: {v}" for k, v in setting['fields'].items()][:3])
                if len(setting['fields']) > 3:
                    field_preview += ", ..."
                print(field_preview)
            
            # Add option to create new settings
            print(f"  {len(manual_inputs)+1}: Create new settings")
            
            # Get user selection
            while True:
                choice = input("\nSelect settings to use or create new: ").strip()
                try:
                    index = int(choice) - 1
                    if 0 <= index < len(manual_inputs):
                        selected_setting = manual_inputs[index]
                        use_previous = True
                        print(f"Using settings #{index+1}")
                        break
                    elif index == len(manual_inputs):
                        # Create new settings
                        use_previous = False
                        break
                    else:
                        print(f"Please enter a number between 1 and {len(manual_inputs)+1}")
                except ValueError:
                    print("Invalid input. Please enter a number.")
        else:
            # No previous settings available
            use_previous = False
        
        # Create metadata structure
        metadata = {
            'type': metadata_template['type'],
            'auto': {}, # Initialize auto metadata
            'manual': {}
        }
        
        # Auto-fill automatic fields based on the template
        # This will now include 'subject' and 'date_added_to_db' as defined in data_descriptions.py
        for field_key in metadata_template['auto']:
            if field_key == 'subject':
                # Determine the subject ID
                current_subject_id = "unknown"
                if subject_id:  # Use subject_id passed to the function (batch-level)
                    current_subject_id = subject_id
                elif metadata_template['auto'][field_key] == 'synthetic': # Handle synthetic case
                    current_subject_id = 'synthetic'
                else: # Try to infer from filename if not synthetic and no batch ID
                    subject_match_eeg = re.search(r'(?:subject|sub|s)[-_]?([a-zA-Z0-9]+)', eeg_name, re.IGNORECASE)
                    if subject_match_eeg:
                        current_subject_id = subject_match_eeg.group(1)
                    else:
                        subject_match_fnirs = re.search(r'(?:subject|sub|s)[-_]?([a-zA-Z0-9]+)', fnirs_name, re.IGNORECASE)
                        if subject_match_fnirs:
                            current_subject_id = subject_match_fnirs.group(1)
                metadata['auto'][field_key] = current_subject_id
            elif field_key == 'date_added_to_db':
                metadata['auto'][field_key] = datetime.now().strftime('%Y-%m-%dT%H:%M:%S') # Date and time
            else:
                # For any other 'auto' fields defined in the template
                metadata['auto'][field_key] = metadata_template['auto'][field_key]
        
        # Handle manual fields
        if use_previous and selected_setting['type'] == type_name:
            # Use the selected previous settings
            for field, value in selected_setting['fields'].items():
                if field in metadata_template['manual']:
                    metadata['manual'][field] = value
            
            print("Using previous field values")
        else:
            # Get new values for each manual field
            print("\nPlease provide the following information:")
            for field, options in metadata_template['manual'].items():
                if isinstance(options, list) and options:
                    # Show options with numbers
                    print(f"\nSelect {field.replace('_', ' ')}:")
                    for j, option in enumerate(options, 1):
                        print(f"  {j}: {option}")
                    print(f"  {len(options)+1}: Custom (enter your own)")
                    
                    # Get selection
                    while True:
                        choice = input("> ").strip()
                        try:
                            choice_idx = int(choice) - 1
                            if 0 <= choice_idx < len(options):
                                value = options[choice_idx]
                                break
                            elif choice_idx == len(options):
                                # Custom option
                                print(f"Enter custom value for {field}:")
                                value = input("> ").strip()
                                break
                            else:
                                print(f"Please enter a number between 1 and {len(options)+1}")
                        except ValueError:
                            print("Invalid input. Please enter a number.")
                else:
                    # Free text field
                    print(f"\nEnter {field.replace('_', ' ')}:")
                    value = input("> ").strip()
                
                metadata['manual'][field] = value
        
        # Create the final pair entry
        pair_with_desc = {
            'eeg_path': eeg_path,
            'fnirs_path': fnirs_path,
            #'task_type': type_name,
            'metadata': metadata # 'metadata.auto' now contains subject and date_added_to_db
        }
        
        pairs_with_descriptions.append(pair_with_desc)
        
        # If we created new settings, store them for future use
        if not use_previous:
            # Store this as a new setting
            new_setting = {
                'type': type_name,
                'fields': metadata['manual'].copy()
            }
            manual_inputs.append(new_setting)
            print(f"Added new settings (#{len(manual_inputs)})")
            print (f"\nManual inputs for future use: {manual_inputs}")
    
    # Save database
    if pairs_with_descriptions:
        # Add to existing pairs
        existing_pairs.extend(pairs_with_descriptions)
        
        # Create full database structure
        database = {
            'last_updated': datetime.now().isoformat(),
            'num_pairs': len(existing_pairs),
            'pairs': existing_pairs
        }
        
        # Write to file
        with open(output_file, 'w') as f:
            json.dump(database, f, indent=2)
        
        print(f"\nSaved {len(pairs_with_descriptions)} new pairs to {output_file}")
    else:
        print("\nNo new pairs to save")
    
    # Return all manual inputs for future use
    
    return manual_inputs

matching_ids, missing_eeg_ids, missing_fnirs_ids = scan_for_matching_ids(path_eeg = '/home/lennart/Desktop/Motor Task Subjects/EEG', path_fnirs = '/home/lennart/Desktop/Motor Task Subjects/fNIRS/NIRX', id_pattern=None)

if matching_ids: 
    first_id = list(matching_ids.keys())[0]
    datasets = list_datasets_per_id(matching_ids[first_id], type_eeg='.fif', type_fnirs='.wl1', recursive=True, return_folders_eeg=False, return_folders_fnirs=True)
    pairs = make_pairs(datasets)
    print(pairs)

    if pairs:
        write_pair_loc_description(pairs, subject_id=first_id)
else:
    print("No matching subject IDs found. Cannot proceed with pairing.")


