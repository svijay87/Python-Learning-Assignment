
import requests
from abc import ABC,abstractmethod
import logging
import json
import unittest

logging.basicConfig(filename="Nasa-shooting-star.log",filemode="a",format="%(asctime)s|%(process)s|%(level)s|%(message)s",level=logging.INFO)
log = logging.getLogger('Nasa-logger')

class Universe(ABC):
    @abstractmethod
    def fireball(self):
        pass


class Nasa(Universe):
    def __init__(self, f_date, t_date):
        self.from_date = f_date
        self.to_date   = t_date  
       
    def __get_data_from_Nasa(self):
        try:
            Nasa_api_url = f"https://ssd-api.jpl.Nasa.gov/fireball.api?date-min={self.from_date}&date-max={self.to_date}&req-alt=true&sort=-energy"
           
            res = requests.get(Nasa_api_url)
            res.raise_for_status()            
            result = json.loads(res.content)      
            return result
           
        except Exception as e:
            msg = f'Exception occur while retrieve response from {url}. Exception :: {e}'
            # print(msg)
            log.fatal(msg)
   
    def fireball(self):
        """Nasa’s public HTTP APIs to create a function which determines
        which of three locations has seen the brightest shooting stars
        since 2017"""
   
        # Prepare data for fetching info from
        lat_lng_info = {
            'BOSTON'         : (42.354558,'N',71.054254,'W'),
            'NCR'            : (28.574389,'N',77.312638,'E'),
            'SAN Francisco'  : (37.793700,'N',122.403906,'W')
        }
       
        try:
            highest_energy = 0.0
           
            ofc_brightest_result = {}
            result = self.__get_data_from_Nasa()
            for record in result['data']:
                energy = float(record[1])
                lat,lat_dir,lng,lng_dir =           float(record[3]),record[4],float(record[5]),record[6]                                              
                for ofc_name, ofc_lat_lng_val in lat_lng_info.items():
                    if ( lat > (ofc_lat_lng_val[0] - 15 ) and lat <
                (ofc_lat_lng_val[0] + 15 ) ) \
                    and ( lng > (ofc_lat_lng_val[2] - 15 ) and lng <
                (ofc_lat_lng_val[2] + 15 ) ) \
                    and ( ofc_lat_lng_val[1] == lat_dir \
                         and ofc_lat_lng_val[3] == lng_dir ):                        
                        if energy > highest_energy:
                            highest_energy = energy
                            ofc_brightest_result[highest_energy] = \
                            [ofc_name,lat,lng]
                            print(f'{ofc_name} :: latitude {lat} :: longitude \
                            {lng} :: energy :: {highest_energy}')
                                               
           
            print(ofc_brightest_result[highest_energy])
            return 0
           
        except Exception as e:
            log.error(f'Exception occur while retrieve response.  Exception :: {e}')
            return 1
       
   
   
# Create object of Nasa    
Nasa_obj = Nasa('2017-01-01','2020-01-01')
rc = Nasa_obj.fireball()
if rc == 0:
    print('Program working fine')    

   
class Nasa_Test(unittest.TestCase):    
   
    def assert_equal_test(self):
        self.assertEqual(rc, 0)
       
    def assert_is_instance(self):
        Nasa_object = Nasa('2017-01-01','2020-01-01')
        self.assertIsIstance(Nasa_object,Nasa, "Object is instance of Nasa Class")  
           
       
ts = unittest.TestSuite()
ts.addTests([Nasa_Test('assert_equal_test'),Nasa_Test('assert_is_instance')])

# Trigger the tests now
unittest.TextTestRunner().run(ts)
