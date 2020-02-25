import json
import geopy
import folium
import certifi
import ssl
import twitter2_1
from geopy.geocoders import Nominatim

from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/', methods=['GET'])
def main_page():
    return render_template('index.html')


def find_location(element):
    """
    dict -> list
    Find names and locations of all username's friends
    and return list of tuple, which consists of friend's
    name and friend's location.
    """
    information = []
    for i in element['users']:
        if len(i['location']) != 0:
            inform = (i['screen_name'], i['location'])
            information.append(inform)
    return information


def define_coordinates(tup_locs):
    """
    list -> list
    Define coordinates of each friend's location and
    return list of smaller lists: the list of friend's
    name, the list of latitudes and list of longitudes.
    """
    dict_locs = dict(tup_locs)
    names = []
    latitude = []
    longitude = []

    ctx = ssl.create_default_context(cafile=certifi.where())
    geopy.geocoders.options.default_ssl_context = ctx

    new_dict = {}
    for element in dict_locs:
        geolocator = Nominatim(user_agent="app_name",
                               timeout=10)
        location = geolocator.geocode(dict_locs[element])
        try:
            if location is not None:
                coord_tup = (location.latitude, location.longitude)
                if coord_tup not in new_dict:
                    new_dict[coord_tup] = []
                    new_dict[coord_tup].append(element)
                else:
                    new_dict[coord_tup].append(element)
        except:
            continue

    for key in new_dict:
        latitude.append(list(key)[0])
        longitude.append(list(key)[1])
        names.append(new_dict[key])
    coordinates = [latitude, longitude, names]
    return coordinates


def make_map(coordinates):

    all_lat = coordinates[0]
    all_long = coordinates[1]
    all_friends = coordinates[2]

    map_ = folium.Map(titles='World Map',
                      location=['48.3794', '31.1656'],
                      tiles="Stamen Terrain",
                      zoom_start=3)
    feat_friends = folium.FeatureGroup(name="Friends")
    for lt, ln, friend in zip(all_lat, all_long, all_friends):
        friend_ = ' '.join(friend)
        feat_friends.add_child \
            (folium.Marker(location=[lt, ln],
                           popup=friend_,
                           icon=folium.Icon(icon='home',
                                            color='red')))

    map_.add_child(feat_friends)
    html_str_map = map_.get_root().render()
    return html_str_map


@app.route('/add_message', methods=['POST'])
def generate_map():
    try:
        name = request.form['name']
        data = twitter2_1.friends_information(name)
        locations = find_location(data)
        coordinates = define_coordinates(locations)
        context = {"html_str_map": make_map(coordinates)}
        return render_template('map.html', **context)
    except:
        return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True, port=7000)
