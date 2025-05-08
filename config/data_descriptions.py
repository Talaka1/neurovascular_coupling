"""
Metadata templates for different types of neurovascular coupling data.
Each template should be a dictionary ending with _METADATA and containing:
- type: String data type identifier
- auto: Dictionary of fields automatically filled -> subject id and date are mandatory
- manual: Dictionary of fields requiring user input (can include lists of options)
"""

# Motor tapping task metadata
MOTOR_TASK_METADATA = {
    'type': 'motor tapping',  # Task type identifier
    'auto': {
        'subject': '',              # Subject ID code - extracted from filename/path
        'date_added_to_db': ''      # Date when the pair was added to the database
    },
    'manual': {
        'hand': ['L', 'R', 'both'],  # Left, Right, or Both hands
        'device': ['button', 'light_barrier', 'accelerometer', 'force_sensor'],  # Device used for tapping
        'isi': [15, 20, 25, 30, 35, 40, 45],  # Inter-stimulus interval in seconds
        'cue_type': ['visual', 'auditory', 'both', 'self_paced'],  # Stimulus presentation modality
        'tapping_rate': [0.5, 1, 2]  # Tapping frequency in Hz
    }
}

# Resting state metadata
RESTING_STATE_METADATA = {
    'type': 'resting state',  # Task type identifier
    'auto': {
        'subject': '',              # Subject ID code - extracted from filename/path
        'date_added_to_db': ''      # Date when the pair was added to the database
    },
    'manual': {
        'eyes': ['open', 'closed', 'alternating'],  # Eye state during recording
        'position': ['sitting', 'supine', 'standing']  # Body position during recording
    }
}

# Synthetic data metadata
SYNTHETIC_DATA_METADATA = {
    'type': 'synthetic',  # Data type identifier
    'auto': {
        'subject': 'synthetic',     # Marked as synthetic data, generated subject ID
        'date_added_to_db': ''      # Date when the synthetic data was created/added
    },
    'manual': {
        'simulated_activity': ['motor', 'resting', 'custom'],  # Type of brain activity
        'noise_level': ['low', 'medium', 'high'],  # Amount of noise in the simulation
        'coupling_strength': ['weak', 'moderate', 'strong'],  # Neural-hemodynamic coupling strength
        'delay_seconds': '',  # Hemodynamic response delay in seconds
        'description': ''  # Free text description of the synthetic data
    }
}

# You can add more templates as needed