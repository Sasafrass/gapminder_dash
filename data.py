def give_data_year(df, what_year):
    df_year = df.query("year == @what_year")
    print(df_year.head())

    # Define all columns with their own vars
    country = df_year['country']
    pop  = df_year['pop']
    cont = df_year.continent
    exp  = df_year.lifeExp
    gdp  = df_year.gdpPercap

    # Get two dictionaries mapping continents to indices and indices to continents
    cont2i = {cont.unique()[i] : i for i in range(len(cont.unique()))}
    i2cont = {i : cont.unique()[i] for i in range(len(cont.unique()))}

    # Remap all values to the dictionary values
    cont_remap = df_year.replace({"continent": cont2i})
    cont = cont_remap.continent

    return df_year, country, pop, cont, exp, gdp, cont2i, i2cont