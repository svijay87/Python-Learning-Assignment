

from abc import ABC, abstractmethod
import requests
import json
import unittest


class Universe(ABC):

    @abstractmethod
    def firewall(self):
        pass

class NASA(Universe):
    def __init__(self, from_date : str, to_date : str) :
        self.cname = 'NASA'
        self.from_date = from_date
        self.to_date = to_date
   
    def firewall(self) -> bool:
        print('This is the implementation')
       
        url = f"https://ssd-api.jpl.nasa.gov/fireball.api?date-min={self.from_date}&date-max={self.to_date}&req-alt=true&sort=-energy"
       
        res = requests.get(url)
       
        res.raise_for_status
       
        print(res.content)
        return True
       
class ISRO(NASA):
    def __init__(self, from_date : str, to_date : str):
        print('INIT ISRO')
        print(from_date)
        self.from_date = from_date
        self.to_date = to_date
   
    def fireball(self):
        print('ISRO Fireball called')
        super().fireball()


obj_nasa = NASA('2017-01-01','2020-01-01')
obj_nasa.firewall()

try:
    isro_obj = ISRO('2017-01-01','2020-01-01')
    #print(isro_obj.firewall())
except TypeError as te:
    print(f'Type error occured while creating obj of ISRO :: {te}')

print('Done')

