# WeatherCls

![PyPI - Version](https://img.shields.io/pypi/v/weathercls)

A Python library for storing and managing weather-related dataclasses from APIs.

## Installation

```bash
pip install weathercls
```

## Basic Usage
You can initialize the class manually or convert a `Dictionary` into the corresponding class using other libraries such as [dacite](https://github.com/konradhalas/dacite).
```python
from dacite import from_dict
from weathercls.weatherapicom import transform_to_snake_case
from weathercls.weatherapicom.forecast_weather.ForecastWeather import ForecastWeather

weather_forecast = {...}
weather_forecast = transform_to_snake_case(weather_forecast) # converts keys with dashes to underscores for better compatibility with dacite

forecast_weather = from_dict(data_class=ForecastWeather, data=weather_forecast)
print(forecast_weather)
```

## List of Classes by Weather APIs
| Name               | Package                                                    |
| ------------------ | ---------------------------------------------------------- |
| **weatherapi.com** | [**weathercls.weatherapicom**](/weathercls/weatherapicom/) |
