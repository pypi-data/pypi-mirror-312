import matplotlib.pyplot as plt
from datetime import datetime
import pickle 
import pandas as pd 
import os, sys
import pandas_datareader as pdr
script_dir = os.path.dirname(__file__)
sys.path.append(os.path.join(script_dir, '..', 'toolbox'))
sys.path.append(f"{os.path.dirname(os.path.abspath(__file__))}/../src/macroecon_tools")
from data_moments import data_moments
sys.path.append(f"{os.path.dirname(os.path.abspath(__file__))}/../src/macroecon_tools")
import __init__ as mt


def test_pddr():
    data = pd.DataFrame(pdr.get_data_fred('GS10'))
    print(data)
    print("complete")

# janus llm add my-gpt-4 --type OpenAI
# janus translate --source-lang matlab --target-lang python --input-dir janus/language/treesitter/_tests/languages --output-dir python-tests

def test_data():
    data_raw_in = os.path.join(script_dir, 'data_raw.test')
    f = open(data_raw_in, 'rb')
    dataraw = pickle.load(f)["tab"]
    f.close()
    data = mt.TimeSeries(dataraw['GDP'].dropna(), 'GDP', freq='quarterly')

test_data()