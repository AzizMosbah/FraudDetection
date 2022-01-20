import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt
import contextily as ctx
import plotly.graph_objects as go

scaling = {'London': 89.6, 'South East': 91.8, 'North West': 73.4, 'West Midlands': 59.3, 'East Midlands': 48.4,
           'Yorkshire and The Humber': 55, 'East of England': 62.4, 'North East': 56.2, 'South West': 26.7}

Regions = gpd.read_file("Data/Regions/Regions__December_2017__Boundaries.shp")
LSOA = gpd.read_file(
    "Data/LSOA/Lower_Layer_Super_Output_Areas__December_2011__Boundaries_Full_Extent__BFE__EW_V3.shp")


def process_raw_shp(PATH):
    return gpd.read_file(PATH)


def add_spatial_labels(df):
    gdf = gpd.GeoDataFrame(
        df, geometry=gpd.points_from_xy(df.delivery_longitude, df.delivery_latitude), crs="EPSG:4326")
    gdf = gdf.to_crs(Regions.crs)
    gdf_r = gpd.sjoin(gdf, Regions, how='left', op='within').loc[:,
            ['order_id', 'order_amount', 'order_date', 'rgn17nm', 'geometry']]
    gdf_r = gpd.sjoin(gdf_r, LSOA, how='left', op='within').loc[:,
            ['order_id', 'order_amount', 'order_date', 'rgn17nm', 'geometry', 'LSOA11NM']]
    return gdf_r


def plot_orders_over_time(multi_index, metric, title):
    fig = go.Figure()
    for region in Regions.rgn17nm.unique():
        fig.add_trace(go.Scatter(x=multi_index['order_amount'][metric][region].index,
                                 y=multi_index['order_amount'][metric][region].values,
                                 mode='lines',
                                 name=region))
    fig.update_layout(title=title)


def agg_areas(df, group, london=False):
    conf_df = df[df.rgn17nm == 'London'].groupby(group).agg(
        {'order_amount': ['sum', 'mean', 'std', 'count']}) if london else df.groupby(group).agg(
        {'order_amount': ['sum', 'mean', 'std', 'count']})
    conf_df = conf_df.order_amount
    conf_df.columns = ["orders_total", "orders_mean", "orders_std", "orders_count"]
    conf_df['yerr'] = 1.96 * (conf_df.orders_std / np.sqrt(conf_df.orders_count))

    return conf_df


def agg_geometries(df, group, shapefile):
    tmp_df = df[df.rgn17nm == 'London'].copy() if group == 'LSOA11NM' else df

    return_df = tmp_df.groupby(group).agg({'order_amount': ['count', 'sum', 'mean']}).order_amount
    return_df.reset_index(level=0, inplace=True)
    return_df = return_df.merge(shapefile, how='left', on=group).loc[:, ['count', 'sum', 'mean', group, 'geometry']]
    return_df = gpd.GeoDataFrame(return_df, crs="EPSG:3857", geometry='geometry')

    if group == 'rgn17nm':
        for i, row in return_df.iterrows():
            return_df.iloc[i, [0]], return_df.iloc[i, [1]] = row[0] / scaling[row[3]], row[1] / scaling[row[3]]

    return return_df


def generate_barchart(df, metric, title, xlabel, ylabel, scaled=False, london=False):
    df = agg_areas(df, 'LSOA11NM', london=True) if london else agg_areas(df, 'rgn17nm')
    with plt.style.context('seaborn-whitegrid'):
        fig = plt.figure(figsize=(15, 5)) if london else plt.figure(figsize=(10, 5))
        df = df.sort_values(metric, ascending=False)

        df[metric] = df[metric] / list(scaling.values()) if scaled else df[metric]

        df = df.sort_values(metric, ascending=False)[:15]
        plt.bar(df.index, df[metric], edgecolor='black', alpha=0.7)
        plt.title(title) if not london else plt.title(title, fontsize=20)
        plt.xlabel('$\it{0}$'.format(xlabel))
        plt.ylabel('$\it{0}$'.format(ylabel))
        plt.xticks(rotation=60)
        plt.show()


def plot_london_heat(gdf_labeled):
    fig, axs = plt.subplots(2, 1, figsize=(30, 30))
    agg_geometries(gdf_labeled, 'LSOA11NM', LSOA).to_crs(epsg=3857).plot(ax=axs[0], column='count', cmap='summer',
                                                                         alpha=0.6, legend=True,
                                                                         legend_kwds={'shrink': 0.5}, vmax=6)
    ctx.add_basemap(axs[0], source=ctx.providers.CartoDB.Positron)
    axs[0].set_title('Total Orders Count per LSOA in London', fontsize=10)
    axs[0].set_axis_off()

    agg_geometries(gdf_labeled, 'LSOA11NM', LSOA).to_crs(epsg=3857).plot(ax=axs[1], column='sum', cmap='summer',
                                                                         alpha=0.6, legend=True,
                                                                         legend_kwds={'shrink': 0.5}, vmax=200)
    ctx.add_basemap(axs[1], source=ctx.providers.CartoDB.Positron)
    axs[1].set_axis_off()
    axs[1].set_title('Orders Value per LSOA in London', fontsize=10)


def plot_england_heat(gdf_labeled):
    fig, axs = plt.subplots(1, 2, figsize=(20, 10))
    agg_geometries(gdf_labeled, 'rgn17nm', Regions).to_crs(epsg=3857).plot(ax=axs[0], column='count', cmap='Reds',
                                                                           alpha=0.8, legend=True,
                                                                           legend_kwds={'shrink': 0.5})
    ctx.add_basemap(axs[0], source=ctx.providers.CartoDB.Positron)
    axs[0].set_title('Total Orders Volume per 100k Population - Region Segments', fontsize=20)
    axs[0].set_axis_off()

    agg_geometries(gdf_labeled, 'rgn17nm', Regions).to_crs(epsg=3857).plot(ax=axs[1], column='sum', cmap='Reds',
                                                                           alpha=0.8, legend=True,
                                                                           legend_kwds={'shrink': 0.5})
    ctx.add_basemap(axs[1], source=ctx.providers.CartoDB.Positron)
    axs[1].set_axis_off()
    axs[1].set_title('Total Orders Value per 100k Population - Segments', fontsize=20)
