import datetime
import fastf1
import fastf1.plotting
from matplotlib import pyplot as plt
import pandas

# defined drivers info: name abbreviation, full name and color
drivers_abv = { '1' : 'VER', '2' : 'SAR',
                '3' : 'RIC',
                '4' : 'NOR', '10' : 'GAS',
               '11' : 'PER', '14' : 'ALO',
               '16' : 'LEC', '18' : 'STR',
               '20' : 'MAG', '21' : 'DEV',
               '22' : 'TSU', '23' : 'ALB', 
               '24' : 'ZHO', '27' : 'HUL',
               '31' : 'OCO', 
               '34' : 'DRU', '44' : 'HAM', 
               '55' : 'SAI', '63' : 'RUS', 
               '77' : 'BOT', '81' : 'PIA'}

drivers_names =   { '1' : 'Max Versttapen', '2' : 'Logan Sargeant',
                    '3' : 'Daniel Ricciardo',
                    '4' : 'Lando Norris', '10' : 'Pierre Gasly',
                   '11' : 'Sergio Peres', '14' : 'Fernando Alonso',
                   '16' : 'Charles Lecler', '18' : 'Lance Stroll',
                   '20' : 'Kevin Magnussen', '21' : 'Nyck De Vries',
                   '22' : 'Yuki Tsunoda', '23' : 'Alex Albon', 
                   '24' : 'Guanyu Zhou', '27' : 'Nico Hulkenberg',
                   '31' : 'Esteban Ocon', 
                   '34' : 'Felipe Drugovich', '44' : 'Lewis Hamilton', 
                   '55' : 'Carlos Sainz', '63' : 'George Russell', 
                   '77' : 'Valteri Bottas', '81' : 'Oscar Piastri'}

drivers_colors =   { '1' : '#0700EE', '2' : '#37BEDD',
                     '3' : '#2C4563',
                     '4' : '#FF8700', '10' : '#0090FF',
                    '11' : '#3671C6', '14' : '#006E61',
                    '16' : '#DC0000', '18' : '#358C75',
                    '20' : '#B6BABD', '21' : '#2C4563',
                    '22' : '#2C4563', '23' : '#015AFF', 
                    '24' : '#C92D4B', '27' : '#FFFFFF',
                    '31' : '#2293D1', 
                    '34' : '#006E61', '44' : '#01D2BD', 
                    '55' : '#F91536', '63' : '#6CD3BF', 
                    '77' : '#900000', '81' : '#F58020'}

drivers = {'abv': drivers_abv,
           'names': drivers_names,
           'colors': drivers_colors}

class F1Event():
    def __init__(self, event_name: str, year: int = 2023):
        self.event_name = event_name
        self.year = year
            
    def load(self):
        self.schedule = fastf1.get_event_schedule(year=self.year)
        self.event = self.schedule.get_event_by_name(self.event_name)

    def create_event_briefing(self) -> str:
        self.load()
        # get relevant information from event details
        date = self.event.EventDate.strftime("%d %B %Y")
        name = self.event.OfficialEventName
        country = self.event.Country
        location = self.event.Location
        sprint = self.event.EventFormat
        session2_date = self.event.Session2DateUtc - datetime.timedelta(hours=3)
        session2_date = session2_date.strftime("%d %B %Y %H:%M")
        session3_date = self.event.Session3DateUtc - datetime.timedelta(hours=3)
        session3_date = session3_date.strftime("%d %B %Y %H:%M")
        session4_date = self.event.Session4DateUtc - datetime.timedelta(hours=3)
        session4_date = session4_date.strftime("%d %B %Y %H:%M")
        race_date = self.event.Session5DateUtc - datetime.timedelta(hours=3)
        race_date = race_date.strftime("%d %B %Y %H:%M")
        
        # select dates based on event type (convetional or sprint shootout)
        if sprint == 'conventional':
            qualify_date = session4_date
        else:
            qualify_date = session2_date
            sprintshootout_date = session3_date
            sprint_date = session4_date

        # create briefing text
        event_briefing = f'On {date} Formula One arrives in {location}, {country} for the {name}. '

        if sprint == 'conventional':
            event_briefing = event_briefing + f'Qualify will be on {qualify_date} and race will be on {race_date}. All times are on Brasilia time.'
        else:
            event_briefing = event_briefing + 'This week we have Sprint race, so plenty of interesting session for delight of fans.'
            event_briefing = event_briefing + f'Qualify will be on {qualify_date}, them we have Sprint Shootout on {sprintshootout_date} '
            event_briefing = event_briefing + f'them we have sprint race on {sprint_date} and finally the race on {race_date}.'
            event_briefing = event_briefing + 'All times are on Brasilia time.'
            
        return event_briefing
    
