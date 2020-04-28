import pandas as pd
import fbprophet
from fbprophet.plot import add_changepoints_to_plot
import logging
logging.getLogger('fbprophet').setLevel(logging.WARNING)
import sys
sys.path.append("/Users/shreyas/Desktop/Web Dev/covidseek")
from covidseek.createdata import counties

class NewModel:
    def __init__(self, state):
        self.state = state
    def makedata(self):
        main = pd.DataFrame(counties)
        main['cases'] = main['cases'].astype(int)
        main['deaths'] = main['deaths'].astype(int)
        example = self.state
        indexes = []
        for i in range(0,len(counties)):
            if counties[i]['state'] != example:
                indexes.append(i)
        main = main.drop(indexes, axis=0)
        total = main.groupby(['date']).sum().loc[:,['cases','deaths']].reset_index()
        upper = total['cases'].max() + 4500
        total['cap'] = upper
        return total, upper
    def train(self, original, capping):
        df_prophet= original.rename(columns={'date': 'ds', 'cases': 'y', 'cap':'cap'})

        overall = fbprophet.Prophet(growth='logistic')
        overall.fit(df_prophet)
        future = overall.make_future_dataframe(periods=30)
        future['cap'] = capping
        new_future = overall.predict(future)
        fig=overall.plot(new_future)
        save = "/Users/shreyas/Desktop/Web Dev/covidseek/covidseek/static/" + self.state + ".png"
        fig.savefig(save)
        return fig