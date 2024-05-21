'''
My program is going to determine which bus I should take in the morning to commute to school and inform me of the weather that day. Program will save me time, I can check both the weather and how to get to school at the same time instead of individually. Pulls data from google  directions api(https://developers.google.com/maps/documentation/directions/overview) to determine which bus to take, what time to leave the house and what time I will arrive at the destination. Weather data will come from openweathermap api (https://openweathermap.org/api), data on temperature, wind, rain and snow are sourced from here. Api keys for both are contained within a file and read by the program. Data output from both are in JSON format, get wanted data from both by indexing. Get start location and end destination for directions from user input. For google urls words are separated by ‘+’ instead of a space, so must convert inputted strings to proper format. For weather data user inputs which city to get weather data from. Wind speeds given in m/s, convert to words putting speeds into context. I have suede shoes I enjoy wearing, so I will create an optional check of precipitation for shoes, decided by user input. Will tell me if it has rained or snowed in the past 3 hours and if it will provide a warning(cannot get suede wet). After obtaining all the data I will output the type of weather today, temperature, state of the wind, which bus to take to get to my destination, and if requested, a check for my shoes. Program only provides data on the first bus to take,it is designed to quickly inform me of which bus to get on so I do not miss it.
'''
import requests

#get google maps API key
gApi_read=open("api_key.txt", 'r')
gApi_key=gApi_read.read()
gApi_read.close()

#input start address, typing home gives location near my home
start = input('Start Address?: ')

#input destination address, typing tmu sets address to 350 Victoria St
Destination = input('Destination?: ')

#file for console output
output = open('cps109_a1_output.txt','w', encoding = 'utf-8')

def convertAddress(start, Destination):
    #get compatible formatting of start address and end address
    while '  ' in start:
        #prevents incorrect url by not accepting inputs with double spaces
        print('Invalid Input, Doubled Spaces')
        print('Invalid Input, Doubled Spaces', file = output)
        start=input('Retry start address: ')

    if start == 'home' or Destination == 'home':
        #quick way to set start to place close to home address
        start='75+Pinegrove+Avenue+Toronto+ON'
    
    else:
        start=start.replace(' ', '+')
    
    while '  ' in Destination:
        #prevents incorrect url by not accepting inputs with double spaces
        print('Invalid Input, Doubled Spaces')
        print('Invalid Input, Doubled Spaces', file = output)
        Destination=input('Retry destination: ')
        
    if Destination == 'tmu' or Destination == 'home':
        #quick way for directions to school
        Destination = '350+Victoria+St+Toronto+ON'
        
    else:
        #converts spaces to plus symbol (correct format for google url)
        Destination=Destination.replace(' ', '+')
    
    return [start, Destination]
        
start, Destination = convertAddress(start, Destination)[0], convertAddress(start, Destination)[1]

#url for google maps(to be accessed using requests module)
url = 'https://maps.googleapis.com/maps/api/directions/json?units=metric&mode=transit&'

#using request module, get data from google maps directions
data = requests.get(url + 'origin=' + start + '&destination=' + Destination + '&key=' + gApi_key).json()

#index into data to get desired data
busToTake = data["routes"][0]["legs"][0]["steps"][1]["transit_details"]["line"]["short_name"]
timeToLeave = data["routes"][0]["legs"][0]["departure_time"]["text"]
arrivalTime = data["routes"][0]["legs"][0]["arrival_time"]["text"]

def weather():
    #gets weather info, temp, wind, forecast, wind chill
    wApi_read=open('weather_key.txt', 'r') #gets api key from file on my pc
    wApi_key=wApi_read.read()
    wApi_read.close()
    
    city=input('City?: ')
    #weather equals output from request to weather api
    weather = requests.get('https://api.openweathermap.org/data/2.5/weather?q='+city + '&units=metric&appid='+wApi_key).json()
    temp=weather['main']['temp']
    eTemp=weather['main']['feels_like']
    forecast= weather['weather'][0]['main']
    wind=weather['wind']['speed']
    #variables above contain info on the weather by indexing into weather variable
    #messages based on wind speed, windy/breezy/none
    if wind > 8.9:  
        windQuip="Watch out it's a windy day!"
    elif wind > 6.7:
        windQuip = 'Bit of a breeze today!'
    else:
        windQuip = 'Barely any wind today'
    windState = 'Wind speeds averaging ' + str(wind) + ' m/s, ' + windQuip
    print('\nWeather today is ' + forecast + '\n' + windState + '\n' + str(temp) + '°C ' + 'feels like ' + str(eTemp) + '°C')
    print('\nWeather today is ' + forecast + '\n' + windState + '\n' + str(temp) + '°C ' + 'feels like ' + str(eTemp) + '°C', file = output)
    #windState printed to console later in program, describes the wind situation
    
    if forecast=='Rain':
        try:
            #rain data are only given when it is raining, so must use try and except to not run into errors
            rain=weather['rain']['rain.1h']
            print(str(rain) + 'mm of rain in the past hour')
            print(str(rain) + 'mm of rain in the past hour', file = output)
        except:
            print('No rain for the past hour!')
            print('No rain for the past hour!', file = output)
    
    elif forecast=='Snow':
        try:
            #snow data are only given when it is snowing, so must use try and except to not run into errors
            snow=weather['snow']['snow.1h']
            print(str(snow) + 'mm of snow in the past hour')
            print(str(snow) + 'mm of snow in the past hour', file = output)
        except:
            print('No snow for the past hour!')
            print('No snow for the past hour!', file = output)

        
def checkForShoes():
    weatherTypes=[]
    try:
        #check for rain or snow in general, could rain or snow in past 3 hours but have a different forecast, appends it to a list
        weatherTypes.append(weather['rain']['rain.3h'])
       
    except:
        weatherTypes.append(0)
        try:
            weatherTypes.append(weather['snow']['snow.3h'])
        except:
            weatherTypes.append(0)
            
    #warning to not wear suede shoes if the ground/air will be wet(rain or snow) determined by whether the list is empty or not
    wetness=[x for x in weatherTypes if x>0]
    if wetness==[]:
        print('No rain or snow, wear whatever!')
        print('No rain or snow, wear whatever!', file = output)

    else:
        print("Raining or Snowing, Don't wear suede!")
        print("Raining or Snowing, Don't wear suede!", file = output)
    

weather()
#prints data from google directions api to console after calling weather function
print('leave at ' + timeToLeave +', take the ' + busToTake + ', arrive at ' + arrivalTime + '(estimated)\n')
print('leave at ' + str(timeToLeave) +', take the ' + str(busToTake) + ', arrive at ' + str(arrivalTime) + '(estimated)\n', file = output)

shoeCheck=input('check weather for shoes? (Y/N): ')
shoeCheck=shoeCheck.upper()
while shoeCheck!= 'Y' and shoeCheck!='N':
    #checks proper inputs for shoeCheck
    shoeCheck=input('check weather for precipitation? (Y/N): ')

if shoeCheck == 'Y':
    #if user inputs 'y' for yes, calls checkForShoes function
    checkForShoes()

output.close()

