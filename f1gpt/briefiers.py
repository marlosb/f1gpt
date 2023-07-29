import datetime

from f1gpt.connectors import F1Session

class SessionBriefer:
    '''Class to create a briefing of a session
    Attributes:
        session: F1Session object (see f1gpt.connectors)
        drivers: DriversAttribute object (see f1gpt.connectors)
        location: location of the event
        name: name of the session
        telemetries: list of pandas.DataFrame with the telemetry data of the two drivers
        cars: list of the two drivers numbers
        fastest_lap: pandas.DataFrame with the fastest lap of the two drivers
        results: pandas.DataFrame with the results of the session
    Methods:
        create_session_brief: creates a briefing of a session (pratice or qualify)
        create_race_brief: creates a briefing of a race
        create_range_briefing: create briefing for a specific range of the lap
        '''
    def __init__(self, session: F1Session) -> None:
        '''Creates a SessionBriefer object
        Args:
            session: (F1Session) object with the session data
        Returns:
            None'''
        self.drivers = session.drivers
        self.location = session.event.Location
        self.name = session.session.name
        self.telemetries = session.get_data()
        self.cars = session.top_2
        self.fastest_lap = session.fastest_lap
        self.results = session.session.results

    def calculate_gap_number(self) -> datetime.timedelta:
        time_format = '%M:%S.%f'
        p1_time = datetime.datetime.strptime(self.fastest_lap['Fastest Lap'][0], time_format)
        p2_time = datetime.datetime.strptime(self.fastest_lap['Fastest Lap'][1], time_format)
        return p2_time - p1_time

    def create_session_brief(self) -> dict[str]:
        '''Creates a briefing of a session (pratice or qualify)
        args:   
            None
        Returns:
            info_dict: dictionary with the following keys:
                name: name of the session
                location: location of the session
                p1_name: name of the driver with the fastest lap
                p1_time: time of the fastest lap of the driver with the fastest lap
                p1_top_speed: top speed of the driver with the fastest lap
                p1_avg_speed: average speed of the driver with the fastest lap
                p2_name: name of the driver with the second fastest lap
                p2_time: time of the fastest lap of the driver with the second fastest lap
                p2_top_speed: top speed of the driver with the second fastest lap
                p2_avg_speed: average speed of the driver with the second fastest lap
                speed_gap: difference between the top speed of the two drivers
                gap: difference between the fastest lap of the two drivers
                others: names of the drivers with the third to tenth fastest lap

                '''
        gap = self.calculate_gap_number()
        p1_number = self.fastest_lap.index[0]
        p1_name = self.drivers[p1_number]["name"]
        p1_time = self.fastest_lap['Fastest Lap'][0][:9]
        p2_number = self.fastest_lap.index[1]
        p2_name = self.drivers[p2_number]["name"]
        p2_time = self.fastest_lap['Fastest Lap'][1][:9]
        
        others = ', '.join(self.drivers[i]["name"] for i in self.fastest_lap.index[2:10])
        
        p1_top_speed = self.telemetries[0]["Speed"].max()
        p1_avg_speed = round(self.telemetries[0]["Speed"].mean(), 2)
        p2_top_speed = self.telemetries[1]["Speed"].max()
        p2_avg_speed = round(self.telemetries[1]["Speed"].mean(), 2)
        speed_gap = round(float(p1_top_speed) - float(p2_top_speed), 2)

        info_dict = {   'name': self.name,
                        'location': self.location,
                        'p1_name': p1_name,
                        'p1_time': p1_time,
                        'p1_top_speed':p1_top_speed,
                        'p1_avg_speed': p1_avg_speed,
                        'p2_name': p2_name,
                        'p2_time': p2_time,
                        'p2_top_speed': p2_top_speed,
                        'p2_avg_speed': p2_avg_speed,
                        'speed_gap': speed_gap,
                        'gap': gap.total_seconds(),
                        'others': others}
        return info_dict
    
    def create_race_brief(self) -> dict[str]:
        '''creates a briefing of a race
         args:
            None
        Returns:
            info_dict: dictionary with the following keys:
                name: name of the session
                location: location of the session
                top_3_names: names of the drivers in the top 3
                fastest_lap_time: time of the fastest lap
                fastest_lap_name: name of the driver with the fastest lap
                others_name: names of the drivers in the 4th to 20th position
                '''
        top_3 = self.results['DriverNumber'].index[:3]
        top_3_names = ', '.join([self.drivers[i]['name'] for i in top_3])
        others_name = ', '.join([self.drivers[i]['name'] for i in self.results['DriverNumber'].index[3:]])
        
        fastest_lap_number = self.fastest_lap.index[0]
        fastest_lap_name = self.drivers[fastest_lap_number]["name"]
        fastest_lap_time = self.fastest_lap['Fastest Lap'][0][:9]

        info_dict = {   'name': self.name,
                        'location': self.location,
                        'top_3_names': top_3_names,
                        'fastest_lap_time': fastest_lap_time,
                        'fastest_lap_name':fastest_lap_name,
                        'others_name': others_name,}
        return info_dict 

    def create_range_briefing(self, 
                       chart_range: list[int], 
                       turn_name,) -> str:
        '''Create briefing for a specific range of the lap
        args:
            chart_range: list with the start and end distance of the range
            turn_name: name of the turn
        Returns:
            briefing: string with the briefing
            '''
        # filter telemetry data to requested range
        p1_telemetry = self.telemetries[0][self.telemetries[0]['Distance'].between(chart_range[0],chart_range[1])]
        p2_telemetry = self.telemetries[1][self.telemetries[1]['Distance'].between(chart_range[0],chart_range[1])]
        # get drivers names
        p1_name = self.drivers[self.cars[0]]["name"]
        p2_name = self.drivers[self.cars[1]]["name"]
        # start briefing string
        briefing = ''
        if turn_name : briefing = briefing + f'At turn {turn_name}: '
        # calculate who arrives faster
        p1_avg_speed = p1_telemetry['Speed'].mean()
        p2_avg_speed = p2_telemetry['Speed'].mean()
        # calculate who brakes firts
        p1_brake_distance = p1_telemetry[p1_telemetry['Brake'] == True]['Distance'].values[0]
        p2_brake_distance = p2_telemetry[p2_telemetry['Brake'] == True]['Distance'].values[0]
        
        p1_top_speed = p1_telemetry['Speed'].max()
        p2_top_speed = p2_telemetry['Speed'].max()
        if p1_brake_distance < p2_brake_distance:
            briefing = briefing + f'{p1_name} brakes earlier than {p2_name}. '
        else:
            briefing = briefing + f'{p1_name} brakes later than {p2_name}. '
        if p1_top_speed > p2_top_speed:
            briefing = briefing + f'{p1_name} arrives faster than {p2_name}. '
        else:
            briefing = briefing + f'{p1_name} arrives slower than {p2_name}. '
        # calculate who resumes throttle earlier
        p1_throttle_distance = p1_telemetry[(p1_telemetry['Distance'] > p1_brake_distance) & (p1_telemetry['Brake'] == False)]['Distance'].values[0]
        p2_throttle_distance = p2_telemetry[(p2_telemetry['Distance'] > p2_brake_distance) & (p2_telemetry['Brake'] == False)]['Distance'].values[0]
        
        if p1_throttle_distance < p2_throttle_distance:
            briefing = briefing + f'{p1_name} releases brake earlier than {p2_name}. '
        else:
            briefing = briefing + f'{p1_name} releases brake later than {p2_name}. '
        # average speed
        briefing = briefing + f'{p1_name} average speed is {round(p1_avg_speed, 2)} km/h '
        briefing = briefing + f'while {p2_name} average speed is {round(p2_avg_speed, 2)} km/h. '
        # calculate how much P1 is faster at this part
        p1_time = (p1_telemetry['Time'].values[-1] - p1_telemetry['Time'].values[0]).astype(datetime.timedelta) / 1000000000
        p2_time = (p2_telemetry['Time'].values[-1] - p2_telemetry['Time'].values[0]).astype(datetime.timedelta) / 1000000000
        briefing = briefing + f'{p1_name} runs this section in  {p1_time} s '
        briefing = briefing + f'while {p2_name} runs it in  {p2_time} s. '
        briefing = briefing + f'{p1_name} is {round(p2_time - p1_time, 3)} s faster.'
        return briefing