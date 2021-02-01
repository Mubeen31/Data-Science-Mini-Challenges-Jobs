import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import string
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
import collections
import spacy
import pandas as pd


data_analyst = pd.read_csv('data-analyst.csv')
data_engineer = pd.read_csv('data-engineer.csv')
data_scientist = pd.read_csv('data-scientist.csv')

combine_data = pd.concat([data_analyst, data_engineer, data_scientist])

# Which is the most skills required for a Data Science job
# First check the most used words in job title and download stopwords for NLP analysis
nltk.download('stopwords')
stopwords = nltk.corpus.stopwords.words('english')

# Set for removal words
remove_words = set(stopwords + list(string.punctuation) + list(string.digits))

# Check the most used words in job title
job_title = combine_data[combine_data['jobTitle'] != '-1']['jobTitle'].tolist()
list_of_words = []
for item in job_title:
    content = nltk.word_tokenize(item)
    for word in content:
        # remove unwanted words
       if word.lower() not in remove_words and word.lower() != 'data'and word.lower() != 'analyst' and word.lower() != 'data analyst' and word.lower() != 'engineer' and word.lower() != 'data engineer' and word.lower() != 'data science' and word.lower() != 'data scientist' and word.lower() != 'science' and word.lower() != 'scientist':
            list_of_words.append(word.upper())

# Convert list into pandas data frame
list_of_words1 = pd.DataFrame({'Job Title': list_of_words})

# Next check the most listed skills in the main data frame job title column
# To extract name entity recognition from all job titles and save in a dictionary
nlp = spacy.load('en_core_web_sm')
name_entity_recognition_job_title = {}
for item in job_title:
    token = nlp(item)
    for ent in token.ents:
        name_entity_recognition_job_title.setdefault(ent.label_ , []).append(ent.text)

# By viewing above, there are some useful technology skills are mentioned in the job title column
# Create list of these skills
list_of_useful_words = ['AWS', 'PYTHON', 'VISUALISATION', 'SQL', 'BI', 'TABLEAU', 'EXCEL', 'QLIK', 'SPARK', 'AZURE', 'MICROSOFT', 'NLP']

# Next I check how many times the above skills are mentioned in the job title column
count_skills_word = []
for word in list_of_words:
    if word in list_of_useful_words:
        count_skills_word.append(word)

# Convert list into pandas data frame
list_of_words2 = pd.DataFrame({'Job Title': count_skills_word})


app = dash.Dash(__name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}])

app.layout = html.Div([
    html.Div((

        html.Div([

            html.Div([
                html.H1('Data Science Mini Challenges', style={'margin-top': '10px'}),
                html.P('Jobs', style={'margin-top': '-8px',
                                      'text-align': 'center'})

            ], className='main_greeting')

        ], className='main_title'),

        html.Div([
            html.Div([
                html.Div([
                    dcc.RadioItems(id='radio_items',
                                   labelStyle={"display": "inline-block"},
                                   value='Applications',
                                   options=[{'label': 'Applications', 'value': 'Applications'},
                                            {'label': 'Jobs', 'value': 'Jobs'}],
                                   style={'text-align': 'center', 'color': '#2e4a66'}),
                ], className="radio_items_style"),
                html.Div([
                    html.Div([

                        html.P(id='text1'),
                        html.P(id='text2'),

                    ]),

                ], className='charts_left_title'),

                dcc.Graph(id='chart1'),

            ], className="charts_left six columns"),

            html.Div([
                html.Div([
                    dcc.RadioItems(id='radio_items1',
                                   labelStyle={"display": "inline-block"},
                                   value='Skills',
                                   options=[{'label': 'Companies', 'value': 'Companies'},
                                            {'label': 'Locations', 'value': 'Locations'},
                                            {'label': 'Average Salary', 'value': 'Average Salary'},
                                            {'label': 'Skills', 'value': 'Skills'}],
                                   style={'text-align': 'center', 'color': '#2e4a66'}),
                ], className="radio_items_style"),
                html.Div([
                    html.Div([

                        html.P(id='text3'),
                        html.P(id='text4'),
                        html.P(id='text5'),
                        html.P(id='text6'),

                    ]),

                ], className='charts_right_title'),
                dcc.Graph(id='chart2'),

            ], className='charts_left six columns')
        ], className="row flex-display"),

    ), className='main_container'),

], className='main')

@app.callback(
    Output('text1', 'children'),
    [Input('radio_items', 'value')]
    )

def update_text(radio_items):

    if radio_items == 'Applications':

     return [
         html.P('Top 10 companies by the most received applications', style={'margin-top': '-14px'})

    ]

@app.callback(
        Output('text2', 'children'),
        [Input('radio_items', 'value')]
    )
