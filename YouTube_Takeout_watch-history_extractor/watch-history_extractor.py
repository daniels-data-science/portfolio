#!/usr/bin/env python
# coding: utf-8

# In[2]:


import os
import re
import html
from tqdm import tqdm
import numpy as np 
import pandas as pd


# In[2]:


def scrape_watch_history_html(
    path = os.path.join('Takeout', 'YouTube and YouTube Music', 'history', 'watch-history.html')
):
    """
    This function parses Google Takeout's watch-history.html file to extract relevant data. 
    Extracted data is written to a .csv file.
    
    Parameters:
    path (str): The file path to the YouTube watch history HTML file. The default assumes the 'Takeout' folder is in the same directory
    
    Returns:
    None. A .csv file 'Youtube_history.csv' is written to disk.
    
    CSV file format:
    The resulting .csv file has the following columns:
    'timestamp','vid_title','vid_link','channel_name','channel_link'
    
    The CSV file uses a tab as a delimiter to prevent issues with commas in the data fields.
    """
    df = pd.DataFrame(
        columns=[
            'vid_link', 
            'vid_title', 
            'channel_link', 
            'channel_name', 
            'timestamp'
        ]
    )

    with open(path, 'r', encoding='utf-8') as file:
        data = file.read()

    pattern = re.compile(
        r'>Watched\xa0<a href="([^"]+)">([^>]+)</a><br><a href="([^"]+)">([^>]+)</a><br>([^>]+)</div>'
    )                         #vid_link #vid_title         #channel_link  #channel_name  #timestamp
    
    print('Collecting video entries... (this could take a while)')
    list_of_details = pattern.findall(data)
    
    for i, session in enumerate(list_of_details):

        vid_link     = session[0]
        vid_title    = session[1] 
        channel_link = session[2]
        channel_name = session[3]
        timestamp    = session[4]
        # The indices of list_of_details correspond to the groups captured in the regex pattern (round brackets)
        
        df.loc[i] = vid_link, vid_title, channel_link, channel_name, timestamp
    
    df.vid_title = df.vid_title.apply(html.unescape)
    df.channel_name = df.channel_name.apply(html.unescape)
    # html.unescape() translates HTML character reference. eg: #39; to ' 
                                     
    print(f'''
    From {df.timestamp.iloc[-1]} 
      to {df.timestamp.iloc[0]}
      
      {df.shape[0]} videos watched.
    ''')
    
    print('Exporting dataset...')
    df.to_csv(
        'Youtube_history.csv',
        encoding='utf-8',
        index = False,
        columns= ['timestamp','vid_title','vid_link','channel_name','channel_link'],
        sep ='\t' # because YouTube titles do not contain tabs
    )
    
    print('Youtube_history.csv is ready!') 


# In[6]:


while True:
    try: 
        scrape_watch_history_html()
    except Error:
        print('An error occurred')
    else:
        break
        exit()

