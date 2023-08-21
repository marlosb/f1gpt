## Schema details

SessionBriefer class requires a F1Session object as input to generate text.
F1Session most have:
- drivers attribute (DriversAttribute objects)
- event.location attribute (string)
- session.name attribute (string)
- top2 attrinute (list of strings with 2 strings, each string is a driver number)
- fastest_lap attribute (pandas.Dataframe with 2 columns: 'Driver' and 'Fastest Lap', ordered by 'Fastest Lap')
- session.results attribute (pandas.DataFrame with 2 columns: 'DriverNumber' and 'Position', ordered by 'Position')
- telemetries attribute (list of pandas.DataFrame)

### Schemas
fastest_lap schema:
 - Fastest Lap            datetime64[ns]
 - Driver                        int64

results schema:
- Position                       int64
- DriverNumber                   object

telemetries schema:
 - Date            datetime64[ns]
 - RPM                      int64
 - Speed                    int64
 - nGear                    int64
 - Throttle                 int64
 - Brake                     bool
 - DRS                      int64
 - Source                  object
 - Time           timedelta64[ns]
 - SessionTime    timedelta64[ns]
 - Status                  object
 - X                        int64
 - Y                        int64
 - Z                        int64
 - Distance               float64