def update_text(radio_items):

    if radio_items == 'Jobs':
     return [
        html.P('Top 10 companies by the most listed jobs', style={'margin-top': '-24px'})

            ]

@app.callback(Output('chart1', 'figure'),
             [Input('radio_items', 'value')])
def update_graph(radio_items):
        # Applications
        combine_data1 = combine_data.groupby(['employerName'])['applications'].sum().sort_values(ascending = False).nlargest(n=10).reset_index()
        labels = combine_data1['employerName']
        values = combine_data1['applications']

        # Jobs
        combine_data2 = combine_data['employerName'].value_counts().sort_values(ascending=False).nlargest(n=15).reset_index()

        colors = ['#30C9C7', '#7A45D1', 'orange', '#EC5333', '#4133EC', '#2C3E50']

        if radio_items == 'Applications':


         return {
            'data': [go.Pie(labels = labels,
                            values = values,
                            marker = dict(colors = colors),
                            hoverinfo = 'label+value+percent',
                            textinfo = 'label+value',
                            textfont = dict(size = 13),
                            texttemplate = '%{label} <br>%{value:,.0f}',
                            textposition = 'auto',
                            # hole = .7,
                            rotation = 160,
                            insidetextorientation='radial',

                            )],

            'layout': go.Layout(
                margin=dict(l=129, r=122),
                plot_bgcolor = 'rgba(255, 255, 255, 0)',
                paper_bgcolor = 'rgba(255, 255, 255, 0)',
                hovermode = 'x',
                title = {'text':'',

                    'y': 0.93,
                    'x': 0.5,
                    'xanchor': 'center',
                    'yanchor': 'top'},
                titlefont = {
                    'color': 'white',
                    'size': 15},
                legend = {
                    'orientation': 'h',
                    'bgcolor': 'rgba(255, 255, 255, 0)',
                    'xanchor': 'center', 'x': 0.5, 'y': -0.15},

                font = dict(
                    family = "sans-serif",
                    size = 12,
                    color = '#2e4a66')
            ),

        }

        elif radio_items == 'Jobs':

            return {
                'data': [go.Bar(x=combine_data2['employerName'],
                                y=combine_data2['index'],
                                text=combine_data2['employerName'],
                                texttemplate='%{text:,.0f}',
                                textposition='auto',
                                marker=dict(color='#008080'),
                                orientation='h',
                                hoverinfo='text',
                                hovertext=
                                '<b>Employer</b>: ' + combine_data2['index'].astype(str) + '<br>' +
                                '<b>Counts</b>: ' + [f'{x:,.0f}' for x in combine_data2['employerName']] + '<br>'

                                )],

                'layout': go.Layout(
                    plot_bgcolor='rgba(255, 255, 255, 0)',
                    paper_bgcolor='rgba(255, 255, 255, 0)',
                    title={
                        'text': '',
                        'y': 0.99,
                        'x': 0.5,
                        'xanchor': 'center',
                        'yanchor': 'top'},
                    titlefont={
                        'color': 'white',
                        'size': 15},

                    hovermode='closest',
                    margin=dict(l=235, r=0, t=17),

                    xaxis=dict(title='<b>Counts</b>',

                               color='#2e4a66',
                               showline=True,
                               showgrid=True,
                               showticklabels=True,
                               linecolor='#2e4a66',
                               linewidth=1,
                               ticks='outside',
                               tickfont=dict(
                                   family='Arial',
                                   size=12,
                                   color='#2e4a66'
                               )

                               ),

                    yaxis=dict(title='<b></b>',
                               autorange='reversed',
                               color='#2e4a66',
                               showline=True,
                               showgrid=False,
                               showticklabels=True,
                               linecolor='#2e4a66',
                               linewidth=1,
                               ticks='outside',
                               tickfont=dict(
                                   family='Arial',
                                   size=12,
                                   color='#2e4a66'
                               )

                               ),
                    font=dict(
                        family="sans-serif",
                        size=12,
                        color='#2e4a66'),

                )
            }

@app.callback(
            Output('text3', 'children'),
            [Input('radio_items1', 'value')]
        )
def update_text(radio_items1):

            if radio_items1 == 'Companies':
                return [
                    html.P('The most applications received for various job positions by companies', style={'margin-top': '-14px'})

                ]

@app.callback(
            Output('text4', 'children'),
            [Input('radio_items1', 'value')]
        )
def update_text(radio_items1):

            if radio_items1 == 'Locations':
                return [
                    html.P('The most applications received for various job positions by locations', style={'margin-top': '-24px'})

                ]

@app.callback(
            Output('text5', 'children'),
            [Input('radio_items1', 'value')]
        )
