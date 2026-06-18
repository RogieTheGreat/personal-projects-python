"""
Basic Class Set-Up
"""

import json

class Person:
    def __init__(self,name, type):
        self.name = name    # Attributes
        self.type = type    # Attributes

    def say_hello(self): #  method
        print(f"Hello {self.name} [{self.type}]")

    def conv_to_dict(self):
        return {
            "name": self.name,
            "type": self.type
        }

    @classmethod
    def conv_from_dic(cls, data):
        return Person(data["name"], data["type"])
    

    """
    
    class Person:

        def __init__(self, name):
            self.name = name

        def say(self):                  # needs object
            print(self.name)

        @classmethod
        def create(cls, name):         # creates object
            return cls(name)


        :.  NORMAL METHOD → USE existing object
            CLASS METHOD  → CREATE new object
    """

    """
    To name or make my own
    """

    def my_decorator(func):
        return func

    # Then

    @my_decorator
    def hello():
        pass


robot_x = Person("R-o-G", "PH3SXJP") # This is now object

robot_x.say_hello() # Runs that method of function under that class

## Save to JSON
with open("file_name.json", "w") as f:
    json.dump(robot_x.conv_to_dic(), f)



## Load from JSON
with open("file_name.json", "r") as f:
    data = json.load(f)

robot_y = Person.conv_from_dic(data)

print(f"Welcome back {robot_y.name} [{robot_y.type}]")
