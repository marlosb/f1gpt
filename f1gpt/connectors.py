import datetime

import pandas
import fastf1

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

class F1Event:
    def __init__(self, event_name: str, year: int = 2023):
        self.event_name = event_name
        self.year = year
        self.schedule = fastf1.get_event_schedule(year=self.year)
        self.event = self.schedule.get_event_by_name(self.event_name)

class F1Session(F1Event):
    def __init__(self, 
                 event_name: str, 
                 session_number: int, 
                 drivers: dict[dict[str]],
                 year: int = 2023):
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
                self.fastest_lap.loc[driver,'Driver'] = self.drivers['abv'][driver]
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
