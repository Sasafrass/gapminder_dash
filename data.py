# Gives back a remapping for the continent column
def give_cont(df):

    # Define continent
    cont = df['continent']

    # Get two dictionaries mapping continents to indices and indices to continents
    cont2i = {cont.unique()[i] : i for i in range(len(cont.unique()))}
    #i2cont = {i : cont.unique()[i] for i in range(len(cont.unique()))}

    # Remap all values to the dictionary values
    cont_remap = df.replace({"continent": cont2i})
    cont = cont_remap['continent']

    return cont

def country_graph_data(country_name, input_value = None, df = None):

    # Depends on whether hover was used or input field
    if input_value != None:
        country_name = input_value.lower()
        country_name = country_name.title()

    # Get the years and GDP Per Capita values
    country_df = df.query('country == @country_name')
    country_year = country_df['year']
    country_gdpPercap = country_df['gdpPercap']

    return country_name, country_year, country_gdpPercap