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
  'briggs' : '25',
  'soltech' : '40',
  'genudine' : '1000',
  'ceres' : '2000'
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


def utc_to_local(utc_dt):
  return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)

def getData(url):
  return requests.request("GET", url, data='{}').json()

def makeAuraxis(query_1, query_2, query_3):
  global attempt
  try:
    r1 = getData(query_1)
    r2 = getData(query_2)
    r3 = getData(query_3)

    r3['result'][0].pop('worldId', None)
    r3['result'][0].pop('timestamp', None)
    r3['result'][0].pop('unknown', None)
    r3['result'][0]['all'] = sum(r3['result'][0].values())

    Auraxis = {
      'time' : str(datetime.now().time().strftime('%H:%M:%S')),
      'server': r1['world_event_list'][0]['world']['name']['en'],
      'pop': r3['result'][0]
    }

    for c in r2['map_list']:
      ci = c['ZoneId']
      cz = c['Regions']['Row']
      vsTer = sum(i['RowData']['FactionId'] == factions['vs'] for i in cz)
      ncTer = sum(i['RowData']['FactionId'] == factions['nc'] for i in cz)
      trTer = sum(i['RowData']['FactionId'] == factions['tr'] for i in cz)
      noTer = sum(i['RowData']['FactionId'] == factions['no'] for i in cz)
      allTer = len(c['Regions']['Row'])
      
      Auraxis[ci] = Auraxis.get(ci, {
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
        Auraxis[ci]['state'] = status['1']
      if len(set(i['RowData']['FactionId'] for i in cz)) <= 2:
        Auraxis[ci]['state'] = status['0']

    for i in [e for e in r1['world_event_list'] if e['metagame_event_state_name'] == 'started' and e['zone_id'] in ['2','4','6','8']]:
      
      alert_dur = 45 if Auraxis[ci]['state'] is status['1'] else 90
      
      if int(int(i['timestamp'])+60*alert_dur)-int(datetime.now().timestamp()) > 0:
        ci = i['zone_id']
        ts = datetime.utcfromtimestamp( int(int(i['timestamp'])+60*alert_dur) )
        dt = utc_to_local(ts)
          
        Auraxis[ci]['state'] = status['4'] if Auraxis[ci]['state'] is status['1'] else status['3']
        Auraxis[ci]['ends'] = str(dt).split('+')[0]
        Auraxis[ci]['countdown'] = 1
    return json.dumps(Auraxis)
  
  except:
    attempt += 1
    if attempt <= 5:
      print(f'Error! Attempt #{attempt}')
      time.sleep(5)
      makeAuraxis()
    else:
      print(f'Error! Attempts exceeded!({attempt})')
      print('Stopping...')
      pass

def main():
  if len(sys.argv) >= 3:
    world = worlds[sys.argv[1].lower()]
    census = f'http://census.daybreakgames.com/s:{sys.argv[2]}/get/ps2/'
    
    query_1 = f"{census}world_event?type=METAGAME&world_id={world}&c:limit=20&c:lang=en&c:sort=timestamp&c:join=metagame_event^inject_at:metagame_event_id,world^inject_at:world,zone^inject_at:zone"
    query_2 = f"{census}map?world_id={world}&zone_ids=2,4,6,8"
    query_3 = f"https://ps2.fisu.pw/api/population/?world={world}"
    
    print(makeAuraxis(query_1, query_2, query_3))
  
  else:
    print('Insufficient parameters')


if __name__ == '__main__': main()