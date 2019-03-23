import requests
import datetime
from pytz import timezone
from requests.exceptions import HTTPError
from .errors import ConnectionError, AerisAPIError

app_id = "*"
client_id = "OJYEZahfbhZ3l3LDVMnw4"
client_secret = "QJZDkwLIwte4e2ReFJjeRuc685GZdYXzynpDuTMf"
#client_secret = "7Bpln54RX53moAUSNLNLd1XtvHn8e3c2eedzWsyn"
verbose = False

#======================
#  For making simple requests that only involve a specific location (the :id action) and
#  parameter settings ( which are optional)
def simpleAerisRequest(location, endpoint, paramMap={}):

    base_url = "http://api.aerisapi.com/"
    keyphrase = '?client_id=%s&client_secret=%s' % (client_id, client_secret)  
	
	# Build phrase from params
    paramList = []
    for k in paramMap:
        term = ''.join(('&', k, '=', paramMap[k]))
        paramList.append(term)
	
    request_url = ''.join((base_url, endpoint, '/', location, keyphrase, ''.join(paramList)))
    # print(request_url)
	
    r = requests.get(request_url)
    try:
        if r.status_code != 200:
            # print('Error, aeris request failure with code: {}'.format(r.status_code))
            r.raise_for_status()
    except HTTPError as e:
        raise ConnectionError('Error code {}'.format(r.status_code)) from e
    else:
        # Check for error in the aeris response
        jres = r.json()
        if ( not jres['success'] ): 
            print('Error, weather request failed!  Reason: {}\n'.format(jres['error']))
            raise AerisAPIError(jres['error'])
        #if verbose:
        #    print('simpleAerisRequest returns {}'.format(jres))
        return jres


#======================
#  Returns a dictionary containing info from Aeris observation:
#       Station name, city, datetime w/ local timezone
#       Temperature, wind speed, general description, matching icon
def getConditions(location):
    specs = { 'fields': 'id,place,profile.tz,obDateTime,ob.tempF,ob.windSpeedMPH,ob.weatherShort,ob.icon' }
    jresponse = simpleAerisRequest(location, 'observations', specs)

    data = jresponse['response']
    ob_data = data['ob']
    map = {}
    map['station'] = data['id']
    map['city'] = ''.join((data['place']['name'].title(), ', ', data['place']['state'].upper()))
    
    datestring = ''.join((data['obDateTime'][:-3], '00'))
    dateobj = datetime.datetime.strptime(datestring, '%Y-%m-%dT%H:%M:%S%z')
    tz = timezone(data['profile']['tz'])
    local_dt = dateobj.astimezone(tz)
    map['datetime'] = local_dt.strftime('%b %d %Y   %I:%M:%S %p %Z')

    for k in ob_data:
        map[k] = ob_data[k]
    # special case
    map['icon'] = ''.join(('AerisIcons/', ob_data['icon']))
        
    if verbose:
        print(map)
    return map

    
#======================
#   Returns an array of dictionaries - forecast info for each day
#       Date, name of day, max temp, min temp, chance of precip, wind speed,
#       hourly temps throughout day
def getForecasts(location):

    # Gather daily info
    today = datetime.date.today().__format__('%Y-%m-%d')
    specs = { 'filter': 'mdnt2mdnt','from': 'today','to': '+3days',
        'fields': 'periods.dateTimeISO,periods.maxTempF,periods.minTempF,periods.pop,periods.windSpeedMaxMPH,profile.tz'
    }   
    num_days = 3
    
    jresponse = simpleAerisRequest(location, 'forecasts', specs)

    fc_days = []
    periods = jresponse['response'][0]['periods']
    
    # Check for inconsistent behavior, where today isn't included in response
    if periods[0]['dateTimeISO'].split('T')[0] != today:
        num_days = 2
        map = {}
        map['date'] = today
        map['day_of_week'] = datetime.datetime.today().strftime('%a')
        map['temp_hi'] = '--'
        map['temp_lo'] = '--'
        map['pop'] = '--'
        map['wind_hi'] = '--'
        fc_days.append(map)

    # Build list for returning data
    for n in range(num_days):    
        fcdata = periods[n]
        map = {}
        map['date'] = fcdata['dateTimeISO'].split('T')[0]
        map['day_of_week'] = day_of_week(fcdata['dateTimeISO'])
        map['temp_hi'] = fcdata['maxTempF']
        map['temp_lo'] = fcdata['minTempF']
        map['pop'] = fcdata['pop']
        map['wind_hi'] = fcdata['windSpeedMaxMPH']
        fc_days.append(map)

    # **moved hourly to separate function call  
        
    if verbose:
        print(fc_days)
    return fc_days
    

#======================
#   Creates 2 arrays of hourly data: temp and % precipitation
#   Each array has elements that are timestamp/data, for 4 days
#   TODO: Include a check that dates in the weather data are as expected
def getHourly(location, start_date):
    specs = {'filter': 'mdnt2mdnt,1hr', 'from': 'today', 'to': '+3days',
        'fields': 'periods.dateTimeISO,periods.timestamp,periods.tempF,periods.pop,profile.tz'
    }
    
    jresponse = simpleAerisRequest(location, 'forecasts', specs)    
    hourly = jresponse['response'][0]['periods']
    tz = jresponse['response'][0]['profile']['tz']
    print('timezone: {}'.format(tz))
    
    temps = []
    pops = []

    # if not x['dateTimeISO'].startswith(day['date']):
        # # print('Hourly date is: {}, days date is:{}\n'.format(x['dateTimeISO'], day['date']))
        # day = it_days.__next__()
        # if not x['dateTimeISO'].startswith(day['date']):
            # print('ERRRROORRRR!!!! make a handler')
            # print('AFTER next - Hourly date is: {}, days date is:{}\n'.format(x['dateTimeISO'], day['date']))
           # break    

    for x in hourly:

        # Put data in format expected by highcharts - array of [time,val]
        time = x['timestamp'] * 1000
        temps.append([time, x['tempF']])
        pops.append([time, x['pop']])
    if verbose:
        print('Temps: {}'.format(temps))
        
    return {'hour_temps': temps, 'hour_pops': pops, 'tz': tz}
    
    
#======================
# Return whether the argument is a valid location for returning weather results
def validate_place(location):
    try:
        jresponse = simpleAerisRequest(location, 'places', {})
    except AerisAPIError as e:
        code = e.errcode['code']
        if not code == 'invalid_location':
            print ('In validate_place, unexpected error code: {}\n'.format(code) )
        return False
    else:
        return True  

#======================
# Return day abbreviation, given a date string in ISO format
def day_of_week(dt_str):
    datestring = ''.join((dt_str[:-3], '00'))
    dateobj = datetime.datetime.strptime(datestring, '%Y-%m-%dT%H:%M:%S%z')
    return dateobj.strftime('%a')
