import os
from pathlib import Path

# Base paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_ROOT = os.path.join(PROJECT_ROOT, "data")


# Add external data paths here
EXTERNAL_DATA_PATHS = {
    'eeg_motor_tasks_trials': '/home/lennart/Desktop/Motor Task Subjects/EEG',
    'fnirs_motor_tasks_trials_raw': '/home/lennart/Desktop/Motor Task Subjects/fNIRS',
}

# Add internal structures here
INTERNAL_DATA_PATHS = {
    'motor_data_combined_sorted_annotations': os.path.join(DATA_ROOT, 'motor_data_combined_sorted_annotations'),  
}



# Ensure directories exist
def create_directories():
    """Create all necessary data directories if they don't exist."""
    for path_dict in [INTERNAL_DATA_PATHS]:
        for path in path_dict.values():
            os.makedirs(path, exist_ok=True)

# Create directories when this module is imported
create_directories()