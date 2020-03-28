# Imports
import numpy as np 
import pandas as pd 

# Dash-y
import dash
import dash_core_components as dcc
import dash_html_components as html 
from dash.dependencies import Output, Input

# Plotly objects
import plotly.graph_objs as go

# Datetime shizz
import datetime
from dateutil.relativedelta import relativedelta

# Relative imports
from data import give_cont
from data import country_graph_data

# time
start = datetime.datetime.today() - relativedelta(years=5)
end = datetime.datetime.today()

# Make a dataframe
df = pd.read_csv("dataset/gapminderfive.csv")
df_for_id = df.query("year == 1952")

# Mapping of cols <--> names
cols2name = {'country':'country', 'year':'year', 'pop':'population', 'continent':'continent',
             'lifeExp':'Life Expectancy', 'gdpPercap':'GDP Per Capita'}
name2cols = {'country':'country', 'year':'year', 'population':'pop', 'continent':'continent',
             'Life Expectancy':'lifeExp', 'GDP Per Capita':'gdpPercap'}

# Dropdown options
options_x = [{'label':cols2name[col], 'value':cols2name[col]} for col in df.columns]
options_y = [{'label':cols2name[col], 'value':cols2name[col]} for col in df.columns]

# Initialize app and style it
app = dash.Dash()
app.layout = html.Div([

    # div for banner
    html.Div([
        html.H2("Gapminder App"),
        html.Img(src="/assets/stock-icon.png")
    ], className="banner"),

    # div for first dropdown
    html.Div(
        dcc.Dropdown(
            id = "x-axis",
            options = options_x,
            value = "GDP Per Capita"
        )
    ),

    # div for second dropdown
    html.Div(
        dcc.Dropdown(
            id = "y-axis",
            options = options_y,
            value = "Life Expectancy"
        )
    ),

    # div for input box
    html.Div([
        dcc.Input(
            id="country-input",
            value="Netherlands",
            type="text"
        )
    ]),

    # div for external css
    html.Div([

        # Main gapminder graph
        html.Div([
            dcc.Graph(id="world-chart")
        ], className = "six columns"),

        # Div for second graph
        html.Div([
            dcc.Graph(id="country-chart")
        ], className = "six columns"),

    ], className="row"),

    # div for slider
    html.Div([
        dcc.Slider(
            id = "world-slider",
            min = df['year'].min(),
            max = df['year'].max(),
            value = df['year'].min(),
            marks = {str(year): str(year) for year in df['year'].unique()},
            step = None,
            updatemode='drag'
        )
    ], className = "six columns")
])

# Allow global css and use sexy eternal css
app.css.config.serve_locally = False
app.css.append_css({
    "external_url":"https://codepen.io/chriddyp/pen/bWLwgP.css"
})

# Callbacks
# Update which element first, then what part of the element
# The function underneath the decorator takes all arguments for its inputs

# Callback for dropdowns to generate world graph
@app.callback(dash.dependencies.Output("world-chart", "figure"),
              [Input('x-axis', 'value'),
               Input('y-axis', 'value'),
               Input('world-slider', 'value')])
def update_world(input_x, input_y, year_slider):

    # Dropdowns contain fancy names, so rename first
    x_axis = name2cols[input_x]
    y_axis = name2cols[input_y]

    # Get the right data
    df_year = df.query("year == @year_slider")
    cont = give_cont(df_year)

    # Size of population for graph
    pop_for_size = 0.0025 * np.sqrt(df_year['pop'])
    
    # Make scatter plot with all stuff
    gdp_life = go.Scatter(
        x = list(df_year[x_axis]),
        y = list(df_year[y_axis]),
        hovertext = list(df_year['country']),
        mode = 'markers',
        marker = dict(size  = list(pop_for_size) ,
                    color = list(cont),
                    colorscale='Viridis'),
        name="gdp_life"
    )

    # Put scatter in list, get layout and make fig
    data = [gdp_life]
    title = "{} and {}".format(input_y, input_x)
    layout = dict(title=title,
                showlegend=False, 

                # Define ranges such that animation works smoothly
                xaxis={
                    'type':'log',
                    'title':input_x,
                    'range':[2.3,4.8]
                },
                yaxis={
                    'title':input_y,
                    'range':[20,90]
                },

                # Transition
                transition = {'duration': 500})
    world_fig = dict(data=data, layout=layout)

    return world_fig


# Callback for input field and country chart
@app.callback(dash.dependencies.Output("country-chart", "figure"),
             [dash.dependencies.Input("country-input", "value"),
              Input('world-chart', 'hoverData')])
def update_country(input_value, hoverData):

    # Print the hoverdata to see how that works
    # If we get data from hovering, use that data to update graph
    if hoverData != None:
        hover_dict = hoverData['points'][0]
        country_id = hover_dict['pointIndex']

        # Set all variables for the country graph update
        country_name = df_for_id['country'].iloc[country_id]
        country_name, country_year, country_gdpPercap = country_graph_data(country_name = country_name, df = df)

        # Set hoverData to None again to prevent issues with graph update
        hoverData = None

    # .. Otherwise use input field to select a specific country from df
    else:
        country_name, country_year, country_gdpPercap = country_graph_data(country_name = input_value, 
                                                                           input_value = input_value,
                                                                           df = df)

    # Make line plot for single country
    country_gdp = go.Scatter(
        x = list(country_year),
        y = list(country_gdpPercap),
        name="gdp_country",
    )

    # Put the plot in list, make layout and fig
    data_country   = [country_gdp]
    country_layout = dict(
        title="GDP of {} throughout the years".format(country_name),
        showlegend=False,

        # Set x and y range for smoother animation
        xaxis={
            'title':'Year',
            'range':[1950, 2010]
        },
        yaxis={
            'title': 'GDP Per Capita',
            'range': [1000, 50000]
        }
        ,transition = {'duration':500, 'easing': 'cubic-in-out'}
    )

    country_fig  =  dict(data=data_country, layout = country_layout)
    return country_fig

# Run in DEBUG mode
if __name__ == "__main__":
    app.run_server(debug=True)