def update_text(radio_items1):

            if radio_items1 == 'Average Salary':
                return [
                    html.P('Maximum average salary of top 10 companies', style={'margin-top': '-24px'})

                ]

@app.callback(
                Output('text6', 'children'),
                [Input('radio_items1', 'value')]
            )
def update_text(radio_items1):

            if radio_items1 == 'Skills':
                    return [
                        html.P('The most skills required for a Data Science job as mentioned in the Job Title column', style={'margin-top': '-24px'})

                    ]

@app.callback(Output('chart2', 'figure'),
             [Input('radio_items1', 'value')])
def update_graph(radio_items1):
        # Companies
        combine_data3 = combine_data.groupby(['employerName'])['applications'].sum().sort_values(ascending = False).nlargest(n=15).reset_index()
        # Locations
        combine_data4 = combine_data.groupby(['locationName'])['applications'].sum().sort_values(ascending=False).nlargest(n=15).reset_index()
        # Average Salary
        combine_data5 = combine_data.groupby(['employerName'])['maximumSalary'].mean().sort_values(ascending=False).nlargest(n=15).reset_index()
        # Skills
        combine_data7 = list_of_words2['Job Title'].value_counts().sort_values(ascending=False).nlargest(n=20).reset_index()

        if radio_items1 == 'Companies':

            return {
                'data': [go.Bar(x=combine_data3['applications'],
                                y=combine_data3['employerName'],
                                text=combine_data3['applications'],
                                texttemplate='%{text:,.0f}',
                                textposition='auto',
                                marker=dict(color='#FF7F50'),
                                orientation='h',
                                hoverinfo='text',
                                hovertext=
                                '<b>Employer</b>: ' + combine_data3['employerName'].astype(str) + '<br>' +
                                '<b>Counts</b>: ' + [f'{x:,.0f}' for x in combine_data3['applications']] + '<br>'

                                )],

                'layout': go.Layout(
                    plot_bgcolor='rgba(255, 255, 255, 0)',
                    paper_bgcolor='rgba(255, 255, 255, 0)',
                    title={
                        'text': '',
                        'y': 0.99,
                        'x': 0.5,
                        'xanchor': 'center',
                        'yanchor': 'top'},
                    titlefont={
                        'color': 'white',
                        'size': 15},

                    hovermode='closest',
                    margin=dict(l=235, r=0, t=17),

                    xaxis=dict(title='<b>Counts</b>',

                               color='#2e4a66',
                               showline=True,
                               showgrid=True,
                               showticklabels=True,
                               linecolor='#2e4a66',
                               linewidth=1,
                               ticks='outside',
                               tickfont=dict(
                                   family='Arial',
                                   size=12,
                                   color='#2e4a66'
                               )

                               ),

                    yaxis=dict(title='<b></b>',
                               autorange='reversed',
                               color='#2e4a66',
                               showline=True,
                               showgrid=False,
                               showticklabels=True,
                               linecolor='#2e4a66',
                               linewidth=1,
                               ticks='outside',
                               tickfont=dict(
                                   family='Arial',
                                   size=12,
                                   color='#2e4a66'
                               )

                               ),
                    font=dict(
                        family="sans-serif",
                        size=12,
                        color='#2e4a66'),

                )
            }

        elif radio_items1 == 'Locations':

            return {
                'data': [go.Bar(x=combine_data4['applications'],
                                y=combine_data4['locationName'],
                                text=combine_data4['applications'],
                                texttemplate='%{text:,.0f}',
                                textposition='auto',
                                marker=dict(color='#ff99cc'),
                                orientation='h',
                                hoverinfo='text',
                                hovertext=
                                '<b>Location</b>: ' + combine_data4['locationName'].astype(str) + '<br>' +
                                '<b>Counts</b>: ' + [f'{x:,.0f}' for x in combine_data4['applications']] + '<br>'

                                )],

                'layout': go.Layout(
                    plot_bgcolor='rgba(255, 255, 255, 0)',
                    paper_bgcolor='rgba(255, 255, 255, 0)',
                    title={
                        'text': '',
                        'y': 0.99,
                        'x': 0.5,
                        'xanchor': 'center',
                        'yanchor': 'top'},
                    titlefont={
                        'color': 'white',
                        'size': 15},

                    hovermode='closest',
                    margin=dict(l=140, r=0, t=17),

                    xaxis=dict(title='<b>Counts</b>',

                               color='#2e4a66',
                               showline=True,
                               showgrid=True,
                               showticklabels=True,
                               linecolor='#2e4a66',
                               linewidth=1,
                               ticks='outside',
                               tickfont=dict(
                                   family='Arial',
                                   size=12,
                                   color='#2e4a66'
                               )

                               ),

                    yaxis=dict(title='<b></b>',
                               autorange='reversed',
                               color='#2e4a66',
                               showline=True,
                               showgrid=False,
                               showticklabels=True,
                               linecolor='#2e4a66',
                               linewidth=1,
                               ticks='outside',
                               tickfont=dict(
                                   family='Arial',
                                   size=12,
                                   color='#2e4a66'
                               )

                               ),
                    font=dict(
                        family="sans-serif",
                        size=12,
                        color='#2e4a66'),

                )
            }

        elif radio_items1 == 'Average Salary':

            return {
                'data': [go.Bar(x=combine_data5['maximumSalary'],
                                y=combine_data5['employerName'],
                                text=combine_data5['maximumSalary'],
                                texttemplate='%{text:,.0f}',
                                textposition='auto',
                                marker=dict(color='#04B77A'),
                                orientation='h',
                                hoverinfo='text',
                                hovertext=
                                '<b>Employer</b>: ' + combine_data5['employerName'].astype(str) + '<br>' +
                                '<b>Average Salary</b>: ' + [f'{x:,.2f}' for x in combine_data5['maximumSalary']] + ' ' + 'GBP' + '<br>'

                                )],

                'layout': go.Layout(
                    plot_bgcolor='rgba(255, 255, 255, 0)',
                    paper_bgcolor='rgba(255, 255, 255, 0)',
                    title={
                        'text': '',
                        'y': 0.99,
                        'x': 0.5,
                        'xanchor': 'center',
                        'yanchor': 'top'},
                    titlefont={
                        'color': 'white',
                        'size': 15},

                    hovermode='closest',
                    margin=dict(l=200, r=0, t=17),

                    xaxis=dict(title='<b>Average Salary</b>',

                               color='#2e4a66',
                               showline=True,
                               showgrid=True,
                               showticklabels=True,
                               linecolor='#2e4a66',
                               linewidth=1,
                               ticks='outside',
                               tickfont=dict(
                                   family='Arial',
                                   size=12,
                                   color='#2e4a66'
                               )

                               ),

                    yaxis=dict(title='<b></b>',
                               autorange='reversed',
                               color='#2e4a66',
                               showline=True,
                               showgrid=False,
                               showticklabels=True,
                               linecolor='#2e4a66',
                               linewidth=1,
                               ticks='outside',
                               tickfont=dict(
                                   family='Arial',
                                   size=12,
                                   color='#2e4a66'
                               )

                               ),
                    font=dict(
                        family="sans-serif",
                        size=12,
                        color='#2e4a66'),

                )
            }

        elif radio_items1 == 'Skills':

         return {
        'data':[
            go.Scatter(
                x = combine_data7['index'],
                y = combine_data7['Job Title'],
                text = combine_data7['Job Title'],
                texttemplate = '%{text:.0f}',
                textposition = 'bottom left',
                mode = 'markers+lines+text',
                line = dict(width = 3, color = 'orange'),
                marker = dict(size = 10, symbol = 'circle', color = '#19AAE1',
                              line = dict(color = '#19AAE1', width = 2)
                              ),

                hoverinfo = 'text',
                hovertext =
                '<b>Skills</b>: ' + combine_data7['index'].astype(str) + '<br>' +
                '<b>Counts</b>: ' + [f'{x:,.0f}' for x in combine_data7['Job Title']] + '<br>'

            )],


        'layout': go.Layout(
             plot_bgcolor='rgba(255, 255, 255, 0)',
             paper_bgcolor='rgba(255, 255, 255, 0)',
             title={
                'text': '',

                'y': 0.99,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
             titlefont={
                        'color': 'white',
                        'size': 15},

             hovermode='closest',
             margin = dict(t = 5, l = 0, r = 0, b = 100),

             xaxis = dict(title = '<b>Skills</b>',
                          automargin = True,
                          visible = True,
                          color = '#2e4a66',
                          showline = True,
                          showgrid = False,
                          showticklabels = True,
                          linecolor = '#2e4a66',
                          linewidth = 1,
                          ticks = 'outside',
                          tickfont = dict(
                             family = 'Arial',
                             size = 12,
                             color = '#2e4a66')

                         ),

             yaxis = dict(title = '<b>Counts listed skills</b>',
                          visible = True,
                          color = '#2e4a66',
                          showline = False,
                          showgrid = True,
                          showticklabels = False,
                          linecolor = '#2e4a66',
                          linewidth = 1,
                          ticks = 'outside',
                          tickfont = dict(
                             family = 'Arial',
                             size = 12,
                             color = '#2e4a66')

                         ),

            font=dict(
                family="sans-serif",
                size=12,
                color='#2e4a66'),

        )

    }



if __name__ == '__main__':
    app.run_server(debug=True)