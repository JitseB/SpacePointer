import time, json, ephem, datetime, math, os
from stepper import Stepper
from servo import Servo
from led import LED

# Define directory
dir = os.path.dirname(__file__)
stepper_step_deg = 200.0 / 360.0 # 1.7 deg

# Define electronics
# Stepper motor (first axis)
stepper = Stepper([22, 26, 24, 18]) # [ain1, ain2, bin1, bin2]

print('Testing freedom of movement')

# Test stepper:
# Forward
for step in range(200):
    stepper.step()
stepper.relax()

# Reverse
for step in range(200):
    stepper.step(True)
stepper.relax()

# Servo motor (second axis)
servo = Servo(18) # Broadcom numbering!
# Test servo
servo.angle(180)
servo.angle(0)

print('Finished')

# LEDs
err_led = LED(21)
top_led = LED(19)

with open(os.path.join(dir, '../config.json'), 'r') as file:
    config = json.load(file)

print('Welcome to Pointer version 1.0')
print(f'Tracking: {config["name"]}')
if 'data' in config.keys():
    print(f'Orbit data: {config["data"]}')
print(f'Observatory position: {config["gps"]}')

while 1:
    if 'data' in config.keys():
        data = config['data']
        if len(data) == 1:
            object = ephem.readdb(config['data'])
            err_led.set(False)
            break
        elif len(data) == 2:
            object = ephem.readtle(config['name'], *config['data'])
            err_led.set(False)
            break
        else:
            err_led.set(True)
            print('Waiting 1s for a fix')
            time.sleep(1)
    else:
        # It's one of the preprogrammed objects
        switch = {
            'Sun': ephem.Sun(),
            'Mercury': ephem.Mercury(),
            'Venus': ephem.Venus(),
            'Moon': ephem.Moon(),
            'Mars': ephem.Mars(),
            'Jupiter': ephem.Jupiter(),
            'Saturn': ephem.Saturn(),
            'Uranus': ephem.Uranus(),
            'Neptune': ephem.Neptune()
        }
        object = switch.get(config['name'], None)
        if object == None:
            err_led.set(True)
            print('Waiting 1s for a fix')
            time.sleep(1)
        else:
            err_led.set(False)
            break

print(f'Object name: {object.name}')

observer = ephem.Observer()
observer.date = datetime.datetime.utcnow()
gps = config["gps"].split(' ')
observer.lat = gps[0]
observer.lon = gps[1]
observer.horizon = 10.0 # [deg] visibility threshold
observer.elevation = float(gps[2])

local_time = ephem.localtime(observer.date)
local_time = local_time.replace(microsecond=0)
print(f'Current UTC time: {observer.date}')
print(f'Current local time: {local_time}')

# Find next pass info of object, returns 6-element tuple:
# 0  Rise time (when it comes up)
# 1  Rise azimuth
# 2  Maximum altitude time
# 3  Maximum altitude
# 4  Set time (when it goes down)
# 5  Set azimuth
try:
    rise_time, azimuth_rise, max_altitude_time, max_altitude, set_time, azimuth_set = observer.next_pass(object)

    # If the object isn't overhead right now, when will it be?
    if set_time > rise_time:
        duration = int((set_time - rise_time)*60*24) # Duration of pass
        local_time = ephem.localtime(rise_time)
        local_time = local_time.replace(microsecond=0)
        print(f'Next pass local time: {local_time} (duration: {duration} min)')
        print(f'Rise time UTC time: {rise_time}')
        print(f'Rise azimuth: {azimuth_rise}')
        print(f'Max altitude time: {max_altitude_time}')
        print(f'Max altitude: {max_altitude}')
        print(f'Set time UTC time: {set_time}')
        print(f'Set azimuth: {azimuth_set}')
except ValueError:
    print('Object seems to stay below your horizon at any given time!')
    print('Program terminates automatically.')
    exit(1)
except TypeError:
    print('Object is not using TLE format, skipping overhead info')

previous_azimuth_deg = 0
while 1:
    print('Loop step')
    with open(os.path.join(dir, '../config.json'), 'r') as file:
        config = json.load(file)

    if 'data' in config.keys():
        data = config['data']
        if len(data) == 1:
            object = ephem.readdb(config['data'])
            err_led.set(False)
        elif len(data) == 2:
            object = ephem.readtle(config['name'], *config['data'])
            err_led.set(False)
        else:
            err_led.set(True)
            print('Waiting .5s for a fix')
            continue
    else:
        # It's one of the preprogrammed objects
        switch = {
            'Sun': ephem.Sun(),
            'Mercury': ephem.Mercury(),
            'Venus': ephem.Venus(),
            'Moon': ephem.Moon(),
            'Mars': ephem.Mars(),
            'Jupiter': ephem.Jupiter(),
            'Saturn': ephem.Saturn(),
            'Uranus': ephem.Uranus(),
            'Neptune': ephem.Neptune()
        }
        object = switch.get(config['name'], None)
        if object == None:
            err_led.set(True)
            print('Waiting .5s for a fix')
            continue
        else:
            err_led.set(False)

    print(f'Object name: {object.name}')

    observer = ephem.Observer()
    observer.date = datetime.datetime.utcnow()
    gps = config["gps"].split(' ')
    observer.lat = gps[0]
    observer.lon = gps[1]
    observer.horizon = 10.0 # [deg] visibility threshold
    observer.elevation = float(gps[2])

    # Find the current location of the object
    object.compute(observer)

    altitude_deg = int(object.alt * 180.0 / math.pi)
    azimuth_deg = int(object.az * 180.0 / math.pi)

    # Set the (green) top LED's status
    top_led.set(True if altitude_deg >= 45 else False)

    delta_azimuth = azimuth_deg - previous_azimuth_deg
    steps = int(float(delta_azimuth) * stepper_step_deg)
    if steps > 100:
        # Go the other direction (prevent a lot of motion)
        steps = 200 - int((steps**2)**(1/2))
        steps *= -1
    if (steps**2)**(1/2) > 0:
        previous_azimuth_deg = azimuth_deg

    for step in range(int((steps**2)**(1/2))):
        stepper.step(steps < 0)
    stepper.relax()

    servo.angle(altitude_deg + 90)

    time.sleep(0.5)
