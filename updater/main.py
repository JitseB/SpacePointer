import time, requests, json, os
from led import LED

# Define directory
dir = os.path.dirname(__file__)
led = LED(23) # LAN LED

while 1:
    time.sleep(15)
    print('Attempting to update ISS data')

    try:
        request = requests.get(url = "https://celestrak.com/NORAD/elements/stations.txt")
        print('Established connection successfully')
    except:
        print('Could not connect to the internet')
        continue

    led.set(True)
    data = request.text.split('\r\n')
    new_iss = {'name': data[0].strip(), 'data': [data[1], data[2]]}
    print(f'New ISS object data: {new_iss}')

    with open(os.path.join(dir, '../website/app/objects.json'), 'r') as file:
        objects = json.load(file)
    standard = objects['standard']

    current_iss = None
    for object in standard:
        if object['name'] == new_iss['name']:
            current_iss = object
            break

    if current_iss != None:
        standard.remove(current_iss)
    standard.append(new_iss)

    objects['standard'] = standard

    with open(os.path.join(dir, '../website/app/objects.json'), 'w') as file:
        json.dump(objects, file)
    print('Saved new ISS data successfully')

    time.sleep(1)
    led.set(False)
