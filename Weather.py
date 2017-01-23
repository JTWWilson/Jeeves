import datapoint

locations = {}
# For each line in settings.txt
for line in open('Places.txt').readlines():
    print line
    keys = []
    latitude = ''
    longitude = ''
    reading = 'key'
    key = ''
    for char in line:
        if char == '#':
            break
        elif reading == 'key':
            if char == ',':
                keys.append(key)
                key = ''
            elif char not in ['=', ' ', '\n' ','] and reading == 'key':
                key += char
            elif char == '=' and reading == 'key':
                keys.append(key)
                reading = 'latitude'
        elif reading == 'latitude':
            if char == ',':
                reading = 'longitude'
            elif char not in ['\n', ' ']:
                latitude += char
        elif reading == 'longitude':
            if char not in ['\n', ' ']:
                longitude += char
    for i in keys:
        if i != '':
           locations[i] = [latitude, longitude]

print locations

def get_forecast_for_lat_lon(latitude, longitude):
    """
    Takes latitude and longitude and returns a basic weather reading
    :param latitude: Latitude of site
    :param longitude: Longitude of site
    :return: Name of site, Description (e.g. Overcast), Temperature (raw number in degrees Celsius)
    """

    # Create datapoint connection
    conn = datapoint.Manager(api_key="****")

    # Get nearest site and print out its name
    site = conn.get_nearest_site(latitude=latitude, longitude=longitude)
    # print site.name

    # Get a forecast for the nearest site
    forecast = conn.get_forecast_for_site(site.id, "3hourly")
    # Get the current timestep using now() and print out some info
    # print forecast.now().weather.text
    # print "%s%s%s" % (forecast.now().temperature.value,
    #                   u'\xb0', #Unicode character for degree symbol
    #                   forecast.now().temperature.units)
    return site.name, forecast.now().weather.text, forecast.now().temperature.value


def get_forecast_for_name(site_name):
    """
    Takes a site name and returns a basic weather reading
    :param site_name: Name of site
    :return: Name of site, Description (e.g. Overcast), Temperature (raw number in degrees Celsius)
    """

    latitude, longitude = locations[site_name]
    return get_forecast_for_lat_lon(latitude, longitude)

if __name__ == '__main__':
    print(get_forecast_for_lat_lon(52.65100, -0.479033))
    print(get_forecast_for_name('BGS'))
