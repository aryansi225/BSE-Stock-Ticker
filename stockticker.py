import dash
import dash_core_components as dcc
import dash_html_components as dhc
from dash.dependencies import Input,Output,State
import pandas as pd
from datetime import datetime
import quandl


quandl.ApiConfig.api_key = "YOUR-API-KEY"
symbol_code = pd.read_csv('stocks.txt', delimiter='|')
symbol_code.set_index('STOCK', inplace=True)
options = []
for each in symbol_code.index:
    mydict={}
    mydict['label'] = each
    mydict['value'] = symbol_code.loc[each]["CODE"]
    options.append(mydict)
app = dash.Dash();
server = app.server
app.layout = dhc.Div([
                    dhc.H1('Bombay Stock Exchange - Stock Ticker Dashboard', style={'font-family':'Ubuntu', 'align':'center', 'font-weight': '300', 'font-size': '2.5rem', 'line-height': '1.2', 'letter-spacing': '-.1rem', 'margin-bottom': '2rem', 'marginLeft':'20rem'}),
                    dhc.Div([dhc.H3('Enter a stock name', style={'font-family':'Ubuntu', 'align':'center', 'font-weight': '300', 'font-size': '1.6rem', 'line-height': '1.3', 'letter-spacing': '-.1rem', 'margin-bottom': '1.5rem', 'margin-top': '1.5rem', 'padding-top': '1.5rem'}),
                    dcc.Dropdown(id='stock_picker',
                            options = options,
                            value=['BOM532540'],
                            multi=True
                    )],style={'display':'inline-block','verticalAlign':'top','width':'50%', 'margin-left':'2rem', 'margin-right':'2rem'}),
                    dhc.Div([dhc.H3('Select a start and end date',style={'font-family':'Ubuntu', 'align':'center', 'font-weight': '300', 'font-size': '1.6rem', 'line-height': '1.3', 'letter-spacing': '-.1rem', 'margin-bottom': '1.5rem', 'margin-top': '1.5rem', 'padding-top': '1.5rem'}),
                    dcc.DatePickerRange(id='date_picker',
                                        min_date_allowed=datetime(2000,1,1),
                                        max_date_allowed=datetime.today(),
                                        start_date = datetime(2015,1,1),
                                        end_date = datetime.today()
                            )],style={'display':'inline-block', 'margin-left':'2rem', 'margin-right':'2rem'}),
                    dhc.Div([
                        dhc.Button(id='submit-button',
                                    n_clicks=0,
                                    children='Submit',
                                    style={'height': '38px', 'padding': '0 50px', 'color': '#555', 'text-align': 'center', 'font-size': '11px', 'font-weight': '600', 'line-height': '38px', 'letter-spacing': '.1rem', 'text-transform': 'uppercase', 'text-decoration': 'none', 'white-space': 'nowrap', 'background-color': 'transparent', 'border-radius': '4px', 'border': '1px solid #bbb', 'cursor': 'pointer', 'box-sizing': 'border-box'})
                    ],style={'display': 'inline-block'}),
                    dcc.Graph(id='graph',
                                figure={'data':[
                                        {'x':[5,8,3,7,9,12,6,18], 'y':[7,2,5,6,4,18,15,23]}
                                ], 'layout': {'title':'Default Title'}}
                    )
])

def findName(val):
        for i in symbol_code.index:
                if str(symbol_code.loc[i]["CODE"]) == val:
                        return i
@app.callback(Output('graph', 'figure'),
                [Input('submit-button','n_clicks')],
                [State('stock_picker','value'),
                State('date_picker','start_date'),
                State('date_picker', 'end_date')])
def update_graph(n_clicks, value, start_date, end_date):
    start = datetime.strptime(start_date[:10],'%Y-%m-%d')
    end = datetime.strptime(end_date[:10],'%Y-%m-%d')
    traces=[]
    for each in value:
        df = quandl.get("BSE/"+each, start_date=start, end_date=end)
        traces.append({'x':df.index,'y':df['Close'],'name':findName(each)})
    fig = {'data':traces,
            'layout':{'title':'Stock Ticker',
            'xaxis':{'title':'Days','size': '20'},
            'yaxis':{'title':'Price of Stocks (in INR)','size': '20'},
            'plot_bgcolor': '#FAF9F9',
            'height': '550',
            'legend':dict(orientation="h"),
            }
    }
    return fig
if __name__=='__main__':
    app.run_server(debug=True)
