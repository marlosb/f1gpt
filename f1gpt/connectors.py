import datetime

import pandas
import fastf1

class DriversAttribute:
    '''Class to store the drivers data
    Attributes:
        items: dictionary with the drivers data
    Methods:
        __getitem__: get the data of a driver by "number" key (str) or index
        '''
    def __init__(self, data: dict[str]) -> None:
        '''Creates a DriversAttribute object
        Args:
            data: (dict[str]) dictionary with the drivers data
        Returns:
            None'''
        self.items = data

    def __getitem__(self, key: str) -> str:
        if isinstance(key, str):
            for item in self.items:
                if item['number'] == key:
                    return item
        else:
            raise TypeError('Key must be a string')

drivers = DriversAttribute([
                            {'number': '1', 'name': 'Max Versttapen', 'color': '#0700EE', 'abv': 'VER', 'team': 'Red Bull Racing'},
                            {'number': '2', 'name': 'Logan Sargeant', 'color': '#37BEDD', 'abv': 'SAR', 'team': 'Williams'},
                            {'number': '3', 'name': 'Daniel Ricciardo', 'color': '#2C4563', 'abv': 'RIC', 'team': 'Alpha Tauri'},
                            {'number': '4', 'name': 'Lando Norris', 'color': '#FF8700', 'abv': 'NOR', 'team': 'McLaren'},
                            {'number': '10', 'name': 'Pierre Gasly', 'color': '#0090FF', 'abv': 'GAS', 'team': 'Alpine'},
                            {'number': '11', 'name': 'Sergio Peres', 'color': '#3671C6', 'abv': 'PER', 'team': 'Red Bull Racing'},
                            {'number': '14', 'name': 'Fernando Alonso', 'color': '#006E61', 'abv': 'ALO', 'team': 'Aston Martin'},
                            {'number': '16', 'name': 'Charles Lecler', 'color': '#DC0000', 'abv': 'LEC', 'team': 'Ferrari'},
                            {'number': '18', 'name': 'Lance Stroll', 'color': '#358C75', 'abv': 'STR', 'team': 'Astom Martin'},
                            {'number': '20', 'name': 'Kevin Magnussen', 'color': '#B6BABD', 'abv': 'MAG', 'team': 'Haas'},
                            {'number': '21', 'name': 'Nyck De Vries', 'color': '#2C4563', 'abv': 'DEV', 'team': 'Alpha Tauri'},
                            {'number': '22', 'name': 'Yuki Tsunoda', 'color': '#2C4563', 'abv': 'TSU', 'team': 'Alpha Tauri'},
                            {'number': '23', 'name': 'Alex Albon', 'color': '#015AFF', 'abv': 'ALB', 'team': 'Williams'},
                            {'number': '24', 'name': 'Guanyu Zhou', 'color': '#C92D4B', 'abv': 'ZHO', 'team': 'Alfa Romeo'},
                            {'number': '27', 'name': 'Nico Hulkenberg', 'color': '#FFFFFF', 'abv': 'HUL', 'team': 'Haas'},
                            {'number': '31', 'name': 'Esteban Ocon', 'color': '#2293D1', 'abv': 'OCO', 'team': 'Alpine'},
                            {'number': '34', 'name': 'Felipe Drugovich', 'color': '#006E61', 'abv': 'DRU', 'team': 'Aston Martin'},
                            {'number': '44', 'name': 'Lewis Hamilton', 'color': '#01D2BD', 'abv': 'HAM', 'team': 'Mercedes'},
                            {'number': '55', 'name': 'Carlos Sainz', 'color': '#F91536', 'abv': 'SAI', 'team': 'Ferrari'},
                            {'number': '63', 'name': 'George Russell', 'color': '#6CD3BF', 'abv': 'RUS', 'team': 'Mercedes'},
                            {'number': '77', 'name': 'Valteri Bottas', 'color': '#900000', 'abv': 'BOT', 'team': 'Alfa Romeo'},
                            {'number': '81', 'name': 'Oscar Piastri', 'color': '#F58020', 'abv': 'PIA', 'team': 'McLaren'}])

class F1Event:
    '''Class to store the data of an event
    Attributes:
        event_name: name of the event (e.g. '"Silverstone"), we use fuzzy logic from fastf1 librarey to find the event
        year: year of the event
        '''
    def __init__(self, event_name: str, year: int = 2023):
        self.event_name = event_name
        self.year = year
        self.schedule = fastf1.get_event_schedule(year=self.year)
        self.event = self.schedule.get_event_by_name(self.event_name)

class F1Session(F1Event):
    '''Class to store the data of a session
    Attributes:
        event_name: name of the event (e.g. '"Silverstone")
        year: year of the event
        session_number: number of the session (e.g. 1 for FP1, 2 for FP2)
        drivers: DriversAttribute object (see f1gpt.connectors)
        '''
    def __init__(self, 
                 event_name: str, 
                 session_number: int, 
                 drivers: DriversAttribute,
                 year: int = 2023):
        '''Creates a F1Session object
        Args:
            event_name: (str) name of the event (e.g. '"Silverstone"), we use fuzzy logic from fastf1 librarey to find the event
            session_number: (int) number of the session (e.g. 1 for FP1, 2 for FP2, 3 for FP3, 4 for Q, 5 for R)
            drivers: (DriversAttribute) object with the drivers data
            year: (int) [optional] year of the event
        Returns:
            None
        '''
        F1Event.__init__(self, event_name, year)
        self.session_number = session_number
        self.drivers = drivers
        self.session = self.event.get_session(self.session_number)
        self.session.load()
    def fastests_lap(self):
        self.fastest_lap = pandas.DataFrame(columns=['Driver', 'Fastest Lap'])

        for driver in self.session.drivers:
            try:
                lap = self.session.laps.pick_driver(driver).pick_fastest()
                laptime = (datetime.datetime(1970,1,1) + lap.LapTime).strftime("%M:%S.%f")
                self.fastest_lap.loc[driver,'Fastest Lap'] = laptime
                self.fastest_lap.loc[driver,'Driver'] = self.drivers[driver]['abv']
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
    def get_data(self, cars: list[str] | None = None) -> list[pandas.DataFrame]:
        if cars:
            self.set_top_2(cars)
        else:
            self.fastests_lap()
            self.get_top_2()
        self.get_telemetries()
        return self.telemetries
