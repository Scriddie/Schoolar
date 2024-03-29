""" 
Query google scholar for information on a given researcher;
Visualize results;
"""
import os
import sys
PARENT_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append(PARENT_DIR)
from scholarly.scholarly import scholarly, ProxyGenerator
import json
import plotly
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import pickle as pk
from collections import Counter
from datetime import datetime


def new_user_id(local=False):
    temp_folder = 'temp' if local else f'{PARENT_DIR}/temp'
    if not os.path.exists(temp_folder):
        os.mkdir(temp_folder)
    prev_users = [0] + [int(i.split('.')[0]) for i in os.listdir(temp_folder)]
    return str(max(prev_users) + 1)


def temp_dir(user_id, local=False):
    temp_folder = 'temp' if local else f'{PARENT_DIR}/temp'
    if not os.path.exists(temp_folder):
        os.mkdir(temp_folder)
    return f'{temp_folder}/{user_id}.pk'


def create_user_storage(user_id, local=False):
    df = pd.DataFrame({'Year': [], 'Citations': [], 'Researcher': []})
    author_data = {'names': [],
                   'other_cites': [],
                   'first_author_cites': [],
                   'last_author_cites': [],
                   'df': df}
    with open(temp_dir(user_id, local=local), 'wb') as fp:
    	pk.dump(author_data, fp)


def use_proxy():
    """ 
    Set up a ProxyGenerator object to use free proxies
    This needs to be done only once per session
    """
    pg = ProxyGenerator()
    pg.FreeProxies()
    scholarly.use_proxy(pg)


def get_author(name):
    """ get author from scholarly 
    args:
        name: Search string for authors
    returns:
        author: first profile
        profiles: String consisting of all profiles
    """
    search_query = scholarly.search_author(name)
    profiles = [i for i in search_query]
    profile_names = [i['name']+', '+i['affiliation'] for i in profiles]
    if len(profiles) == 0:
        return None, ""
    elif len(profiles) > 1:
        # not unique, return names
        return None, profile_names
    else:
        # unique profile
        first_profile = profiles[0]
        author = scholarly.fill(first_profile, sections=['basics', 'citations', 'counts', 'publications'])
        return author, profile_names


def load_authors(user_id, local=False):
    """ load authors from temp directory """
    with open(temp_dir(user_id, local=local), 'rb') as fp:
        author_data = pk.load(fp)
    return author_data
    # return pd.read_csv(temp_dir(user_id, local=local))


def contains_enough(string, substring):
    # TODO Note that this may fail in some instances
    c1, c2 = Counter(string), Counter(substring)
    if len(c2) == 0:  # No author information found
        return False
    comparison = [c1[x] >= c2[x] for x in c2]
    return (sum(comparison) / len(c2)) > 0.8


def add_author(author, user_id, local=False):
    """ Save new author info """

    # store cite per year info
    author_data = load_authors(user_id, local=local)
    df = author_data['df']
    years, cites, researcher = [], [], []
    years += list(author['cites_per_year'].keys())
    cites += list(author['cites_per_year'].values())
    researcher += len(list(author['cites_per_year'].values()))*[author['name']]
    new_author = pd.DataFrame({'Year': years, 'Citations': cites, 'Researcher': researcher})    
    df = pd.concat((df, new_author), axis=0)
    
    # first author cites / other cites
    first_author_cites = 0
    last_author_cites = 0
    for p in author['publications']:
        authors = p['bib']['author'].split(', ')
        first_author = authors[0]
        last_author = authors[-1]
        if contains_enough(author['name'], first_author):
            first_author_cites += p['num_citations']
        elif contains_enough(author['name'], last_author):
            last_author_cites += p['num_citations']
        else:
            pass
    # TODO can result in negative numbers if there are different versions of the same publication
    other_cites = author['citedby'] - first_author_cites - last_author_cites

    author_data = {
        'names': author_data['names']+[author['name']],
        'other_cites': author_data['other_cites']+[other_cites],
        'first_author_cites': author_data['first_author_cites'] + [first_author_cites],
        'last_author_cites': author_data['last_author_cites'] + [last_author_cites],
        'df': df
    }

    with open(temp_dir(user_id, local=local), 'wb') as fp:
    	pk.dump(author_data, fp)
    


def plot_cite_timeline(author_data, show=False):
    """
    Citations per year per researcher
    args:
        author_data: dict containing author details
    returns:
        timelineJSON: JSON of timeline plot
    """
    # TODO keep user order of added researchers!
    df = author_data['df']
    y = datetime.now().year
    df_current = df.loc[df['Year']==y, :]
    df_before = df.loc[df['Year']!=y, :]
    if df_before.shape[0] == 1:  # no line with just one entry
        timeline = px.scatter(data_frame=df_before, x='Year', y='Citations', color='Researcher')
    else:
        timeline = px.line(data_frame=df_before, x='Year', y='Citations', color='Researcher')
    try:
        current = px.scatter(data_frame=df_current, x='Year', y='Citations', color='Researcher')
        for i in current.data:
            i['showlegend']=False
            timeline.add_trace(i)
    except IndexError:
        pass

    if show:
        timeline.show()
    else:
        timelineJSON = json.dumps(timeline, cls=plotly.utils.PlotlyJSONEncoder)
        return timelineJSON


def plot_cite_type(author_data, show=False):
    """
    Stacked bar plot of researcher citations by type
    args:
        author_data: dict containing author details
    returns:
        barJSON: JSON of bar plot
    """
    df_bar = pd.DataFrame({
        'Researcher': author_data['names'],
        'Other citations': author_data['other_cites'],
        'First-author citations': author_data['first_author_cites'],
        'Last-author citations': author_data['last_author_cites']
    })
    df_bar_long = pd.melt(df_bar, 
        id_vars=['Researcher'], value_name ='Citations', var_name='Citation Type')
    df_bar_long.sort_values(by='Citation Type', inplace=True)
    bar = px.bar(data_frame=df_bar_long, 
        x='Researcher', y='Citations', color='Citation Type',
        color_discrete_sequence=px.colors.qualitative.G10)
    if show:
        bar.show()
    else:
        barJSON = json.dumps(bar, cls=plotly.utils.PlotlyJSONEncoder)
        return barJSON


def plot_cite_gini(author_data, show=False):
    """ 
    GINI curves for all authors
    args:
        author_data: dict containing author details
    returns:
        barJSON: JSON of bar plot
    """
    # TODO plot concentration of citations
    pass



if __name__ == '__main__':
    # use_proxy()
    user_id = new_user_id()
    create_user_storage(user_id, local=True)
    author, profiles = get_author('Sebastian Weichwald')
    add_author(author, user_id, local=True)
    author_data = load_authors(user_id, local=True)
    plot_cite_type(author_data, show=True)