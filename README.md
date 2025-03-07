# Neurovascular Coupling Analysis

This project combines fNIRS and EEG data to investigate neurovascular coupling using various methods:
- Time-delayed correlation between EEG bands and fNIRS amplitude
- Phase-amplitude coupling (PAC) with fNIRS as the slow signal
- EEG-informed General Linear Model (GLM)

## Project Structure

- `config/`: Configuration files for analysis parameters and data paths
- `data/`: Data handling, preprocessing, and synthetic data generation
- `methods/`: Analysis method implementations
- `analysis/`: Analysis workflows and task-specific code
- `visualization/`: Plotting and reporting utilities
- `utils/`: Helper functions and metrics
- `scripts/`: Executable analysis scripts

## Getting Started

1. Set up your environment: `pip install -r requirements.txt`
2. Configure data paths in `config/data_paths.py`
3. Run analysis scripts from the `scripts/` directory
