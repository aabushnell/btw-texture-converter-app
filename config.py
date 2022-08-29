import pandas as pd

# source file for texture mappings
TEXTURE_MAP = pd.read_csv('map.csv', index_col=0)

# folders for pack i/o
INPUT_FOLDER = 'packs/input/'
OUTPUT_FOLDER = 'packs/output/'
