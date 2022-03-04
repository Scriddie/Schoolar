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
    # Get an iterator for the author results
    search_query = scholarly.search_author(name)
    first_profile = next(search_query)
    author = scholarly.fill(first_profile)
    return author


def add_author(df, author):
    if df is None:
         df = pd.DataFrame({'Citations': [], 'Year': [], 'Researcher': []})
<form method="POST">
    <input name="text">
    <input type="submit">
</form>


def plot_citations(authors):
    """ authors: list of authors """
    years, cites, researcher = [], [], []
    for a in authors:
        years += list(a['cites_per_year'].keys())
        cites += list(a['cites_per_year'].values())
        researcher += len(list(a['cites_per_year'].values())) * [a['name']]

    df = pd.DataFrame({'Year': years, 'Citations': cites, 'Researcher': researcher})
    fig = px.line(data_frame=df, x='Year', y='Citations', color='Researcher')
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON
    # plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)
    # plt.tight_layout()
    # plt.show()


if __name__ == '__main__':
    use_proxy()
    christof = get_author('Christof Seiler')
    sebastian = get_author('Sebastian Weichwald')
    plot_citations(christof, sebastian)
