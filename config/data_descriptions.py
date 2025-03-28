# Motor tapping task metadata
TAPPING_METADATA = {
    'subject': '',              # Subject ID or code
    'hand': '',                 # 'L'/'R'/'both'
    'device': '',               # 'button'/'light_barrier'/'accelerometer'
    'isi': 0,                   # Inter-stimulus interval in seconds
    'tapping_length': 0,        # Duration of tapping period in seconds
    'cue_type': '',             # 'visual'/'auditory'/'both'
    'trials_per_hand': 0,       # Number of trials per hand
    'date': '',                 # Recording date
    'tapping_rate': 0,          # If externally paced, frequency in Hz
}

# Resting state metadata
RESTING_METADATA = {
    'subject': '',              # Subject ID or code
    'eyes': '',                 # 'open'/'closed'/'alternating'
    'position': '',             # 'sitting'/'supine'
    'duration': 0,              # Total duration in seconds
    'date': '',                 # Recording date
}