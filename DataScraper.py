############################################ Import Python Libraries Required ############################################ 
import numpy as np
import pandas as pd
import scipy

import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
import matplotlib.colors

import datetime
import os 
from os import path
import seaborn as sns
from scipy import signal

import warnings
warnings.filterwarnings('ignore')

import pickle

import statistics
import math 
pd.set_option('display.max_columns', 20)
pd.set_option('display.max_rows', 20)
# %config InlineBackend.figure_format = 'retina'
from PIL import Image

import tabula as tb
import re
import requests


################## Get Bulletin PDF ############# 
lastDay = 0
with open('Data/DataFrames/districts.pkl', 'rb') as f:
        district = pickle.load(f)
for k in range(18):

    url = "https://covid19.karnataka.gov.in/storage/pdf-files/EMB-NOV21//"+'{:02}'.format(k+1)+"-11-2021%20HMB%20English.pdf"
    response = requests.get(url)

    pdfFile = 'Data/PDF/November_'+'{:02}'.format(k+1)+'_2021.pdf'

    with open( pdfFile, 'wb') as f:
        f.write(response.content)

    data = tb.read_pdf(pdfFile,area=(85,20,700,580),columns=(1,40,130,190,250,320,370,420,470,520,580),pages='5',pandas_options={'header':None})

    for i in range(len(data[0][1])):
        if(data[0][1][i]=='1'):
            index = i
    SlNo = [int(x) for x in data[0][1][index:index+33] if (str(x)!='nan')]
    
    dailyPositive = [int(x) for x in data[0][3][index:index+33] if (str(x)!='nan')]

    totalPositive = [int(x) for x in data[0][4][index:index+33] if (str(x)!='nan')]
    dailyDischarge = [int(x) for x in data[0][5][index:index+33] if (str(x)!='nan')]
    totalDischarge = [int(x) for x in data[0][6][index:index+33] if (str(x)!='nan')]
    totalActive = [int(x) for x in data[0][7][index:index+33] if (str(x)!='nan')]
    dailyDeaths= [int(x) for x in data[0][8][index:index+33] if (str(x)!='nan')]
    totalDeaths= [int(x) for x in data[0][9][index:index+33] if (str(x)!='nan')]

    

    df = pd.DataFrame()
    df['SrNo'] = SlNo
    df['District'] = district
    df['Daily Positive'] = dailyPositive
    df['Total Positive'] = totalPositive
    df['Daily Discharged'] = dailyDischarge
    df['Total Discharged'] = totalDischarge
    df['Active'] = totalActive
    df['Daily Deaths'] = dailyDeaths
    df['Total Deaths'] = totalDeaths

    pklFile = "Data/DataFrames/November_"+'{:02}'.format(k+1)+ "_2021.pkl"

    open_file = open(pklFile, "wb")
    pickle.dump(df, open_file)
    open_file.close()
    lastDay+=1


open_file = open('Data/DataFrames/lastDay.pkl', "wb")
pickle.dump(lastDay, open_file)

