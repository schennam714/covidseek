import pandas as pd
import fbprophet
from fbprophet.plot import add_changepoints_to_plot
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
        return total
    def train(self, original):
        df_prophet= original.rename(columns={'date': 'ds', 'cases': 'y'})

        m_global = fbprophet.Prophet(changepoint_prior_scale=0.05,changepoint_range=0.95,
                            daily_seasonality=False, 
                            weekly_seasonality=True,
                            mcmc_samples=300)
        m_global.add_seasonality(name='monthly', period=30.5, fourier_order=5)
        m_global.fit(df_prophet)
        future_global = m_global.make_future_dataframe(periods=30, freq='D')
        forecast_global = m_global.predict(future_global)
        fig=m_global.plot(forecast_global)
        a = add_changepoints_to_plot(fig.gca(), m_global, forecast_global)
        fig.savefig('/Users/shreyas/Desktop/Web Dev/covidtrack/covidtrack/static/graph.png')
        return fig