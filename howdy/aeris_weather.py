import requests
import datetime
from pytz import timezone

app_id = "*"
client_id = "OJYEZahfbhZ3l3LDVMnw4"
client_secret = "7Bpln54RX53moAUSNLNLd1XtvHn8e3c2eedzWsyn"
verbose = False


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
    if r.status_code != 200:
        print('Error, aeris request failure with code: {}'.format(r.status_code)) # TODO change to exception
        return {}
    
    # Check for error in the aeris response
    jres = r.json()
    if ( not jres['success'] ):  #TODO change to exception
        print('Error, weather request failed!  Reason: {}\n'.format(jres['error']))
    return jres
	
#  Returns a dictionary containing info from Aeris observation:
#       Station name, city, datetime w/ local timezone
#       Temperature, wind speed, general description, matching icon
def getConditions(location):
    specs = { 'fields': 'id,place,profile.tz,obDateTime,ob.tempF,ob.windSpeedMPH,ob.weatherShort,ob.icon' }
    
    #TODO  add code to catch exception
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

#   Returns an array of dictionaries - forecast info for each day
#       Date, name of day, max temp, min temp, chance of precip, wind speed,
#       hourly temps throughout day
def getForecasts(location):

    # Gather daily info
    today = datetime.date.today().__format__('%Y-%m-%d')
    specs = { 'filter': 'mdnt2mdnt','from': 'today','to': '+3days',
        'fields': 'periods.dateTimeISO,periods.maxTempF,periods.minTempF,periods.pop,periods.windSpeedMaxMPH,profile.tz'
    }   
    #TODO  add code to catch exception
    jresponse = simpleAerisRequest(location, 'forecasts', specs)

    fc_days = []
    periods = jresponse['response'][0]['periods']
    
    # Check for inconsistent behavior, where today isn't included in response
    if periods[0]['dateTimeISO'].split('T')[0] != today:
        map = {}
        map['date'] = today
        map['day_of_week'] = datetime.datetime.today().strftime('%a')
        map['temp_hi'] = '--'
        map['temp_lo'] = '--'
        map['pop'] = '--'
        map['wind_hi'] = '--'
        map['hour_temps'] = []
        map['hour_pops']  = []
        fc_days.append(map)

    # Build list for returning data
    for n in range(3):    #(len(periods))
        fcdata = periods[n]
        map = {}
        map['date'] = fcdata['dateTimeISO'].split('T')[0]
        map['day_of_week'] = day_of_week(fcdata['dateTimeISO'])
        map['temp_hi'] = fcdata['maxTempF']
        map['temp_lo'] = fcdata['minTempF']
        map['pop'] = fcdata['pop']
        map['wind_hi'] = fcdata['windSpeedMaxMPH']
        map['hour_temps'] = []
        map['hour_pops']  = []                
        fc_days.append(map)

    # Gather hourly info - expecting fc_days to have same dates, ordering as hourly array
    specs = {'filter': 'mdnt2mdnt,3hr', 'from': 'today', 'to': '+3days',
        'fields': 'periods.dateTimeISO,periods.tempF,periods.pop'
    }
    #TODO  add code to catch exception
    jresponse = simpleAerisRequest(location, 'forecasts', specs)
    
    hourly = jresponse['response'][0]['periods']
    it_days = iter(fc_days)
    day = it_days.__next__()
    for x in hourly:
        if not x['dateTimeISO'].startswith(day['date']):
            # print('Hourly date is: {}, days date is:{}\n'.format(x['dateTimeISO'], day['date']))
            day = it_days.__next__()
            if not x['dateTimeISO'].startswith(day['date']):
                print('ERRRROORRRR!!!! make a handler')
                print('AFTER next - Hourly date is: {}, days date is:{}\n'.format(x['dateTimeISO'], day['date']))
                break
        day['hour_temps'].append(x['tempF'])
        day['hour_pops'].append(x['pop'])
    
    if verbose:
        print(fc_days)
    return fc_days

# Return day abbreviation, given a date string in ISO format
def day_of_week(dt_str):
    datestring = ''.join((dt_str[:-3], '00'))
    dateobj = datetime.datetime.strptime(datestring, '%Y-%m-%dT%H:%M:%S%z')
    return dateobj.strftime('%a')