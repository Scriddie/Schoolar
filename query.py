import os
import sys
sys.path.append('/var/www/FlaskApps/SchoolarFlask/')
from scholarly.scholarly import scholarly
import matplotlib.pyplot as plt
import seaborn as sns
import json
import plotly
import plotly.express as px
import pandas as pd


def use_proxy():
    """ 
    Set up a ProxyGenerator object to use free proxies
    This needs to be done only once per session
    """
    from scholarly import ProxyGenerator
    pg = ProxyGenerator()
    pg.FreeProxies()
    scholarly.use_proxy(pg)


def get_author(name):
    """ get author from scholarly """
    search_query = scholarly.search_author(name)
    first_profile = next(search_query)
    author = scholarly.fill(first_profile)
    return author


def load_authors():
    """ load authors from temp directory """
    if os.path.exists('temp/authors.csv'):
        return pd.read_csv('temp/authors.csv')
    else:
        return pd.DataFrame({'Year': [], 'Citations': [], 'Researcher': []})


def add_author(author):
    """ Add new author to dataframe """
    df = load_authors()
    years, cites, researcher = [], [], []
    years += list(author['cites_per_year'].keys())
    cites += list(author['cites_per_year'].values())
    researcher += len(list(author['cites_per_year'].values()))*[author['name']]
    new_author = pd.DataFrame({'Year': years, 'Citations': cites, 'Researcher': researcher})    
    authors = pd.concat((df, new_author), axis=0)
    authors.to_csv('temp/authors.csv', index=False)


def plot_citations(df):
    """ df: contains Year, Citations, Researcher """
    fig = px.line(data_frame=df, x='Year', y='Citations', color='Researcher')
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON


if __name__ == '__main__':
    use_proxy()
    christof = get_author('Christof Seiler')
    sebastian = get_author('Sebastian Weichwald')
    plot_citations(christof, sebastian)
