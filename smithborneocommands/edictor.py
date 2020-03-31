"""Convert to an edictor application"""

from lexibank_northeuralex import Dataset
from lingpy import *

def run(args):

    ds = Dataset(args)
    wl = Wordlist.from_cldf(str(
        ds.cldf_specs().metadata_path))
    
    wl.output('tsv', filename='smith-borneo-edictor', ignore='all',
            prettify=False)