class F1Session():
    def __init__(self, event_name: str, session_number: int, year: int = 2023):
        self.event_name = event_name
        self.session_number = session_number
        self.year = year
        
    def load(self):
        self.schedule = fastf1.get_event_schedule(year=self.year)
        self.event = self.schedule.get_event_by_name(self.event_name)
        self.session = self.event.get_session(self.session_number)
        self.session.load()
    
    def fastests_lap(self):
        self.fastest_lap = pandas.DataFrame(columns=['Driver', 'Fastest Lap'])

        for driver in self.session.drivers:
            try:
                lap = self.session.laps.pick_driver(driver).pick_fastest()
                laptime = (datetime.datetime(1970,1,1) + lap.LapTime).strftime("%M:%S.%f")
                self.fastest_lap.loc[driver,'Fastest Lap'] = laptime
                self.fastest_lap.loc[driver,'Driver'] = drivers['abv'][driver]
            except:
                self.fastest_lap.loc[driver,'Fastest Lap'] = None

        self.fastest_lap.sort_values('Fastest Lap', inplace=True)

    def get_top_2(self):
        self.top_2 = self.fastest_lap.index[:2]

    def set_top_2(self, top_2: list[str]):
        self.top_2 = top_2

    def get_telemetries(self):
        self.telemetries =[]
        for car in self.top_2:
            lap = self.session.laps.pick_driver(car).pick_fastest()
            car_data = lap.get_car_data()
            pos = self.session.pos_data[car]
            pos = pos.slice_by_lap(lap)
            telemetry = pos.merge_channels(car_data)
            telemetry = telemetry.add_distance()
            self.telemetries.append(telemetry)
        
    def calculate_gap_number(self) -> datetime.timedelta:
        time_format = '%M:%S.%f'
        p1_time = datetime.datetime.strptime(self.fastest_lap['Fastest Lap'][0], time_format)
        p2_time = datetime.datetime.strptime(self.fastest_lap['Fastest Lap'][1], time_format)
        return p2_time - p1_time
    
    def prepare(self, cars: list[str] | None = None):
        self.load()
        self.fastests_lap()

        if cars is None:
            self.get_top_2()
        else:
            self.set_top_2(cars)

        self.get_telemetries()
        
    def session_briefing(self, cars: list[str] | None = None) -> dict:

        self.prepare(cars)

        gap = self.calculate_gap_number()
        p1_number = self.fastest_lap.index[0]
        p1_name = drivers["names"][p1_number]
        p1_time = self.fastest_lap['Fastest Lap'][0][:9]
        p2_number = self.fastest_lap.index[1]
        p2_name = drivers["names"][p2_number]
        p2_time = self.fastest_lap['Fastest Lap'][1][:9]
        
        others = ', '.join(drivers["names"][i] for i in self.fastest_lap.index[2:10])
        
        p1_top_speed = self.telemetries[0]["Speed"].max()
        p1_avg_speed = round(self.telemetries[0]["Speed"].mean(), 2)
        p2_top_speed = self.telemetries[1]["Speed"].max()
        p2_avg_speed = round(self.telemetries[1]["Speed"].mean(), 2)
        speed_gap = round(float(p1_top_speed) - float(p2_top_speed), 2)

        info_dict = {   'name': self.session.name,
                        'location': self.event.Location,
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
    
    def race_briefing(self, cars: list[str] | None = None) -> dict:

        self.prepare(cars)
    
        top_3 = self.session.results['DriverNumber'].index[:3]
        top_3_names = ', '.join([drivers['names'][i] for i in top_3])
        others_name = ', '.join([drivers['names'][i] for i in self.session.results['DriverNumber'].index[3:]])
        
        fastest_lap_number = self.fastest_lap.index[0]
        fastest_lap_name = drivers["names"][fastest_lap_number]
        fastest_lap_time = self.fastest_lap['Fastest Lap'][0][:9]

        info_dict = {   'name': self.session.name,
                        'location': self.event.Location,
                        'top_3_names': top_3_names,
                        'fastest_lap_time': fastest_lap_time,
                        'fastest_lap_name':fastest_lap_name,
                        'others_name': others_name,}
        return info_dict 
    
    def range_briefing(self, 
                       chart_range: list[int], 
                       turn_name,
                       cars: list[str] | None = None) -> str:
    
        self.prepare(cars)

        # filter telemetry data to requested range
        p1_telemetry = self.telemetries[0][self.telemetries[0]['Distance'].between(chart_range[0],chart_range[1])]
        p2_telemetry = self.telemetries[1][self.telemetries[1]['Distance'].between(chart_range[0],chart_range[1])]
        # get drivers names
        p1_name = drivers["names"][self.top_2[0]]
        p2_name = drivers["names"][self.top_2[1]]
        # start briefing string
        briefing = ''
        if turn_name : briefing = briefing + f'At turn {turn_name}: '
        # calculate who arrives faster
        p1_top_speed = p1_telemetry['Speed'].max()
        p2_top_speed = p2_telemetry['Speed'].max()
        if p1_top_speed > p2_top_speed:
            briefing = briefing + f'{p1_name} arrives faster than {p2_name}. '
        else:
            briefing = briefing + f'{p1_name} arrives slower than {p2_name}. '
        # calculate who brakes firts
        p1_brake_distance = p1_telemetry[p1_telemetry['Brake'] == True]['Distance'].values[0]
        p2_brake_distance = p2_telemetry[p2_telemetry['Brake'] == True]['Distance'].values[0]
        if p1_brake_distance < p2_brake_distance:
            briefing = briefing + f'{p1_name} brakes earlier than {p2_name}. '
        else:
            briefing = briefing + f'{p1_name} brakes later than {p2_name}. '
        # calculate who resumes throttle earlier
        p1_throttle_distance = p1_telemetry[(p1_telemetry['Distance'] > p1_brake_distance) & (p1_telemetry['Throttle'] > 0)]['Distance'].values[0]
        p2_throttle_distance = p2_telemetry[(p2_telemetry['Distance'] > p1_brake_distance) & (p2_telemetry['Throttle'] > 0)]['Distance'].values[0]

        if p1_throttle_distance < p2_throttle_distance:
            briefing = briefing + f'{p1_name} resumes acceleration earlier {p2_name}. '
        else:
            briefing = briefing + f'{p1_name} resumes acceleration later than {p2_name}. '
        # calculate how much P1 is faster at this part
        p1_time = (p1_telemetry['Time'].values[-1] - p1_telemetry['Time'].values[0]).astype(datetime.timedelta) / 1000000000
        p2_time = (p2_telemetry['Time'].values[-1] - p2_telemetry['Time'].values[0]).astype(datetime.timedelta) / 1000000000
        briefing = briefing + f'{p1_name} runs this section in  {p1_time} s '
        briefing = briefing + f'while {p2_name} runs it in  {p2_time} s. '
        briefing = briefing + f'{p1_name} is {round(p2_time - p1_time, 3)} s faster.'
        return briefing
