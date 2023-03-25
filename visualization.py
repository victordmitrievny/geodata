import pandas as pd
import plotly.express as px
import plotly.graph_objs as pxgo
import dash
from dash import dash_table
from dash import dcc
from dash import html
from dash import Input, Output
from sqlalchemy import create_engine


#Import data from the MySQL server to the DataFrame
engine = create_engine('mysql+pymysql://root:@localhost/geodata')
df = pd.read_sql_table('geodata_iso', engine)


#----------------------------------------------Visualization---------------------------------

#Code for fixed rows in Datatable
columns_fixed = []
for i in df.columns:
  columns_fixed.append(i)
labels = ['Category A', 'Category B', 'Category C']
values = [50, 25, 25]

#------------------------------------------Initiation and Layout
vis = dash.Dash()

html.Br()

vis.layout = html.Div([
  
  html.H1('Geo Data', style={'textAlign': 'center'}),

  html.Br(),

  #Dropdown

  html.Div([
    dcc.Dropdown(['Population', 'Density', 'Area','Water %', 'Top Traded Currency', 'GDP Total', 'GDP Per Capita', 'HDI', 'Gini', 
                  'Christianity', 'Islam', 'Hinduism', 'Buddhism', 'Judaism'], 
                  id='dropdown', value = 'Population',
                  style={'width': '1000px'}
                  )
             ],
             style={'margin-left':'20%', 'margin-bottom':'30px'}),
  
  #Div for single country info + Map
  html.Div([
    
    #Info for single country
    html.Div( 
      [
        html.H2('Country Information', 
                style={'textAlign': 'center',
                        'margin': 3,
                      }
               ),

        html.H3('-', id = 'p_country_name', 
                style={'textAlign': 'center',
                       'font-weight': 'bold',
                        'margin-top': 20,
                      }
               ),    
       
        #Div for Capital
        html.Div([
          html.P('Capital:', style = {'font-weight': 'bold', 'margin': '5px 10px 5px 4px'}),
          html.P(id = 'p_capital', style = {'margin': '5px 15px 5px 99px'}),
        ],
          style = {'display': 'flex'}),

        #Div for Head of Governmnent
        html.Div([
          html.P('Head of Government:', style = {'font-weight': 'bold', 'margin': '5px 10px 5px 5px','min-width': '150px'}),
          html.P(id = 'p_government', style = {'margin': '5px 15px 5px 3px'}),
        ],
          style = {'display': 'flex'}),
        
        #Div for Currency
        html.Div([
          html.P('Currency:', style = {'font-weight': 'bold', 'margin': '5px 10px 5px 5px'}),
          html.P(id = 'p_currency', style = {'margin': '5px 15px 5px 83px'}),
        ],
          style = {'display': 'flex'}),

        #Div for Population
        html.Div([
          html.P('Population:', style = {'font-weight': 'bold', 'margin': '5px 10px 5px 5px'}),
          html.P(id = 'p_population', style = {'margin': '5px 15px 5px 73px'}),
        ],
          style = {'display': 'flex'}),          

        #Div for Density
        html.Div([
          html.P('Density:', style = {'font-weight': 'bold', 'margin': '5px 10px 5px 5px'}),
          html.P(id = 'p_density', style = {'margin': '5px 15px 5px 96px'}),
        ],
          style = {'display': 'flex'}),    

        #Div for Area
        html.Div([
          html.P('Area:', style = {'font-weight': 'bold', 'margin': '5px 10px 5px 5px'}),
          html.P(id = 'p_area', style = {'margin': '5px 15px 5px 113px'}),
        ],
          style = {'display': 'flex'}),   

        #Div for Water
        html.Div([
          html.P('Water %:', style = {'font-weight': 'bold', 'margin': '5px 10px 5px 5px'}),
          html.P(id = 'p_water', style = {'margin': '5px 15px 5px 83px'}),
        ],
          style = {'display': 'flex'}),   

        #Div for GDP Total
        html.Div([
          html.P('GDP Total:', style = {'font-weight': 'bold', 'margin': '5px 10px 5px 5px'}),
          html.P(id = 'p_gdp', style = {'margin': '5px 15px 5px 73px'}),
        ],
          style = {'display': 'flex'}),   

        #Div for GDP Per Capita
        html.Div([
          html.P('GDP Per Capita:', style = {'font-weight': 'bold', 'margin': '5px 10px 5px 5px'}),
          html.P(id = 'p_gdp_pc', style = {'margin': '5px 15px 5px 33px'}),
        ],
          style = {'display': 'flex'}),   

        #Div for HDI
        html.Div([
          html.P('HDI:', style = {'font-weight': 'bold', 'margin': '5px 10px 5px 5px'}),
          html.P(id = 'p_hdi', style = {'margin': '5px 15px 5px 114px'}),
        ],
          style = {'display': 'flex'}),   

        #Div for Gini
        html.Div([
          html.P('Gini:', style = {'font-weight': 'bold', 'margin': '5px 10px 5px 5px'}),
          html.P(id = 'p_gini', style = {'margin': '5px 15px 5px 113px'}),
        ],
          style = {'display': 'flex'}),   

        #Div for Religion container and graph
        html.Div([
          dcc.Graph(
                      id='pie_chart',
                      figure={
                              'data': [pxgo.Pie(values = values, 
                                                labels = labels,
                                                textposition='inside')],
                              'layout': pxgo.Layout(title = { 'text': '<b>Religion:</b>', 
                                                            'font': {
                                                                      'family': 'Open Sans',
                                                                      'size': 16,   
                                                                      'color': 'black'
                                                                    },
                                                            'y': 0.95
                                                             },
                                                    width = 320,
                                                    height = 320,
                                                    margin = dict(t=0, b=70),
                                                    legend = {
                                                              'x': 1.0,
                                                              'y': 0.5
                                                             },
                                                    paper_bgcolor='rgba(255,255,255,0)'
                                                    )
                                },
                      style={'margin': {'top': 0, 'bottom': 0, 'left': 0, 'right': 0}}
                    ),

                  ],
        style = {'height':'230px', 'border': '2px solid black'}),

        html.Div(style = {'height':'100px'})
      
      ],
        style = {
              'border': '2px solid black',
              'height': '500px',
              'width': '25%',
              'overflowY': 'scroll'
                },
                
            ),
    
    #Separator
    html.Div(style={'width': '5px'}),

    #Map
    dcc.Graph(  
                id = 'map',
                style={
                    'border': '2px solid black',
                    'height': '500px',
                    'width': '74%',
                    },
              ),

    
  ],
  style = {
          #'border': '2px solid black',
          'display': 'flex',
          'flex-wrap': 'nowrap'
          },
  
  ),


  html.Br(),

  #Bar Chart
  dcc.Graph(id = 'barchart',       
            #style= {'border':'2px solid black'}
  ),
   
  #Datatable
  dash_table.DataTable(
    data=df.to_dict('records'),
    columns = [{"name": i, "id": i} for i in df.columns],
    sort_action = "native",
    virtualization = True,
    page_size = 250,    
    fixed_rows = {'headers': True, 'data': columns_fixed},
    fixed_columns = {'headers': True, 'data': 1},
    style_header={
            'backgroundColor': 'rgb(230, 230, 230)',
            'fontWeight': 'bold'
        },
    style_cell={
            'minWidth': '150px',
            'maxWidth': '150px',
            'textOverflow': 'ellipsis'
        },
    style_table={'minWidth': '100%'},
    
    #Custom column width
    style_data_conditional=[
            {'if': {'column_id': 'Country Name'}, 'minWidth': '300px', 'backgroundColor': 'rgb(245, 245, 245)'},
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
            {'if': {'column_id': 'ISO3'}, 'minWidth': '50px'},
            {'if': {'column_id': 'Religion'}, 'minWidth': '1000px'},
            ]

  ),

])

