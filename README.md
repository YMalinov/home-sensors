# home-sensors
### Abstract
Simple, light-weight service, hosted in AppEngine, capable of receiving sensor readings from one or more clients and put that data in a Google Sheet. Currently, the clients are two Raspberries I had lying around - one of them is installed outside and sends out data about the air pressure, humidity, temperature and dust buildup (PM); the other one is inside and measures the temperature in my room.

### Parts list
<ul>
    <li>Raspberry Pi 1 Model B+ & Raspberry Pi 2 Model B</li>
    <li>SDS011 2.5PM and 10PM dust sensor</li>
    <li>GY-BME280 temperature, barometer and humidity sensor</li>
    <li>Two DS18B20 temperature probes, fitted in a weather-resistant cable</li>
<ul>
