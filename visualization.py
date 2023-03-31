import pandas as pd
import plotly.express as px
import plotly.graph_objects as pxgo
import dash
from dash import dash_table
from dash import dcc
from dash import html
from dash import Input, Output
from sqlalchemy import create_engine

#Import data from the MySQL server to the DataFrame
engine = create_engine('mysql+pymysql://baebbc1dedd03e:18882be2@us-cdbr-east-06.cleardb.net/heroku_50f453d91482063') #mysql+pymysql://root:@localhost/geodata' (on local server)
df = pd.read_sql_table('geodata_iso', engine)
ds = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/2014_world_gdp_with_codes.csv')

#----------------------------------------------Visualization---------------------------------

#Code for fixed rows in Datatable
columns_fixed = []
for i in df.columns:
  columns_fixed.append(i)
labels = ['n/a']
values = [1]


#------------------------------------------Initiation and Layout
vis = dash.Dash(__name__)

vis.layout = html.Div([
  
  html.Div([
    html.Img(src='/assets/logo.png', style={'height': '90px', 'width': '300px'}), #rgba(102,252,241,255)
    dcc.Link('Methodology', href='https://docs.google.com/document/d/1mtUqbVAg3osFj2a1Fv1QR2rn2oNnjwu60KnVMMutFnE/edit?usp=sharing',
            target='_blank', 
            style = {'color':'rgba(102,252,241,255)',
                     'margin-left':'70%',
                     'margin-bottom':'60px', 
                     'fontFamily': 'sans-serif',
                     'font-size': '13px'}),
         ],
    style = {'display': 'flex', 'align-items': 'center'}),

  #Dropdown
  html.Div([
              html.P('Chart Map by:', style = {'margin-right':'10px', 'font-weight':'bold'}),
              dcc.Dropdown(['Population', 'Density', 'Area','Water %', 'Top Traded Currency', 'GDP Total', 'GDP Per Capita', 'HDI', 'Gini', 
                            'Christianity', 'Islam', 'Hinduism', 'Buddhism', 'Judaism'], 
                    id='dropdown', value = 'Population',
                    style={'width': '200px','backgroundColor': '#253346',
                           'borderRadius': '10px', 'color':'black', 'fontFamily': 'sans-serif'})
              ],
              style={'margin-left':'70%', 'margin-bottom':'5px', 'display': 'flex', 'align-items': 'center'}),
  
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

        html.P('No Country Selected', id = 'p_country_name', 
                style={'textAlign': 'center',
                        'margin-top': 20,
                        'font-style':'italic'
                      }
               ),    
       
        #Div for Capital
        html.Div([
          html.P('Capital:', style = {'font-weight': 'bold', 'margin': '5px 10px 5px 16px'}),
          html.P(id = 'p_capital', style = {'margin': '5px 15px 5px 99px'}),
        ],
          style = {'display': 'flex'}),

        #Div for Head of Governmnent
        html.Div([
          html.P('Government:', style = {'font-weight': 'bold', 'margin': '5px 10px 5px 15px','min-width': '150px'}),
          html.P(id = 'p_government', style = {'margin': '5px 15px 5px 8px'}),
        ],
          style = {'display': 'flex'}),
        
        #Div for Currency
        html.Div([
          html.P('Currency:', style = {'font-weight': 'bold', 'margin': '5px 10px 5px 15px'}),
          html.P(id = 'p_currency', style = {'margin': '5px 15px 5px 82px'}),
        ],
          style = {'display': 'flex'}),

        #Div for Population
        html.Div([
          html.P('Population:', style = {'font-weight': 'bold', 'margin': '5px 10px 5px 15px'}),
          html.P(id = 'p_population', style = {'margin': '5px 15px 5px 70px'}),
        ],
          style = {'display': 'flex'}),          

        #Div for Density
        html.Div([
          html.P('Density:', style = {'font-weight': 'bold', 'margin': '5px 10px 5px 15px'}),
          html.P(id = 'p_density', style = {'margin': '5px 15px 5px 95px'}),
        ],
          style = {'display': 'flex'}),    

        #Div for Area
        html.Div([
          html.P('Area:', style = {'font-weight': 'bold', 'margin': '5px 10px 5px 15px'}),
          html.P(id = 'p_area', style = {'margin': '5px 15px 5px 117px'}),
        ],
          style = {'display': 'flex'}),   

        #Div for Water
        html.Div([
          html.P('Water %:', style = {'font-weight': 'bold', 'margin': '5px 10px 5px 15px'}),
          html.P(id = 'p_water', style = {'margin': '5px 15px 5px 89px'}),
        ],
          style = {'display': 'flex'}),   

        #Div for GDP Total
        html.Div([
          html.P('GDP Total:', style = {'font-weight': 'bold', 'margin': '5px 10px 5px 15px'}),
          html.P(id = 'p_gdp', style = {'margin': '5px 15px 5px 76px'}),
        ],
          style = {'display': 'flex'}),   

        #Div for GDP Per Capita
        html.Div([
          html.P('GDP Per Capita:', style = {'font-weight': 'bold', 'margin': '5px 10px 5px 15px'}),
          html.P(id = 'p_gdp_pc', style = {'margin': '5px 15px 5px 33px'}),
        ],
          style = {'display': 'flex'}),   

        #Div for HDI
        html.Div([
          html.P('HDI:', style = {'font-weight': 'bold', 'margin': '5px 10px 5px 15px'}),
          html.P(id = 'p_hdi', style = {'margin': '5px 15px 5px 123px'}),
        ],
          style = {'display': 'flex'}),   

        #Div for Gini
        html.Div([
          html.P('Gini:', style = {'font-weight': 'bold', 'margin': '5px 10px 5px 15px'}),
          html.P(id = 'p_gini', style = {'margin': '5px 15px 5px 120px'}),
        ],
          style = {'display': 'flex'}),   

        #Div for Religion container and graph
        html.Div([
          dcc.Graph(
                      id='pie_chart',
                      config={ "displayModeBar": False},
                      figure={
                              'data': [pxgo.Pie(
                                              labels = ['                '],
                                              values = [1],
                                              marker=dict(colors = ['#D1FFE4']),
                                              textposition='inside')],
                              'layout': pxgo.Layout(title = { 'text': '<b>Religion:</b>', 
                                                            'font': {
                                                                      'family': 'sans-serif',
                                                                      'size': 16,   
                                                                      'color': 'white'
                                                                    },
                                                            'y': 0.92
                                                            },
                                                    width = 320,
                                                    height = 230,
                                                    margin = dict(t=10, b=0),
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
        style = {'height':'230px', 'border': '1px solid transparent', 'border-top-color': 'white'}),

      
      ],
      style = {
              'border': '2px solid black',
              'height': '500px',
              'width': '25%',
              'overflowY': 'scroll',
              'borderRadius': '15px',
              'backgroundColor': 'rgba(37,51,70,255)',
              'scrollbar-color': 'red blue',
              'margin':'0'
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
            style= {'border':'3px solid black', 'margin':'0px 0px', 'borderRadius': '15px'}
  ),

  html.H3('Datatable', style={'textAlign': 'center'}),
   
  #Datatable
  dash_table.DataTable(
    data=df.to_dict('records'),
    columns = [{"name": i, "id": i} for i in df.columns],
    sort_action='native',
    page_size = 250,   
    virtualization = True, 
    fixed_rows = {'headers': True, 'data': columns_fixed},
    fixed_columns = {'headers': True, 'data': 1},
    style_header={
            'backgroundColor': '#18212E',
            'fontWeight': 'bold'
        },
    style_cell={
            'minWidth': '150px',
            'maxWidth': '150px',
            'textOverflow': 'ellipsis',
            'fontFamily': 'sans-serif'
        },
    style_table={"height": "610px", "maxHeight": "610px", "minWidth": '100%', 'backgroundColor': '#253346'},
    #Custom column width
    style_data_conditional=[
            {'if': {'column_id': 'Country Name'}, 'minWidth': '300px', 'backgroundColor': '#18212E', 'fontWeight': 'bold'},
            {'if': {'column_id': 'Capital'}, 'minWidth': '300px', 'backgroundColor': '#253346'},
            {'if': {'column_id': 'Government'}, 'minWidth': '300px', 'backgroundColor': '#253346'},
            {'if': {'column_id': 'Population'}, 'minWidth': '150px', 'backgroundColor': '#253346'},
            {'if': {'column_id': 'Density'}, 'minWidth': '150px', 'backgroundColor': '#253346'},
            {'if': {'column_id': 'Area'}, 'minWidth': '150px', 'backgroundColor': '#253346'},
            {'if': {'column_id': 'Water %'}, 'minWidth': '75px', 'backgroundColor': '#253346'},
            {'if': {'column_id': 'GDP Total'}, 'minWidth': '175px', 'backgroundColor': '#253346'},
            {'if': {'column_id': 'GDP Per Capita'}, 'minWidth': '150px', 'backgroundColor': '#253346'},
            {'if': {'column_id': 'HDI'}, 'minWidth': '100px', 'backgroundColor': '#253346'},
            {'if': {'column_id': 'Gini'}, 'minWidth': '100px', 'backgroundColor': '#253346'},
            {'if': {'column_id': 'Currency'}, 'minWidth': '280px', 'backgroundColor': '#253346'},
            {'if': {'column_id': 'Top Traded Currency'}, 'minWidth': '150px', 'backgroundColor': '#253346'},
            {'if': {'column_id': 'ISO'}, 'minWidth': '50px', 'backgroundColor': '#253346'},
            {'if': {'column_id': 'ISO3'}, 'minWidth': '80px', 'backgroundColor': '#253346'},
            {'if': {'column_id': 'Christianity'}, 'minWidth': '120px', 'backgroundColor': '#253346'},
            {'if': {'column_id': 'Islam'}, 'minWidth': '120px', 'backgroundColor': '#253346'},
            {'if': {'column_id': 'Hinduism'}, 'minWidth': '120px', 'backgroundColor': '#253346'},
            {'if': {'column_id': 'Buddhism'}, 'minWidth': '120px', 'backgroundColor': '#253346'},
            {'if': {'column_id': 'Judaism'}, 'minWidth': '120px', 'backgroundColor': '#253346'},
            {'if': {'column_id': 'Religion'}, 'minWidth': '1000px', 'backgroundColor': '#253346'},
            ],
  ),

],
style = {'fontFamily': 'sans-serif', 'backgroundColor': '#0B0C10', 'color': 'white'} #'color': 'rgba(227,228,230,255)'

)

#------------------------------Callback for clicking individual country to get data------------------------

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
                                              marker=dict(colors = ['#65FCF2', '#50CBE6', '#50E6B5', 
                                                                    '#59B9FE','#CFD0FF','#D1FFE4'],
                                                          line=dict(color='white', width=2)),
                                              textposition = 'inside')],
                            'layout': pxgo.Layout(title = { 'text': '<b>Religion:</b>', 
                                                            'font': {
                                                                    'family': 'sans-serif',
                                                                    'size': 16,   
                                                                    'color': 'black'
                                                                  },
                                                            'y': 0.92
                                                            },
                                                    width = 320,
                                                    height = 230,
                                                    margin = dict(t=10, b=0),
                                                    legend = {
                                                              'x': 1.0,
                                                              'y': 0.5
                                                             },
                                                    paper_bgcolor='rgba(255,255,255,0)',
                                                    font_color='white',
                                                    title_font_color='white'
                                                    )}


  return(html.H3(country_name, style={'font-style':'normal'}),  
         capital, government, currency, population, 
         density, area, water, gdp, gdp_pc,hdi, gini, religion_pie_chart)




