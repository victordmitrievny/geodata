import pandas as pd
import plotly.express as px
import dash
from dash import dash_table
from dash import dcc
from dash import html
from dash import Input, Output

#Import dataframe
excel_file = pd.read_csv('wikiso.csv')
df = pd.DataFrame(excel_file)
df = df.drop('Unnamed: 0', axis=1)



#----------------------------------------------------Additional formatting----------------------------------------

#Format Country Name
for i in range(len(df)):
    df.loc[i, "Country Name"] = df.loc[i, "Country Name"].replace('(the)','')

#Format Population
for i in range(len(df)):
    df.loc[i, "Population"] = df.loc[i, "Population"].replace(',','').split('or')[0]

#Format Density
df["Density"] = df["Density"].astype(str)
for i in range(len(df)):
    df.loc[i, "Density"] = df.loc[i, "Density"].replace(',','').split('.')[0].replace('n/a','0').replace('nan','0')



df["Population"] = df["Population"].astype(int)
df["Density"] = df["Density"].astype(int)





#----------------------------------------------Visualization---------------------------------

#Code for fixed rows in Datatable
columns_fixed = []
for i in df.columns:
  columns_fixed.append(i)


#-------Initiation and Layout
vis = dash.Dash()

vis.layout = html.Div([

  html.H1('Geo Data', style={'textAlign': 'center'}),

  #Dropdown
  dcc.Dropdown(['Population', 'Density'], id='dropdown'),

  #Map
  dcc.Graph(
    id = 'map',
    figure = 0,
    style={'width': '100%', 'height': '600px', 'margin-left': '100px'}                                      
  ),

  #Bar Chart
  dcc.Graph(
    id = 'barchart',
    figure = 0                                       
  ),
   
  #Datatable
  dash_table.DataTable(
    data=df.to_dict('records'),
    columns = [{"name": i, "id": i} for i in df.columns],
    sort_action = "native",
    virtualization = True,
    page_size = 250,    
    fixed_rows={'headers': True, 'data': columns_fixed},

    style_header={
            'backgroundColor': 'rgb(230, 230, 230)',
            'fontWeight': 'bold'
        },

    style_cell={
            'minWidth': '150px',
            'maxWidth': '150px',
            #'whiteSpace': 'normal',
            #'overflow': 'hidden',
            'textOverflow': 'ellipsis'
        },
    
    #Custom column width
    style_data_conditional=[
            {'if': {'column_id': 'Country Name'}, 'minWidth': '300px'},
            {'if': {'column_id': 'Capital'}, 'minWidth': '300px'},
            {'if': {'column_id': 'Government'}, 'minWidth': '300px'},
            {'if': {'column_id': 'Population'}, 'minWidth': '150px'},
            {'if': {'column_id': 'Density'}, 'minWidth': '150px'},
            {'if': {'column_id': 'Area'}, 'minWidth': '150px'},
            {'if': {'column_id': 'Water'}, 'minWidth': '75px'},
            {'if': {'column_id': 'HDI'}, 'minWidth': '100px'},
            {'if': {'column_id': 'Gini'}, 'minWidth': '100px'},
            {'if': {'column_id': 'Currency'}, 'minWidth': '250px'},
            {'if': {'column_id': 'Top Traded Currency'}, 'minWidth': '150px'},
            {'if': {'column_id': 'ISO'}, 'minWidth': '50px'},
            {'if': {'column_id': 'ISO3'}, 'minWidth': '50px'}
            ]

    # style_table={
    #         'table-layout': 'fixed'}
  )

])




#----------------------Callbacks
@vis.callback(
    Output('map', 'figure'),
    Output('barchart', 'figure'),
    Input('dropdown', 'value'),
)

def update_output_value(input_value):

  #Map 
  map1 = px.choropleth(df,
                      locations = 'ISO3',
                      color = input_value,
                      color_continuous_scale=[[0, 'rgb(240,240,240)'],
                        [0.05, 'rgb(13,136,198)'],
                        [0.1, 'rgb(191,247,202)'],
                        [0.20, 'rgb(4,145,32)'],
                        [1, 'rgb(227,26,28,0.5)']],
                      scope = 'world',
                      featureidkey = 'ISO3'
                      )
  if input_value == "Density":
    map1.update_layout(coloraxis=dict(cmin=0, cmax=800))

  #Bar Chart
  dfbarchart = df.head(15)
  fig = px.bar(dfbarchart, x = 'Country Name', y = input_value)

  return map1, fig



if __name__ == '__main__':
  vis.run_server()
    
server = vis.server

#map.show()





#---------------------------SOME COUNTRIES ARE MISSING AT THE STAGE OF MERGING TABLES - SOMALILAND SPECIFICALLY


