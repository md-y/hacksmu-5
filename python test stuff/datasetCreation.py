import json
import random
from datetime import date, timedelta
#This file creates the dataset

#sample asset
# {
#     "_id": {
#         "$oid": "6506219063e84859ba1a2eab"
#     },
#     "Asset ID": {
#         "$numberInt": "1"
#     },
#     "Asset Type": "Elevator",
#     "Floor": {
#         "$numberInt": "7"
#     },
#     "Room": {
#         "$numberInt": "103"
#     },
#     "Installation Date": "1/6/2020",
#     "Manufacturer": "Manufacturer_4",
#     "Operational Time (hrs)": {
#         "$numberInt": "39313"
#     },
#     "Repairs": {
#         "$numberInt": "1"
#     },
#     "Last Serviced Date": "6/19/2023",
#     "Criticality Level": {
#         "$numberInt": "0"
#     },
#     "Error Logs": [
#         {
#             "Logger Name": "",
#             "Date": "",
#             "Description": ""
#         }
#     ],
#     "Operational Logs": [
#         {
#             "Logger Name": "",
#             "Log Description": "",
#             "Log Date": ""
#         }
#     ],
#     "Service Reports": [
#         {
#             "Servicer Name": "",
#             "Service Description": "",
#             "Date Serviced": "",
#             "Cost": {
#                 "$numberInt": "0"
#             },
#             "Service Reason": ""
#         }
#     ],
#     "Time Between Services": {
#         "$numberInt": "0"
#     },
#     "Work Orders": [
#         {
#             "Filer Name": "",
#             "File Date": "",
#             "Completion Date": "",
#             "Description": ""
#         }
#     ],
#     "Cost": {
#         "$numberInt": "0"
#     },
#     "Energy Efficiency": {
#         "$numberInt": "0"
#     },
#     "Weight": {
#         "$numberInt": "0"
#     },
#     "Height From Floor": {
#         "$numberDouble": "0.0"
#     }
# }

N = 2
assets = []
#criticality level & energy efficiency [0,10]
asset_names = [
    {
        "name": "Elevator",
        "criticality_level" : 5,
        "time_between_service": 4000,
        "cost": 100000,
        "energy_efficiency": 5,
        "weight": 2000000,
        "height_from_floor": 0,
    },
    {
        "name": "Plumbing System",
        "criticality_level" : 9,
        "time_between_service": 8000,
        "cost": 5000000,
        "energy_efficiency": 5,
        "weight": 200000,
        "height_from_floor": 0,
    },
    {
        "name": "Fire Alarm",
        "criticality_level" : 5,
        "time_between_service": 16000,
        "cost": 50,
        "energy_efficiency": 5,
        "weight": 1,
        "height_from_floor": 8,
    }
]
employee_names = ["David", "Nevin", "Sam", "Jayesh", "Bob", "Jerry", "Charlene", "Dolly"]
MAX_FLOOR = 100
MAX_ROOM = 400
#date(year,month,day)
INSTALLATION_START_DATE = '01/01/2015'
INSTALLATION_END_DATE = '09/16/2023'

def randomDate(start, end):
    month, day, year = INSTALLATION_START_DATE.split('/')
    start = date(int(year),int(month),int(day))
    month, day, year = INSTALLATION_END_DATE.split('/')
    end = date(int(year),int(month),int(day))
    daysBetween = (end - start).days
    newDate = start + timedelta(random.randint(0,daysBetween))
    return str(newDate.month) + '/' + str(newDate.day) + '/' + str(newDate.year)

for i in range(N):
    assetInfo = random.choice(asset_names)
    install_date = randomDate(INSTALLATION_START_DATE, INSTALLATION_END_DATE)
    asset = {
        "Asset ID": {
            "$numberInt": i,
        },
        "Asset Type": assetInfo["name"],
        "Floor": {
            "$numberInt": MAX_FLOOR
        },
        "Room": {
            "$numberInt": random.randint(0, MAX_ROOM)
        },
        "Installation Date": install_date,
        "Manufacturer": "Manufacturer_" + str(random.randint(0,10)),
        "Operational Time (hrs)": {
            "$numberInt": str(random.randint(1,100000))
        },
        "Criticality Level": {
            "$numberInt": assetInfo["criticality_level"]
        },
        "Error Logs": [
            {
                "Logger Name": random.choice(employee_names),
                "Date": randomDate(install_date, INSTALLATION_END_DATE),
                "Description": "This is a random error log"
            }
        ],
        "Operational Logs": [
            {
                "Logger Name": random.choice(employee_names),
                "Log Description": "This is a random operational log",
                "Log Date": randomDate(install_date, INSTALLATION_END_DATE)
            }
        ],
        "Service Reports": [
            {
                "Servicer Name": random.choice(employee_names),
                "Service Description": "This is a random service description",
                "Date Serviced": randomDate(install_date, INSTALLATION_END_DATE),
                "Cost": {
                    "$numberInt": random.randint(assetInfo["cost"] // 100, assetInfo["cost"] // 2),
                },
                "Service Reason": "This is a random service reason"
            }
        ],
        "Time Between Services": {
            "$numberInt": assetInfo["time_between_service"]
        },
        "Work Orders": [
            {
                "Filer Name": random.choice(employee_names),
                "File Date": randomDate(install_date, INSTALLATION_END_DATE),
                "Completion Date": randomDate(install_date, INSTALLATION_END_DATE), #FIX THIS LINE, THE COMPLETION DATE CAN BE AFTER THE FILE DATE
                "Description": "This is a random description"
            }
        ],
        "Cost": {
            "$numberInt": assetInfo["cost"],
        },
        "Energy Efficiency": {
            "$numberInt": assetInfo["energy_efficiency"]
        },
        "Weight": {
            "$numberInt": assetInfo["weight"]
        },
        "Height From Floor": {
            "$numberDouble": assetInfo["height_from_floor"]
        }
    }

    assets.append(asset)

#store assets
# Serializing json
json_object = json.dumps(assets, indent=2)
 
# Writing to sample.json
with open("dataset.json", "w") as outfile:
    outfile.write(json_object)


