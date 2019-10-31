# home-sensors
### Abstract
A small, portable weather-station, capable of measuring outside and inside temperature, atmospheric pressure, humidity and air quality. This data should get reported to a Google AppEngine project, which should update a Google spreadsheet. The AppEngine should also have a route serving a simple and responsive HTML page showing the latest readings from all sensors and perhaps have routes performing some number-crunching (averages, min, max, etc.)

### Parts list
<ul>
    <li>Raspberry Pi 2 Model B</li>
    <li>SDS011 2.5PM and 10PM dust sensor</li>
    <li>GY-BME280 temperature, barometer and humidity sensor</li>
    <li>One (or two) DS18B20 temperature probes</li>
<ul>
