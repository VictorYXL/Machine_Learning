import json
import urllib
import KMeans
import KMeans

def GetGeo(city, street):
    #Get url for baidu map
    apiStem = 'http://api.map.baidu.com/geocoder?'
    params = {}
    params['address'] = street
    params['output'] = 'json'
    params['key'] = '6eea93095ae93db2c77be9ac910ff311'
    params['city'] = city
    url = apiStem + urllib.parse.urlencode(params)

    #Send request and get responce
    responce = urllib.request.urlopen(url)

    #Extract the point from responce
    result = json.load(responce)
    if 'status' in result and result['status'] == 'OK' and 'location' in result['result'] and 'lng' in result['result']['location'] and 'lat' in result['result']['location']:
        return result['result']['location']['lng'], result['result']['location']['lat']
    return None

def LoadPlace(fileName):
    file = open(fileName,'r', encoding = 'UTF-8')
    geoDataArray = []
    for line in file.readlines():
        place = line.strip().split(' ')
        if len(place) != 2:
            continue
        geoData = GetGeo(place[0], place[1])
        if geoData != None:
            geoDataArray.append(geoData)
    return geoDataArray
if __name__ == '__main__':
    dataArray = LoadPlace('Xianyang.txt')
    clusterPointMat, clusterAssement = KMeans.BinKMeans(dataArray, 3)
    KMeans.Plot(dataArray, clusterPointMat, clusterAssement)