# SolarEnergyPy

## SolarEnergyPy

SolarEnergyPy is for education purpose where one can have fundamental information of solar energy.

## Basic Information
- Solar constant.
- Solar position relative to a site on Earth in terms of lattitude, longitude and datetime.
- Instant solar radiation on outer edge of atmosphere as well as beam and diffusion on Earth.
- Spectral radiation map.


## Requirements

* [Python](http://www.python.org) 3 
* Matplotlib is installed.

## Documentation

To be continued.

## Installation
```bash
pip install SolarEnergyPy
```

## Usage
```Python
from datetime import datetime

import pendulum

from SolarEnergyPy.solarPosition import solarPosition as sp

from SolarEnergyPy.solarRadiation import solarRadiation as sr



def solar_system_demo(longitude, latitude, dt):



    solar_position = sp(longitude, latitude)

    solar_radiation = sr()

    solar_position.clocktime = dt

    solar_radiation.clocktime = dt



    print(f"Solar Position:{sp.site}")

    print(f"Date-Time: {solar_position._datetime}")

    print(f"Latitude: {solar_position.latitude}")

    print(f"Longitude: {solar_position.longitude}")

    print(f"Declination: {solar_position.declination}")

    print(f"Solar Azimuth: {solar_position.solar_azimuth}")

    print(f"Solar Zenith: {solar_position.zenith}")



    print("\nSolar Radiation:")

    beam, diffuse = solar_radiation.solar_radiation_at()

    print(f"Beam Radiation: {beam} W/m^2")

    print(f"Diffuse Radiation: {diffuse} W/m^2")



if __name__ == '__main__':

    longitude = 112

    latitude = 31

    dt = pendulum.now('Asia/Shanghai')

    solar_system_demo(longitude, latitude, dt)
```

## Update log
`0.0.4` fix some bugs
`0.0.3` Add some demos

`0.0.2` Fix some bugs and and add case demos

`0.0.1` SolarEnergyPy

## License

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

## Contact
heliqun@ustc.edu.cn
