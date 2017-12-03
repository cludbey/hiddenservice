import flask
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from plotly.graph_objs import *
import pandas as pd
import urllib.request, os

directory = '/var/www/mapapp/'

mapbox_access_token = 'pk.eyJ1IjoiY29kZWVsdWRiZXkiLCJhIjoiY2phbTFwczZmMzI5bjMzbnF3cmtnZGsydiJ9.CWeBSgnwvWjd1EGK8bzeYA'

df = pd.read_csv('GEOSPATIAL.csv')

application = flask.Flask(__name__)
app = dash.Dash(__name__, server=application)
app.title = ('Crime Maps')

app.scripts.config.serve_locally = True

app.css.append_css({'external_url': "https://rawgit.com/cludbey/test/master/crim.css"})

app.layout = html.Div([
	html.Div([ #row

        html.Div([
                dcc.Graph(
                    id='map',
                    ),
                html.H6('Select Suburb'),
        		dcc.Dropdown(
        				id='suburb-selector',
        				options=[
                                {'label' : 'REDFERN','value':'REDFERN'},
                                {'label' : 'SYDNEY','value':'SYDNEY'},
                                {'label' : 'WOOLLOOMOOLOO','value':'WOOLLOOMOOLOO'},
                                {'label' : 'SURRY HILLS','value':'SURRY HILLS'},
                                {'label' : 'HAYMARKET','value':'HAYMARKET'},
                                {'label' : 'POTTS POINT','value':'POTTS POINT'},
                                {'label' : 'DARLINGHURST','value':'DARLINGHURST'},
                                {'label' : 'THE ROCKS','value':'THE ROCKS'},
                                {'label' : 'ANNANDALE','value':'ANNANDALE'},
                                {'label' : 'GLEBE','value':'GLEBE'},
                                {'label' : 'WATERLOO','value':'WATERLOO'},
                                {'label' : 'ULTIMO','value':'ULTIMO'},
                                {'label' : 'PYRMONT','value':'PYRMONT'},
                                {'label' : 'ELIZABETH BAY','value':'ELIZABETH BAY'},
                                {'label' : 'DARLINGTON','value':'DARLINGTON'},
                                {'label' : 'MOORE PARK','value':'MOORE PARK'},
                                {'label' : 'DAWES POINT','value':'DAWES POINT'},
                                {'label' : 'ALEXANDRIA','value':'ALEXANDRIA'},
                                {'label' : 'PADDINGTON','value':'PADDINGTON'},
                                {'label' : 'NEWTOWN','value':'NEWTOWN'},
                                {'label' : 'CAMPERDOWN','value':'CAMPERDOWN'},
                                {'label' : 'CHIPPENDALE','value':'CHIPPENDALE'},
                                {'label' : 'ZETLAND','value':'ZETLAND'},
                                {'label' : 'ERSKINEVILLE','value':'ERSKINEVILLE'},
                                {'label' : 'MILLERS POINT','value':'MILLERS POINT'},
                                {'label' : 'ROSEBERY','value':'ROSEBERY'},
                                {'label' : 'EVELEIGH','value':'EVELEIGH'},
                                {'label' : 'BARANGAROO','value':'BARANGAROO'},
                                {'label' : 'RUSHCUTTERS BAY','value':'RUSHCUTTERS BAY'},
                                {'label' : 'FOREST LODGE','value':'FOREST LODGE'},
                                {'label' : 'BEACONSFIELD','value':'BEACONSFIELD'},
                                {'label' : 'ST PETERS','value':'ST PETERS'},
                                {'label' : 'CENTENNIAL PARK','value':'CENTENNIAL PARK'}],
                				value='REDFERN',
                				multi=False),
                html.H6('Select Offence'),
                dcc.Dropdown(
                        id='offence-selector',
                        options=[
                                {'label' : 'Non-domestic violence related assault','value':'Non-domestic violence related assault'},
                                {'label' : 'Robbery without a weapon','value':'Robbery without a weapon'},
                                {'label' : 'Robbery with a weapon not a firearm','value':'Robbery with a weapon not a firearm'},
                                {'label' : 'Robbery with a firearm','value':'Robbery with a firearm'},
                                {'label' : 'Graffiti','value':'Graffiti'},
                                {'label' : 'Motor vehicle theft','value':'Motor vehicle theft'},
                                {'label' : 'Possession and/or use of amphetamines','value':'Possession and/or use of amphetamines'},
                                {'label' : 'Possession and/or use of cocaine','value':'Possession and/or use of cocaine'},
                                {'label' : 'Possession and/or use of ecstasy','value':'Possession and/or use of ecstasy'},
                                {'label' : 'Possession and/or use of cannabis','value':'Possession and/or use of cannabis'},
                                {'label' : 'Possession and/or use of narcotics','value':'Possession and/or use of narcotics'},
                                {'label' : 'Possession and/or use of other drugs','value':'Possession and/or use of other drugs'},
                                {'label' : 'Steal from motor vehicle','value':'Steal from motor vehicle'}],
                				value='Non-domestic violence related assault',
                				multi=False),
                    html.H6('Select Year'),
                    dcc.Dropdown(
                        id='year-selector',
                        # min='2012',
                        # max='2016',
                        # step=1,
                        # value=2012)
                        options=[
                                {'label' : '2012','value':'2012'},
                                {'label' : '2013','value':'2013'},
                                {'label' : '2014','value':'2014'},
                                {'label' : '2015','value':'2015'},
                                {'label' : '2016','value':'2016'}],
                				value='2012',
                				multi=False)
                ],className='twelve columns'),
        ],className='row'),
],className='container')


@app.callback(
Output(component_id='map', component_property='figure'),
[dash.dependencies.Input('offence-selector', 'value'), dash.dependencies.Input('suburb-selector', 'value'),
dash.dependencies.Input('year-selector', 'value')])

def update_figure(offence, suburb, year):
    #select appropriate lines
    lat=df['bcsrgclat'].loc[df['locsurb'].isin([suburb]) & df['bcsrcat'].isin([offence]) & df['incyear'].isin([year])].head(n=1000)
    lon=df['bcsrgclng'].loc[df['locsurb'].isin([suburb]) & df['bcsrcat'].isin([offence]) & df['incyear'].isin([year])].head(n=1000)
    name=df['bcsrcat'].loc[df['locsurb'].isin([suburb]) & df['bcsrcat'].isin([offence]) & df['incyear'].isin([year])].head(n=1000)

    #format for mapbox
    lat = list(map(str, lat))
    lon = list(map(str, lon))
    name = list(map(str, name))

    data = Data([
        Scattermapbox(
            lat=lat,
            lon=lon,
            mode='markers',
            marker=Marker(
                size=10
            ),
            text=name,
        )
    ])
    layout = Layout(
        autosize=True,
        hovermode='closest',
        mapbox=dict(
            accesstoken=mapbox_access_token,
            bearing=0,
            center=dict(
                lat=-33.865,
                lon=151.209
            ),
            pitch=0,
            zoom=11
        ),
    )

    fig = dict(data=data, layout=layout)


    return {
    'data': data,
    'layout': layout
    # xaxis={'title': 'Offence'},
    # yaxis={'title': 'Number'},
    # margin={'l': 40, 'b': 200, 't': 10, 'r': 100},
    # hovermode='closest'
    # )
    }

if __name__ == '__main__':
    app.run_server(debug=True)
