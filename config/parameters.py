"""Configuration parameters for EEG and fNIRS preprocessing and analysis."""

# EEG Preprocessing Parameters
EEG_PREPROCESSING = {
    'filter': {
        'l_freq': 0.1,  # High-pass filter in Hz
        'h_freq': 80.0,  # Low-pass filter in Hz
        'notch_freq': [50, 100],  # For line noise
    },
    'bands': {
        'delta': (0.5, 4),
        'theta': (4, 8),
        'alpha': (8, 13),
        'beta': (13, 30),
        'gamma': (30, 45)
    },
    'bad_channels_criteria': {
        'threshold': 5.0  # Z-score threshold for automatic bad channel detection
    }
}

# fNIRS Preprocessing Parameters
FNIRS_PREPROCESSING = {
    'filter': {
        'l_freq': 0.01,  # High-pass filter in Hz
        'h_freq': 0.5,   # Low-pass filter in Hz
        'h_trans_bandwidth': 0.2,
        'l_trans_bandwidth': 0.005
    },
    'sci': {
        'threshold': 0.7,  # Scalp coupling index threshold
        'time_window': 60  # Seconds
    },
    'remove_mayer': False,  # Whether to remove Mayer wave component
    'apply_tddr': True      # Apply Temporal Derivative Distribution Repair
}

# Combined Data Parameters
COMBINE_PARAMS = {
    'resample_to': 250  # Resample combined data to this frequency (Hz)
}

# Neurovascular Coupling Analysis Parameters
NVC_ANALYSIS = {
    'time_delay': {
        'max_lag_seconds': 10.0,
        'min_lag_seconds': -2.0,
        'correlate_with': 'hbo'  # 'hbo', 'hbr', or 'both'
    },
    'pac': {
        'low_fq_range': [0.01, 0.9],  # fNIRS frequency range
        'low_fq_width': 0.1,
        'high_fq_range': [1.0, 45.0],  # EEG frequency range 
        'high_fq_width': 1.0,
        'method': 'tort'  # Options: 'tort', 'penny', 'duprelatour'
    },
    'glm': {
        'drift_model': 'cosine',
        'high_pass': 0.005,
        'hrf_model': 'spm'
    }
}

# Task-specific Parameters
MOTOR_TASK = {
    'epoch': {
        'tmin': -5,  # Time before event (seconds)
        'tmax': 15,  # Time after event (seconds)
        'baseline': (None, 0)
    }
}

RESTING_STATE = {
    'epoch_duration': 30,  # Duration of resting state epochs (seconds)
    'epoch_overlap': 15    # Overlap between epochs (seconds)
}