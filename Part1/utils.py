import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.colors import ListedColormap, BoundaryNorm
import matplotlib.dates as mdates
import matplotlib.patches as mpatches
import numpy as np
import plotly.express as px



def process_raw(PATH="Data/task1_transport_data.csv"):
    return pd.read_csv(PATH)


def fix_dates(df):
    tmp_df = df.copy()
    tmp_df.iloc[440, 0] = '2013-03-17'
    tmp_df.iloc[608, 0] = '2013-09-01'
    tmp_df.iloc[14, 0] = '2012-01-16'
    tmp_df.date = pd.to_datetime(tmp_df.date, format="%Y-%m-%d").dt.date

    return tmp_df


def fix_circumstance(df):
    tmp_df = df.copy()
    tmp_df.iloc[347, 2] = 'rainy'
    tmp_df.circumstance = tmp_df.circumstance.str.lower()
    tmp_df.loc[df.circumstance == 'dr', ['circumstance']] = 'dry'
    return tmp_df


def plot_time_series(df):
    num_classes = 4
    ts = range(len(df))
    numerical_labels = df.replace({'circumstance': {'dry': 0, 'rainy': 1, 'very_rainy': 2, 'strike': 3}}).circumstance

    cmap = ListedColormap(['green', 'orange', 'blue', 'red'])
    norm = BoundaryNorm(range(num_classes + 1), cmap.N)
    points = np.array([df.index, df.orders]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)

    lc = LineCollection(segments, cmap=cmap, norm=norm)
    lc.set_array(numerical_labels)

    with plt.style.context('seaborn-whitegrid'):
        fig = plt.figure(figsize=(20, 10))
        ax = plt.gca().add_collection(lc)
        plt.xlim(df.index.min(), df.index.max())
        plt.ylim(df.orders.min() - 500, df.orders.max() + 500)
        plt.gca().spines['top'].set_visible(False)
        plt.gca().spines['right'].set_visible(False)
        plt.xticks(df.index, df.date)
        plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=60))
        plt.gcf().autofmt_xdate()
        plt.title("Volume of Orders Over Time - Circumstance Segmentation by Color")
        plt.xlabel('$\it{Date}$')
        plt.ylabel('$\it{Orders\ Volume}$')
        green_patch, orange_patch, blue_patch, red_patch = mpatches.Patch(color='green', label='dry'), mpatches.Patch(
            color='orange', label='rainy'), mpatches.Patch(color='blue', label='very rainy'), mpatches.Patch(
            color='red', label='strike')
        plt.legend(handles=[green_patch, orange_patch, blue_patch, red_patch], loc='lower right')


def plot_hist_circ(density_df):
    fig = px.histogram(density_df[density_df.circumstance != 'strike'], x="orders", color="circumstance",
                       marginal="box",  # or violin, rug
                       barmode='overlay',
                       histnorm='probability',
                       opacity=.4,
                       nbins=40,
                       color_discrete_sequence=['orange', 'green', 'royalblue']
                       )
    return fig


def plot_mean_volumes(density_df):
    conf_df = density_df[density_df.circumstance != 'strike'].groupby('circumstance').agg(
        {'orders': ['mean', 'std', 'count']})
    conf_df = conf_df.orders
    conf_df.columns = ["orders_mean", "orders_std", "orders_count"]
    conf_df['yerr'] = 1.96 * (conf_df.orders_std / np.sqrt(conf_df.orders_count))

    with plt.style.context('seaborn-whitegrid'):
        fig = plt.figure(figsize=(10, 5))
        plt.bar(conf_df.index, conf_df.orders_mean, yerr=conf_df.yerr, edgecolor='black',
                color=['orange', 'green', 'blue'], alpha=0.7)
        plt.axhline(y=conf_df['orders_mean']['dry'], zorder=0, linewidth=2, color='red')
        plt.title("Mean Volume of Orders per Day - Circumstance Segmentation by Color", fontsize=15)
        green_patch, orange_patch, blue_patch, red_patch = mpatches.Patch(color='green', label='dry'), mpatches.Patch(
            color='orange', label='rainy'), mpatches.Patch(color='blue', label='very rainy'), mpatches.Patch(
            color='red', label='Mean Volume of Orders on dry days')
        plt.legend(handles=[green_patch, orange_patch, blue_patch, red_patch], bbox_to_anchor=(1.1, 1.05))
        plt.xlabel('$\it{circumstance}$')
        plt.ylabel('$\it{mean orders volume}$')


def add_temporal_features(df):
    tmp_df = df.copy()
    tmp_df['month'] = tmp_df.date.apply(lambda x: x.month)
    tmp_df['weekday'] = tmp_df.date.apply(lambda x: x.weekday())

    return tmp_df


def plot_monthly_mean(density_df):
    conf_df = density_df[density_df.circumstance != 'strike'].groupby('month').agg({'orders': ['mean', 'std', 'count']})
    conf_df = conf_df.orders
    conf_df.columns = ["orders_mean", "orders_std", "orders_count"]
    conf_df['yerr'] = 1.96 * (conf_df.orders_std / np.sqrt(conf_df.orders_count))

    with plt.style.context('seaborn-whitegrid'):
        fig = plt.figure(figsize=(14, 7))
        plt.bar(conf_df.index, conf_df.orders_mean, yerr=conf_df.yerr, edgecolor='black', alpha=0.7)
        plt.axhline(y=density_df.orders.mean(), zorder=0, linewidth=2, color='red')
        plt.title("Mean Volume of Orders - Month Segmentation by Color")
        plt.xlabel('$\it{Months}$')
        plt.ylabel('$\it{mean\ orders\ volume}$')


def add_previous_days(df, window_size=4):
    tmp_df = df.sort_values('date')
    for i in range(window_size):
        tmp_df['orders_lag_{0}'.format(i + 1)] = tmp_df.orders.shift(i + 1)
    return tmp_df


def very_rainy(df):
    tmp_df = df
    tmp_df.circumstance = tmp_df.circumstance.replace(['dry', 'rainy', 'strike', 'very_rainy'], [0, 0, 0, 1])
    return tmp_df


def bundle_months(df):
    tmp_df = df
    tmp_df['month_cat'] = tmp_df.date.apply(lambda x: x.month)
    tmp_df.month_cat = tmp_df.month_cat.replace([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
                                                [-1, -1, 0, 1, 1, 1, 0, -1, -1, 0, 1, 0])
    return tmp_df