#----------------------------Callback for clicking individual country to get data------------------------

@vis.callback(
    Output('p_country_name', 'children'),
    Output('p_capital','children'),
    Output('p_government','children'),
    Output('p_currency','children'),
    Output('p_population','children'),
    Output('p_density','children'),
    Output('p_area','children'),
    Output('p_water','children'),
    Output('p_gdp','children'),
    Output('p_gdp_pc','children'),
    Output('p_hdi','children'),
    Output('p_gini','children'),
    Output('pie_chart','figure'),
    Input('map','clickData')
)
def update_output(input_value):
  #Find ISO3 of the country clicked
  ISO3 = str(input_value['points'][0]['location'])
  for i in range(len(df)):
    if df.loc[i,"ISO3"] == ISO3:
      country_name = df.loc[i,"Country Name"]
      capital = df.loc[i,"Capital"]
      government = df.loc[i,"Government"]
      currency = df.loc[i,"Currency"]
      population = df.loc[i,"Population"]
      density = df.loc[i,"Density"]
      area = df.loc[i,"Area"]
      water = df.loc[i,"Water %"]
      gdp = df.loc[i,"GDP Total"]
      gdp_pc = df.loc[i,"GDP Per Capita"]
      hdi = df.loc[i,"HDI"]
      gini = df.loc[i,"Gini"]
      #Prepare and format religions chart
      for religion in ["Christianity", "Islam", "Buddhism","Hinduism","Judaism"]:
         if df.loc[i,religion] == '':
            df.loc[i,religion] = 0 
         df.loc[i,religion] = float(df.loc[i,religion])

      other = 100 - (df.loc[i,"Christianity"] + df.loc[i,"Islam"] +
                     df.loc[i,"Buddhism"] + df.loc[i,"Hinduism"] + df.loc[i,"Judaism"])

      religion_pie_chart = {'data': [pxgo.Pie(values = [df.loc[i,"Christianity"], 
                                                        df.loc[i,"Islam"],
                                                        df.loc[i,"Buddhism"],
                                                        df.loc[i,"Hinduism"],
                                                        df.loc[i,"Judaism"],
                                                        other
                                                        ], 
                                              labels = ['Christianity',
                                                        'Islam',
                                                        'Buddhism',
                                                        'Hinduism',
                                                        'Judaism',
                                                        'Other'
                                                        ],
                                              marker=dict(colors = ['blue', 'red', 'green', 'purple','grey','orange']),
                                              textposition = 'inside')],
                            'layout': pxgo.Layout(title = { 'text': '<b>Religion:</b>', 
                                                            'font': {
                                                                    'family': 'Open Sans',
                                                                    'size': 16,   
                                                                    'color': 'black'
                                                                  },
                                                            'y': 0.95
                                                            },
                                                    width = 320,
                                                    height = 320,
                                                    margin = dict(t=0, b=70),
                                                    legend = {
                                                              'x': 1.0,
                                                              'y': 0.5
                                                             },
                                                    paper_bgcolor='rgba(255,255,255,0)'
                                                    )}
      

  return(country_name, capital, government, currency, population, 
         density, area, water, gdp, gdp_pc,hdi, gini, religion_pie_chart)