#-----------------------------------------Callback for sorting barchart and map-----------------
@vis.callback(
    Output('map', 'figure'),
    Output('barchart', 'figure'),
    Input('dropdown', 'value'),
)

def update_output_value(input_value):
  #------------Map-----------

  #If religion is selected, convert religion columns into floats and add zero where no data is available 
  if input_value in ['Christianity', 'Islam', 'Judaism', 'Hinduism', 'Buddhism']:
    for i in range(len(df)):
      if df.loc[i, input_value] == '':
        df.loc[i,input_value] = 0
    df[input_value] = df[input_value].astype(float)

  #Colors for parameters
  color_palette =    {#Density is in a separate "if"
                      'Population':          [[0, 'rgb(255,255,255)'],[0.50, 'rgba(102,252,241,255)'],[1, 'rgb(5, 250, 234)']],
                      'Area':                [[0, '#ffffff'],[1, '#9494FF']],
                      'Water %':             [[0, '#ffffff'],[0.25, '#59B9FE'],[1, '#29B9FE']],
                      'Top Traded Currency': [[0, '#ffffff'],[1, '#50E6B5']],
                      'GDP Total':           [[0, '#ffffff'],[0.1,'#FFEADB'],[0.6, '#B5F5DB'],[1, '#52F5DB']],
                      'GDP Per Capita':      [[0, '#ffffff'],[0.08,'#2EE5F2'],[1, '#0036F2']],
                      'HDI':                 [[0, '#E6383E'],[1, '#50CBE6']],
                      'Gini':                [[0, '#ffffff'],[0.6,'#FFE303'],[1, '#FF1703']],
                      'Christianity':        [[0, '#ffffff'],[1, '#65FCF2']],
                      'Islam':               [[0, '#ffffff'],[1, '#50CBE6']],
                      'Judaism':             [[0, '#ffffff'],[1, '#CFD0FF']],
                      'Hinduism':            [[0, '#ffffff'],[1, '#59B9FE']],
                      'Buddhism':            [[0, '#ffffff'],[1, '#50E6B5']]}

  #Map 
  map1 = px.choropleth(
                      df,
                      locations = 'ISO3',
                      color = input_value,
                      color_continuous_scale=[[0, 'rgb(255,255,255)'],[0.50, 'rgba(102,252,241,255)'],[1, 'rgb(5, 250, 234)']],
                      )
  
  if input_value == "Density":
    map1 = px.choropleth(
                    df,
                    locations = 'ISO3',
                    color = input_value,
                    color_continuous_scale=[[0, '#ffffff'], [0.40,'#6BCBE6'],[1, '#00ABE6']],
                    )
    map1.update_layout(coloraxis=dict(cmin=0, cmax=800))


  if input_value in ['Population','Area','Water %','Top Traded Currency',
                     'GDP Total', 'GDP Per Capita','HDI','Gini',
                     'Christianity', 'Islam', 'Judaism', 'Hinduism', 'Buddhism']:
      map1 = px.choropleth(df, locations = 'ISO3', color = input_value,
                      color_continuous_scale = color_palette[input_value])
          

  #Update layout
  map1.update_layout(
    margin={"r":0,"t":27,"l":0,"b":0},
    plot_bgcolor="rgba(37,51,70,255)",
    paper_bgcolor="rgba(37,51,70,255)",
    geo_bgcolor="rgba(37,51,70,255)",
    coloraxis_colorbar=dict(
      title_font_color="white",
      tickfont_color="white")
  )
  



  #------Bar Chart-------
  df_sorted = df.sort_values(by = input_value, ascending = False)
  dfbarchart = df_sorted.head(20)
  barchart = px.bar(dfbarchart, x = 'Country Name', y = input_value)
  barchart.update_layout(xaxis_title=None,
                         plot_bgcolor="rgba(37,51,70,255)",
                         paper_bgcolor="rgba(37,51,70,255)",
                         font_color='white',
                         xaxis=dict(tickfont=dict(family='sans-serif', size=14)),
                         yaxis=dict(tickfont=dict(family='sans-serif'),
                                    title_font=dict(family='sans-serif', size=18))                                 
                         )

  barchart.update_traces(marker={'color': 'rgba(8,250,234,255)'}) #'color': 'rgba(102,252,241,255)'


  return map1, barchart



if __name__ == '__main__':
  vis.run_server()
    
server = vis.server


#---------------------------SOME COUNTRIES ARE MISSING AT THE STAGE OF MERGING TABLES - SOMALILAND SPECIFICALLY



#Code for making SQL datatable
# CREATE TABLE geodata (
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