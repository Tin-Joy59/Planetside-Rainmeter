from datetime import datetime, timedelta, timezone
import time, sys
import requests, json

attempt = 0

worlds = {
  'connery' : '1',
  'miller' : '10',
  'cobalt' : '13',
  'emerald' : '17',
  'jaeger' : '19',
  'apex' : '24',
  'briggs' : '25',
  'soltech' : '40',
  'genudine' : '1000',
  'ceres' : '2000'
 }
zones = {
  '0' : 'Unknown',
  '2' : 'Indar',
  '4' : 'Hossin',
  '6' : 'Amerish',
  '8' : 'Esamir',
  '344': 'Oshur'
}
factions = {
  'no' : '0',
  'vs' : '1',
  'nc' : '2',
  'tr' : '3',
  'ns' : '4'
 }
status = {
  '0' : 'Locked',
  '1' : 'Unstable',
  '2' : 'Stable',
  '3' : 'Alert',
  '4' : 'Unstable Alert'
 }

zone_ids = ','.join(list(zones.keys())[1:])

def utc_to_local(utc_dt):
  return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)

def getData(url):
  return requests.request("GET", url, data='{}').json()

def tuckInDick(dick, tuck_as):
  o = []
  
  for k, v in dick.items():
    if isinstance(v, dict):
      o.append( {**{tuck_as:k}, **v} )
    
    elif isinstance(v, int):
      o.append( {tuck_as:k, 'count':v} )
  
  return o

def makeAuraxis(server, query_1, query_2, query_3):
  Auraxis = {
    'time'  : str(datetime.now().time().strftime('%H:%M:%S')),
    'server': server,
    'state' : 'Loading',
    'pop'   : {},
    'maps'  : {},
    'visible_meters' : 0,
    'error' : None
  }

  global attempt
  
  try:
    r1 = getData(query_1)
    r2 = getData(query_2)
    r3 = getData(query_3)

    r3['result'][0].pop('worldId', None)
    r3['result'][0].pop('timestamp', None)
    r3['result'][0].pop('unknown', None)
    r3['result'][0]['all'] = sum(r3['result'][0].values())

    Auraxis['server'] = r1['world_event_list'][0]['world']['name']['en']
    Auraxis['state']  = 'Unlocked' if r1['world_event_list'][0]['world']['state'] == 'online' else 'Locked'
    Auraxis['pop']    = r3['result'][0]

    if 'error' in r2.keys():
      Auraxis['state'] = 'Error'
      Auraxis['error'] = 'Could not load continents!'
    
    else:
      if len(r2['map_list']) == 0:
        Auraxis['state'] = 'Error'
        Auraxis['error'] = 'Could not load continents!'
      
      else:
        for c in r2['map_list']:
          ci = c['ZoneId']
          cz = c['Regions']['Row']
          vsTer = sum(i['RowData']['FactionId'] == factions['vs'] for i in cz)
          ncTer = sum(i['RowData']['FactionId'] == factions['nc'] for i in cz)
          trTer = sum(i['RowData']['FactionId'] == factions['tr'] for i in cz)
          noTer = sum(i['RowData']['FactionId'] == factions['no'] for i in cz)
          allTer = len(c['Regions']['Row'])
          
          Auraxis['maps'][ci] = Auraxis.get(ci, {
              'name' : zones[ci] if ci in zones.keys() else zones['0'],
              'ends': 0,
              'state': status['2'],
              'countdown': 0,
              'division': {
                'vs' : round(vsTer / allTer * 100, 3),
                'nc' : round(ncTer / allTer * 100, 3),
                'tr' : round(trTer / allTer * 100, 3),
                'no' : round(noTer / allTer * 100, 3)
              }
           })

          if noTer > 2:
            Auraxis['maps'][ci]['state'] = status['1']
          if len(set(i['RowData']['FactionId'] for i in cz)) <= 2:
            Auraxis['maps'][ci]['state'] = status['0']

        for i in [e for e in r1['world_event_list'] if e['metagame_event_state_name'] == 'started' and e['zone_id'] in zone_ids]:
          
          alert_dur = 45 if Auraxis['maps'][ci]['state'] is status['1'] else 90
          
          if int(int(i['timestamp'])+60*alert_dur)-int(datetime.now().timestamp()) > 0:
            ci = i['zone_id']
            ts = datetime.utcfromtimestamp( int(int(i['timestamp'])+60*alert_dur) )
            dt = utc_to_local(ts)
  
            Auraxis['maps'][ci]['state'] = status['4'] if Auraxis['maps'][ci]['state'] is status['1'] else status['3']
            Auraxis['maps'][ci]['ends'] = str(dt).split('+')[0]
            Auraxis['maps'][ci]['countdown'] = 1

    Auraxis['maps'] = tuckInDick(Auraxis['maps'], 'id')
    Auraxis['visible_meters'] = len(Auraxis['maps'])
    Auraxis['maps'] = dict(enumerate(Auraxis['maps']))

    return json.dumps(Auraxis)

  except:
    Auraxis['state'] = 'Error'
    Auraxis['error'] = 'Unable to retrieve data!'
    return json.dumps(Auraxis)

def main():

  if len(sys.argv) >= 3:
    world = worlds[sys.argv[1].lower()]
    census = f'http://census.daybreakgames.com/s:{sys.argv[2]}/get/ps2/'
    
    query_1 = f"{census}world_event?type=METAGAME&world_id={world}&c:limit=20&c:lang=en&c:sort=timestamp&c:join=metagame_event^inject_at:metagame_event_id,world^inject_at:world,zone^inject_at:zone"
    query_2 = f"{census}map?world_id={world}&zone_ids={zone_ids}"
    query_3 = f"https://ps2.fisu.pw/api/population/?world={world}"
    print(makeAuraxis(sys.argv[1].capitalize(), query_1, query_2, query_3))
  
  else:
    print(json.dumps({
      'server':'Unknown',
      'time':str(datetime.now().time().strftime('%H:%M:%S')),
      'error':'Insufficient parameters',
      'state':'Error',
      'visible_meters':0
    }))


if __name__ == '__main__': main()