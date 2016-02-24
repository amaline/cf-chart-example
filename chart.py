from spyre import server

import pandas as pd
import urllib2
import json
import os
import ssl

class StockExample(server.App):
    title = "Historical Stock Prices"

    inputs = [{     "type":'dropdown',
                    "label": 'Company',
                    "options" : [ {"label": "Bank of America", "value":"BAC"},
                                  {"label": "Wells Fargo Bank", "value":"WFC"},
                                  {"label": "JPMorgan Chase Bank", "value":"JPM"},
                                  {"label": "Citibank", "value":"C"},
                                  {"label": "U.S. Bank", "value":"USB"},
                                  {"label": "PNC Bank", "value":"PNC"},
                                  {"label": "Capital One", "value":"COF"},
                                  {"label": "TD Bank", "value":"TD"},
                                  {"label": "The Bank of New York Mellon", "value":"BK"},
                                  {"label": "SunTrust Bank", "value":"STI"}
                                ],
                    "key": 'ticker',
                    "action_id": "update_data"}]

    controls = [{    "type" : "hidden",
                    "id" : "update_data"}]

    tabs = ["Plot", "Table"]

    outputs = [{ "type" : "plot",
                    "id" : "plot",
                    "control_id" : "update_data",
                    "tab" : "Plot"},
                { "type" : "table",
                    "id" : "table_id",
                    "control_id" : "update_data",
                    "tab" : "Table",
                    "on_page_load" : True }]

    def getData(self, params):
        ticker = params['ticker']
        # make call to yahoo finance api to get historical stock data
        api_url = 'https://chartapi.finance.yahoo.com/instrument/1.0/{}/chartdata;type=quote;range=3m/json'.format(ticker)
        ssl._create_default_https_context = ssl._create_unverified_context
        result = urllib2.urlopen(api_url).read()
        data = json.loads(result.replace('finance_charts_json_callback( ','')[:-1])  # strip away the javascript and load json
        self.company_name = data['meta']['Company-Name']
        df = pd.DataFrame.from_records(data['series'])
        df['Date'] = pd.to_datetime(df['Date'],format='%Y%m%d')
        return df

    def getPlot(self, params):
        df = self.getData(params).set_index('Date').drop(['volume'],axis=1)
        plt_obj = df.plot()
        plt_obj.set_ylabel("Price")
        plt_obj.set_title(self.company_name)
        fig = plt_obj.get_figure()
        return fig

app = StockExample()
#app.launch(port=9093)
print 'PORT: {}'.format(os.environ['PORT'])
app.launch(host="all",port=int(os.environ['PORT']))
