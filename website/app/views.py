from app import app
from flask import render_template, request, redirect, session
import json, os, subprocess

# Define directory
dir = os.path.dirname(__file__)

def get_error():
    with open(os.path.join(dir, '../../config.json'), 'r') as file:
        config = json.load(file)

    return config['_error']

def get_gps():
    with open(os.path.join(dir, '../../config.json'), 'r') as file:
        config = json.load(file)

    return config['gps']

def set_gps(gps):
    with open(os.path.join(dir, '../../config.json'), 'r') as file:
        config = json.load(file)

    config['gps'] = gps

    with open(os.path.join(dir, '../../config.json'), 'w') as file:
        json.dump(config, file)

def get_standard():
    with open(os.path.join(dir, 'objects.json'), 'r') as file:
        objects = json.load(file)

    return objects['standard']

def get_custom():
    with open(os.path.join(dir, 'objects.json'), 'r') as file:
        objects = json.load(file)

    return objects['custom']

def get_current():
    with open(os.path.join(dir, '../../config.json'), 'r') as file:
        config = json.load(file)

    return {'name': config['name']}

def set_current(name):
    with open(os.path.join(dir, '../../config.json'), 'r') as file:
        config = json.load(file)
    with open(os.path.join(dir, 'objects.json'), 'r') as file:
        objects = json.load(file)

    all = objects['standard'] + objects['custom']
    for object in all:
        if object['name'] == name:
            config['name'] = object['name']
            if 'data' in object.keys():
                config['data'] = object['data']
            else:
                config.pop('data', None)
            break

    with open(os.path.join(dir, '../../config.json'), 'w') as file:
        json.dump(config, file)

def save_object(object):
    with open(os.path.join(dir, 'objects.json'), 'r') as file:
        objects = json.load(file)
    custom = objects['custom']
    custom.append(object)
    objects['custom'] = custom
    with open(os.path.join(dir, 'objects.json'), 'w') as file:
        json.dump(objects, file)

def del_object(id):
    with open(os.path.join(dir, 'objects.json'), 'r') as file:
        objects = json.load(file)
    objects['custom'] = [object for index, object in enumerate(objects['custom']) if index+1 != int(id)]
    with open(os.path.join(dir, 'objects.json'), 'w') as file:
        json.dump(objects, file)

@app.route('/')
def index():
    return render_template('index.html', time=session.get('time'), gps=get_gps(), hor_error=get_error(), current_object=get_current(), standard_objects=get_standard(), custom_objects=get_custom())

@app.route('/set-gps', methods=['POST'])
def set_gps_web():
    set_gps(request.form['gps'])
    return redirect('/#change-location')

@app.route('/add-object', methods=['POST'])
def add_object_web():
    save_object({'name': request.form['object-name'].strip(), 'data': request.form['object-data'].split('\r\n')})
    return redirect('/#add-object')

@app.route('/set-object', methods=['POST'])
def set_object_web():
    set_current(request.form['object-selector'])
    return redirect('/#select-object')

@app.route('/del-object', methods=['POST'])
def del_object_web():
    del_object(request.form['object-delete'])
    return redirect('/#previously-added')

@app.route('/fix-time', methods=['POST'])
def fix_time_web():
    time = request.form['time']
    subprocess.call(['sudo', 'date', '-s', f'{time}'])
    session['time'] = True
    return redirect('/')