#----------------------------Callback for sorting barchart and map
@vis.callback(
    Output('map', 'figure'),
    Output('barchart', 'figure'),
    Input('dropdown', 'value'),
)

def update_output_value(input_value):

  #If religion is selected, convert religion columns into floats and add zero where no data is available 
  if input_value in ['Christianity', 'Islam', 'Judaism', 'Hinduism', 'Buddhism']:
    for i in range(len(df)):
      if df.loc[i, input_value] == '':
        df.loc[i,input_value] = 0
    df[input_value] = df[input_value].astype(float)

  #Map 
  map1 = px.choropleth(df,
                      locations = 'ISO3',
                      color = input_value,
                      color_continuous_scale=[
                        [0, 'rgb(255,255,255)'],
                        [0.60, 'rgb(255,0,0)'],
                        [1, 'rgb(255,0,0)']
                        #Green[1, 'rgb(7,255,73)']
                        ],
                      scope = 'world',
                      featureidkey = 'ISO3',
                      )


  map1.update_layout(margin={"r":0,"t":27,"l":0,"b":0}),
  if input_value == "Density":
    map1.update_layout(coloraxis=dict(cmin=0, cmax=800))
  

  #Bar Chart 
  df_sorted = df.sort_values(by = input_value, ascending = False)
  dfbarchart = df_sorted.head(20)
  barchart = px.bar(dfbarchart, x = 'Country Name', y = input_value)

  return map1, barchart



if __name__ == '__main__':
  vis.run_server()
    
server = vis.server


#---------------------------SOME COUNTRIES ARE MISSING AT THE STAGE OF MERGING TABLES - SOMALILAND SPECIFICALLY



#Code for making SQL datatable
# CREATE TABLE geodata_iso (
#     country_name VARCHAR(500),
#     government VARCHAR(500),
#     population BIGINT(11),
#     density FLOAT(25,5),
#     area FLOAT(25,5),
#     water FLOAT(25,5),
#     gdp_total FLOAT(25,5),
#     gdp_per_capita FLOAT(25,5), 
#     hdi FLOAT(25,5), 
#     gini FLOAT(25,5), 
#     currency VARCHAR(500),
#     top_traded_currency VARCHAR(500),
#     christianity FLOAT(25,5),
#     islam FLOAT(25,5),
#     hinduism FLOAT(25,5),
#     buddhism FLOAT(25,5),
#     judaism FLOAT(25,5), 
#     iso3 VARCHAR(500)
# );