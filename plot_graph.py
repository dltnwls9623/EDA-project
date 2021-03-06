import pandas as pd
import numpy as np
import json
import plotly
import plotly.graph_objs as go
import plotly.express as px
import plotly.figure_factory as ff
import json
import os

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
DATA = pd.read_csv(os.path.join(THIS_FOLDER, 'static/data/2015.csv'))

def draw_mapplot():
    # Numerical columns of DATA
    cols_dd = ['Happiness Score', 'GDP per Capita','Social Support', 'Life Expectancy', 'Freedom', 'Corruption','Generosity']
    # Define which trade will be visible:
    visible = np.array(cols_dd)

    # Define traces and buttons:
    traces = []
    buttons = []
    for value in cols_dd:
        traces.append(go.Choropleth(locations=DATA['Country']
                                    , locationmode='country names'
                                    , z=DATA[value].astype(float)
                                    , colorbar_title=value
                                    , visible= True if value==cols_dd[0] else False
                                    , colorscale='RdBu'
                                    , reversescale=True
                                )
                    )
        txt = f'<b>{value}<b>'
        buttons.append(dict(label=value
                            , method='update'
                            , args=[{'visible':list(visible==value)}, {'title':txt}]))

    updatemenus = [{'active':0
                    ,'buttons':buttons
                }]


    # Show figure
    fig = go.Figure(data=traces,
                    layout=dict(updatemenus=updatemenus))
    # This is in order to get the first title displayed correctly
    first_title = cols_dd[0]
    fig.update_layout(title=f"<b>{first_title}</b>")

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON


def draw_corr():
    corr = DATA[['Happiness Score', 'GDP per Capita','Social Support', 'Life Expectancy', 'Freedom', 'Corruption','Generosity']].astype(float).corr()
    l = list(corr.columns)

    fig = ff.create_annotated_heatmap(np.array(round(corr,4)), x=l, y=l, colorscale = 'RdBu', reversescale=True )
    fig.update_layout(title=f"<b>Correlation</b>")

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON


def draw_boxplot():
    q1, _, q3 = DATA['Happiness Score'].quantile([0.25,0.5,0.75])

    def category(value):
        if value < q1:
            return 'low'
        if value > q3:
            return 'high'
        else:
            return 'medium'
    
    DATA['Category'] = DATA['Happiness Score'].apply(category)    
    
    # Boxplot with dropdown menu for main features:

    fig = go.Figure()

    # Add Traces

    fig.add_trace(go.Box(x=DATA['Category'], y=DATA['GDP per Capita']))
    fig.add_trace(go.Box(x=DATA['Category'], y=DATA['Social Support'], visible=False))  
    fig.add_trace(go.Box(x=DATA['Category'], y=DATA['Life Expectancy'], visible=False))  
    fig.add_trace(go.Box(x=DATA['Category'], y=DATA['Freedom'], visible=False))  
    fig.add_trace(go.Box(x=DATA['Category'], y=DATA['Corruption'], visible=False))  
    fig.add_trace(go.Box(x=DATA['Category'], y=DATA['Generosity'], visible=False))  
    

    # Add Buttons

    fig.update_layout(
        updatemenus=[
            dict(
                active=1,
                buttons=list([ 
                    
                    dict(label='GDP',
                        method='update',
                        args=[{'visible': [True, False,False, False, False, False]},
                            {'title': '<b>Boxplot for GDP per Capita (Happiness Category split)<b>'}]),
                    
                    dict(label='Social Support',
                        method='update',
                        args=[{'visible': [False, True, False, False, False, False]},
                            {'title': '<b>Boxplot for Social Support (Happiness Category split)<b>'}]),
                    
                    dict(label='Life Expectancy',
                        method='update',
                        args=[{'visible': [False,  False, True, False, False, False]},
                            {'title': '<b>Boxplot for Health (Happiness Category split)<b>'}]),
                    
                    dict(label='Freedom',
                        method='update',
                        args=[{'visible': [False, False, False, True,  False, False]},
                            {'title': '<b>Boxplot for Freedom (Happiness Category split)<b>'}]),
                    
                    dict(label='Corruption',
                        method='update',
                        args=[{'visible': [False, False, False, False, True, False]},
                            {'title': '<b>Boxplot for Corruption (Happiness Category split)<b>'}]),
                    
                    dict(label='Generosity',
                        method='update',
                        args=[{'visible': [False, False, False, False, False,True]},
                            {'title': '<b>Boxplot for Generosity (Happiness Category split)<b>'}]),
                    
                
                ]),
            )
        ])
    fig.update_layout(title=f"<b>Boxplot for GDP per Capita (Happiness Category split)<b>")
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON


def draw_scatter():    
    cols = ['GDP per Capita','Social Support', 'Life Expectancy', 'Freedom', 'Corruption', 'Generosity']
    scatters = []
    for value in cols: 
        fig = px.scatter(DATA
                    , x = value
                    , y ="Happiness Score"
                    , size ="GDP per Capita"
                    , color ="Continent"
                    , hover_name ="Country"
                    , size_max = 15
                    )
        txt = '<b>Happiness vs ' + value + ' (sized by GDP per Capita)<b>'
        fig.update_layout(title_text=txt)
        fig.update_yaxes(range=[2,8])
        fig.update_xaxes(range=[-0.01,round((max(DATA[value]))+0.1,2)])
        scatters.append(json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder))
    
    return scatters