import datetime

from matplotlib import pyplot as plt
import pandas

from f1gpt.connectors import F1Session

class Ploter:
    '''Class to plot a comparison between two drivers
    Attributes:
        session: F1Session object (see f1gpt.connectors)
    Methods:
        plot_comparison: plot a comparison between the two drivers
        '''
    def __init__(self, 
                 session: F1Session) -> None:
        self.drivers = session.drivers
        self.location = session.event.Location
        self.name = session.session.name       
        self.telemetries = session.get_data()
        self.cars = session.top_2

    def calculate_gap(self, window_size: int = 75) -> pandas.DataFrame:
        merged = pandas.merge(self.telemetries[0][['Distance', 'Speed', 'Time']], 
                              self.telemetries[1][['Distance', 'Speed', 'Time']], 
                              on='Distance', 
                              how='outer',
                              suffixes=[f'_{self.cars[0]}', f'_{self.cars[1]}'])

        merged = merged.sort_values('Distance')

        merged.interpolate(inplace=True)

        merged['Time_Gap'] = merged[f'Time_{self.cars[1]}'] - merged[f'Time_{self.cars[0]}']
        merged['Time_Gap'] = merged['Time_Gap'].apply(datetime.timedelta.total_seconds)
        merged['Time_Gap'] = merged['Time_Gap'].rolling(window=window_size).mean()
        merged['Time_Gap'] = merged['Time_Gap'].fillna(0)
        
        self.telemetries[0] = pandas.merge(self.telemetries[0], merged[['Distance', 'Time_Gap']], on='Distance', how='left')
        
    
    def plot_comparison(self,
                        axis_x: str = 'Distance',
                        features: list[str] = ['Time_Gap', 'Speed', 'Throttle', 'Brake', 'nGear'],
                        chart_range: list[int] = None,
                        save_png: bool = True) -> None :  
        '''Plot a comparison between the two drivers
        args:
            axis_x: (str) x axis of the chart - either "Distance" or "Time"
            features: (list[str]) of features to be plotted - possible feature ["Time_Gap", "Speed", "Throttle", "Brake", "nGear"]
            chart_range: (list[int]) [optional] range of the chart - e.g. [0, 100] for the first 100 meters
            save_png: (bool) [optional] save the chart as a png file
        Returns:
            None'''
        
        len_features = len(features)
        font_size = 14
        self.calculate_gap()
        
        fig, ax = plt.subplots(len_features, figsize=(17,6 * len_features))
        fig.set_facecolor('black')
        
        if 'Time_Gap' in features:
            telemetry = self.telemetries[0]
            if chart_range:
                telemetry = telemetry[telemetry[axis_x].between(chart_range[0],chart_range[1])]
            ax[0].plot(telemetry[axis_x], 
                    telemetry['Time_Gap'], 
                    label = f'GAP: {self.drivers[self.cars[0]]["abv"]} vs {self.drivers[self.cars[1]]["abv"]}',
                    color = 'white')
            ax[0].set_ylabel('Time Gap', fontsize=font_size)
            ax[0].xaxis.label.set_color('white')
            ax[0].yaxis.label.set_color('white')
            ax[0].legend(fontsize=font_size)
            ax[0].set_title(f'{self.name} fastest lap comparison by {axis_x}', color='white', fontsize=20)
            ax[0].tick_params(axis='both', labelsize = font_size, labelcolor='white')
            ax[0].set_facecolor('black')
            ax[0].grid(True, color='white')
            
        for feature_index in range(len_features):
            feature = features[feature_index]
            if feature == 'Time_Gap': continue
            for car_index in range(len(self.cars)):
                telemetry = self.telemetries[car_index]
                if chart_range:
                    telemetry = telemetry[telemetry[axis_x].between(chart_range[0],chart_range[1])]
                car = self.cars[car_index]
                ax[feature_index].plot(telemetry[axis_x], 
                                    telemetry[feature], 
                                    label=self.drivers[car]['abv'],
                                    color=self.drivers[car]['color'])
                ax[feature_index].set_ylabel(feature, fontsize=font_size, )
                ax[feature_index].tick_params(axis='both', labelsize = font_size,  labelcolor='white')
                ax[feature_index].set_facecolor('black')
                if feature_index == 1:
                    ax[feature_index].legend(fontsize=font_size)
                if feature_index == len_features - 1:
                    ax[feature_index].set_xlabel(axis_x, fontsize=font_size)
                    ax[feature_index].tick_params(axis='x', labelsize = font_size)
                ax[feature_index].grid(True, color='white')
                ax[feature_index].xaxis.label.set_color('white')
                ax[feature_index].yaxis.label.set_color('white')

        if save_png: fig.savefig('chart.png', bbox_inches='tight', facecolor='black')
