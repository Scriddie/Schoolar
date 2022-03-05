import os
import sys
from threading import local

from bibtexparser import load
sys.path.append('/var/www/FlaskApps/SchoolarFlask/')
from scholarly.scholarly import scholarly, ProxyGenerator
import matplotlib.pyplot as plt
import seaborn as sns
import json
import plotly
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import pickle as pk
from collections import Counter


def temp_dir(user_id, local=False):
    if local:
        return f'temp/{user_id}.pk'
    else:
        return f'/var/www/FlaskApps/SchoolarFlask/temp/{user_id}.pk'


def create_user_storage(user_id, local=False):
    df = pd.DataFrame({'Year': [], 'Citations': [], 'Researcher': []})
    author_data = {'names': [],
                   'other_cites': [],
                   'first_author_cites': [],
                   'df': df}
    with open(temp_dir(user_id, local=local), 'wb') as fp:
    	pk.dump(author_data, fp)
    # df.to_csv(temp_dir(user_id, local=local))


def use_proxy():
    """ 
    Set up a ProxyGenerator object to use free proxies
    This needs to be done only once per session
    """
    pg = ProxyGenerator()
    pg.FreeProxies()
    scholarly.use_proxy(pg)


def get_author(name):
    """ get author from scholarly """
    search_query = scholarly.search_author(name)
    try:
        first_profile = next(search_query)
        author = scholarly.fill(first_profile, sections=['basics', 'citations', 'counts', 'publications'])
        return author
    except StopIteration:
        None


def load_authors(user_id, local=False):
    """ load authors from temp directory """
    with open(temp_dir(user_id, local=local), 'rb') as fp:
        author_data = pk.load(fp)
    return author_data
    # return pd.read_csv(temp_dir(user_id, local=local))


def contains_all(string, substring):
    c1, c2 = Counter(string), Counter(substring)
    return all(c1[x] >= c2[x] for x in c2)


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
    for p in author['publications']:
        # TODO not sure if best criterion
        if contains_all(author['name'], p['bib']['author'].split(' and')[0]):
            first_author_cites += p['num_citations']
    other_cites = author['citedby'] - first_author_cites

    author_data = {
        'names': author_data['names']+[author['name']],
        'other_cites': author_data['other_cites']+[other_cites],
        'first_author_cites': author_data['first_author_cites']+[first_author_cites],
        'df': df
    }

    with open(temp_dir(user_id, local=local), 'wb') as fp:
    	pk.dump(author_data, fp)
    


def plot_citations(author_data, show=False):
    """ df: contains Year, Citations, Researcher """
    df = author_data['df']
    # fig = make_subplots(rows=2, cols=1)
    
    # # cites per year
    # fig.append_trace(
    #     go.Scatter(x=df['Year'], y=df['Citations'], fill=df['Researcher']), 
    #     # px.line(data_frame=df, x='Year', y='Citations', color='Researcher'), 
    # row=1, col=1)
        # # total cites
    # fig.append_trace(
    #     go.Bar(x=author_data['names'], y=author_data['cites']), 
    # row=2, col=1)
    # fig.append_trace(go.Bar(
    #     x=author_data['names'], y=author_data['first_author_cites']), 
    # row=2, col=1)

    ###
    # fig = px.line(data_frame=df, x='Year', y='Citations', color='Researcher')
    ###

    df_bar = pd.DataFrame({
        'Researcher': author_data['names'],
        'Other citations': author_data['other_cites'],
        'First-author citations': author_data['first_author_cites'],
    })
    df_bar_long = pd.melt(df_bar, 
        id_vars=['Researcher'], value_name ='Citations', var_name='Citation Type')
    df_bar_long.sort_values(by='Citation Type', inplace=True)
    fig = px.bar(data_frame=df_bar_long, 
        x='Researcher', y='Citations', color='Citation Type')

    if show:
        fig.show()
    else:
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return graphJSON


if __name__ == '__main__':
    # use_proxy()
    user_id = 1
    create_user_storage(user_id, local=True)
    add_author(get_author('Sebastian Weichwald'), user_id, local=True)
    # add_author(get_author('Christof Seiler Maastricht'), user_id, local=True)
    author_data = load_authors(user_id, local=True)
    plot_citations(author_data, show=True)