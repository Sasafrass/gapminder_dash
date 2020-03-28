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
from data import give_data_year

# time
start = datetime.datetime.today() - relativedelta(years=5)
end = datetime.datetime.today()

# Make a dataframe and get all relevant stuff from it
df = pd.read_csv("dataset/gapminderfive.csv")
what_year = 2007
country, pop, cont, exp, gdp, cont2i, i2cont = give_data_year(df, what_year)
pop_for_size = 0.0025 * np.sqrt(pop)

###############################################
# Make scatter plot for gdp and life expectancy
gdp_life = go.Scatter(
    x = list(gdp),
    y = list(exp),
    hovertext = list(country),
    mode = 'markers',
    marker = dict(size  = list(pop_for_size) ,
                  color = list(cont),
                  colorscale='Viridis'),
    name="gdp_life"
)

# Put scatter in list, get layout and make fig
data = [gdp_life]
layout = dict(title="Life Expectancy and GDP Per Capita",
              showlegend=False, xaxis=dict(type='log'))
fig = dict(data=data, layout=layout)
################################################


################################################

################################################

# Initialize app and style it
app = dash.Dash()
app.layout = html.Div([

    # div for banner
    html.Div([
        html.H2("Gapminder App"),
        html.Img(src="/assets/stock-icon.png")
    ], className="banner"),

    # div for dropdown
    html.Div([
        
    ])

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
            dcc.Graph(id="world-chart",
                      figure=fig)
        ], className = "six columns"),

        # Div for second graph
        html.Div([
            dcc.Graph(id="country-chart")
        ], className = "six columns"),

    ], className="row")
])

# Allow global css and use sexy eternal css
app.css.config.serve_locally = False
app.css.append_css({
    "external_url":"https://codepen.io/chriddyp/pen/bWLwgP.css"
})

# Callbacks
# Update which element first, then what part of the element
@app.callback(dash.dependencies.Output("country-chart", "figure"),
             [dash.dependencies.Input("country-input", "value")])
def update_country(input_value):
    # Select a specific country from df
    country_name = input_value.lower()
    country_name = country_name.title()
    country_df = df.query('country == @country_name')
    country_year = country_df['year']
    country_gdpPercap = country_df['gdpPercap']

    # Make line plot for single country
    country_gdp = go.Scatter(
        x = list(country_year),
        y = list(country_gdpPercap),
        name="gdp_country"
    )

    # Put the plot in list, make layout and fig
    data_country   = [country_gdp]
    country_layout = dict(
        title="GDP of {} throughout the years".format(country_name),
        showlegend=False
    )

    country_fig  =  dict(data=data_country, layout = country_layout)
    return country_fig


# Run in DEBUG mode
if __name__ == "__main__":
    app.run_server(debug=True)