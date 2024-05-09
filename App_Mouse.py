
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from pprint import pprint




external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__,external_stylesheets=external_stylesheets)

mouse_data = pd.read_csv("/Applications/Folders/Dash/data/Mouse_metadata.csv")
study_results = pd.read_csv("/Applications/Folders/Dash/data/Study_results.csv")
merged_df = pd.merge(mouse_data, study_results, on = 'Mouse ID')


# -------------------------------------------------------------------------------------------------------------- 

#											PART 1: DESIGN PARAMETERS

# --------------------------------------------------------------------------------------------------------------
# Here we will set the colors, margins, DIV height&weight and other parameters

color_choices = {
	'light-blue': '#7FAB8',
	'light-grey': '#F7EFED',
	'light-red':  '#F1485B',
	'dark-blue':  '#33546D',
	'middle-blue': '#61D4E2'
}

drug_colors = {
	'Placebo':		'#29304E',
	'Capomulin':	'#27706B',	
	'Ramicane':		'#71AB7F',
	'Ceftamin':		'#9F4440',
	'Infubinol':	'#FFD37B',
	'Ketapril':		'#FEADB9',
	'Naftisol':		'#B3AB9E',
	'Propriva':		'#ED5CD4',
	'Stelasyn':		'#97C1DF',
	'Zoniferol':	'#8980D4'
}


colors = {
		'full-background':		color_choices['light-grey'],
		'chart-background':		color_choices['light-grey'],
		'histogram-color-1':	color_choices['dark-blue'],
		'histogram-color-2':	color_choices['light-red'],
		'block-borders':		color_choices['dark-blue']
}

margins = {
		'block-margins': '10px 10px 10px 10px',
		'block-margins': '4px 4px 4px 4px'
}

sizes = {
		'subblock-heights': '290px'
}



# -------------------------------------------------------------------------------------------------------------- 

#											PART 2: ACTUAL LAYOUT

# --------------------------------------------------------------------------------------------------------------
# Here we will set the DIV-s and other parts of our layout
# We need to have a 2x2 grid
# I have also included 1 more grid on top of others, where we will show the title of the app



# -------------------------------------------------------------------------------------- DIV for TITLE
div_title = html.Div(children =	html.H1('Title'),
					style ={
							'border': '3px {} solid'.format(colors['block-borders']),
							'margin': margins['block-margins'],
							'text-align': 'center'
							}
					)

# ---------# -------------------------------------------------------------------------------------- DIV for first row (1.1 and 1.2)

# -------------------------------------------------------------- inside DIV 1.1
div_1_1_button = dcc.Checklist (
				id = 'weight-histogram-checklist',
		        options=[
		        	{'label': drug, 'value': drug} for drug in np.unique(mouse_data['Drug Regimen'])
		        ],
		        value=['Placebo'],
		        labelStyle={'display': 'inline-block'}
			)#This is a Dash Core Component Checklist component. It allows users to select one or more options from a list.



div_1_1_graph = dcc.Graph(
				id = 'weight-histogram',
		        
			)#This is a Dash Core Component Graph component. It represents the histogram graph for displaying the weight distribution of selected drug types. 

div_1_1 = html.Div(children = [div_1_1_button, div_1_1_graph],
				#className = 'test',
					style = {
							'border': '1px {} solid'.format(colors['block-borders']),
							'margin': margins['block-margins'],
							'width': '50%',
							# 'height': sizes['subblock-heights'],
					},
					        

				)# This is a Dash HTML Component Div component that contains both the div_1_1_button and div_1_1_graph components. 

# -------------------------------------------------------------- inside DIV 1.2
div_1_2 = html.Div(children=[
                        dcc.RadioItems(
                        id='overlay-drug-radio',
                        options=[{'label': drug, 'value': drug} for drug in np.unique(mouse_data['Drug Regimen'])],
                        value='Placebo',
                        labelStyle={'display': 'inline-block'}
                        ),
                        dcc.Graph(
                            id='weight-distribution-chart',
                            figure= {}
                        ),

                    ],
                    style={
                        'border': '1px {} solid'.format(colors['block-borders']),
                        'margin': margins['block-margins'],
                        'width': '50%',
                    },
                    )    # This is a placeholder div for Chart 2


# -------------------------------------------------------------------------------------- Collecting all DIV-s in the final layout


# -------------------------------------------------------------------------------------- Collecting all DIV-s in the final layout
# Here we collect all DIV-s into a final layout DIV
app.layout = html.Div([
    div_title,  # Title row
    html.Div([div_1_1, div_1_2], style={'display': 'flex'}),  # First row
],
    style={
        'backgroundColor': colors['full-background']
    }
)
# -------------------------------------------------------------------------------------------------------------- 


# histogram of mice weights' for each drug
# it is a stacked histogram which lets us put histograms on top of each other 
@app.callback(
    Output(component_id='weight-histogram', component_property='figure'),
    [Input(component_id='weight-histogram-checklist', component_property='value')]
)
def update_weight_histogram(drug_names):
    
    traces = []

    for drug in drug_names:
    	traces.append(go.Histogram(x=mouse_data[mouse_data['Drug Regimen']==drug]['Weight (g)'],
    							name = drug,
    							opacity = 0.9,
    							marker = dict(color=drug_colors[drug]))
    				)

    return {
        'data': traces,
        'layout': dict(
        	barmode='stack',
            xaxis={'title': 'mouse weight',
   					'range': [merged_df['Weight (g)'].min(), merged_df['Weight (g)'].max()],
   					'showgrid': False
   					},
            yaxis={'title': 'number of mice', 
            		'showgrid': False,
            		'showticklabels': True
            		},
            autosize=False,
           	paper_bgcolor = colors['chart-background'],
           	plot_bgcolor = colors['chart-background'],
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
	    







            legend={'x': 0, 'y': 1},
        )
    }

@app.callback(
    Output(component_id='weight-distribution-chart', component_property='figure'),
    [Input(component_id='overlay-drug-radio', component_property='value')]
)
def update_weight_distribution(selected_drug):
    traces = []

    # Overall weight distribution
    overall_distribution = go.Histogram(x=mouse_data['Weight (g)'],
                                        name='All mice',
                                        opacity=0.5,
                                        marker=dict(color='gray'))

    traces.append(overall_distribution)

    # Weight distribution for the selected drug
    if selected_drug:
        selected_distribution = go.Histogram(x=mouse_data[mouse_data['Drug Regimen'] == selected_drug]['Weight (g)'],
                                            name=selected_drug,
                                            opacity=0.9,
                                            marker=dict(color=drug_colors[selected_drug]))

        traces.append(selected_distribution)

    return {
        'data': traces,
        'layout': dict(
            barmode='overlay',
            xaxis={'title': 'Mouse Weight'},
            yaxis={'title': 'Number of Mice'},
            autosize=False,
            paper_bgcolor=colors['chart-background'],
            plot_bgcolor=colors['chart-background'],
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            legend={'x': 0, 'y': 1},
        )
    }










# -------------------------------------------------------------------------------------------------------------- 

#											PART 4: RUNNING THE APP

# --------------------------------------------------------------------------------------------------------------
# >> use __ debug=True __ in order to be able to see the changes after refreshing the browser tab,
#			 don't forget to save this file before refreshing
# >> use __ port = 8081 __ or other number to be able to run several apps simultaneously
if __name__ == '__main__':
	app.run_server(debug=True, port = 8081)