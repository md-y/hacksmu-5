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

N = 1000
assets = []
#criticality level & energy efficiency [0,10]
asset_names = [
    {
        "name": "Elevator",
        "criticality_level" : 5,
        "time_between_service": 365*24,
        "cost": 55000,
        "energy_efficiency": 4,
        "weight": 5000,
        "height_from_floor": 0,
        "operation_rate": 1,
    },
    {
        "name": "Plumbing System",
        "criticality_level" : 9,
        "time_between_service": 365 * 24,
        "cost": 75000,
        "energy_efficiency": 6,
        "weight": 4000,
        "height_from_floor": 0,
        "operation_rate": 1,
    },
    {
        "name": "Fire Alarm",
        "criticality_level" : 8,
        "time_between_service": 365 * 12,
        "cost": 1000,
        "energy_efficiency": 9,
        "weight": 5,
        "height_from_floor": 8,
        "operation_rate": 365,
    },
    {
        "name": "HVAC",
        "criticality_level" : 3,
        "time_between_service": 365 * 12,
        "cost": 500000,
        "energy_efficiency": 2,
        "weight": 2000,
        "height_from_floor": 10,
        "operation_rate": 7,
    },
    {
        "name": "Electrical Panel",
        "criticality_level" : 4,
        "time_between_service": 365 * 6,
        "cost": 3000,
        "energy_efficiency": 5,
        "weight": 75,
        "height_from_floor": 5,
        "operation_rate": 30,
    }
]
employee_names = ["David", "Nevin", "Sam", "Jayesh", "Bob", "Jerry", "Charlene", "Dolly"]
MAX_FLOOR = 72
MAX_ROOM = 200
#date(year,month,day)
INSTALLATION_START_DATE = '01/01/2015'
INSTALLATION_END_DATE = '06/16/2023'

def addDaysToDate(curDate, days):
    month, day, year = curDate.split('/')
    start = date(int(year),int(month),int(day))
    start = start + timedelta(days)
    return str(start.month) + '/' + str(start.day) + '/' + str(start.year)

def randomDate(start, end, n = -1):
    month, day, year = INSTALLATION_START_DATE.split('/')
    start = date(int(year),int(month),int(day))
    month, day, year = INSTALLATION_END_DATE.split('/')
    end = date(int(year),int(month),int(day))
    daysBetween = (end - start).days

    #n is number of days on average += 20%
    if n != -1:
        n = daysBetween // n
        n = random.randint((int)(n * .8), (int)(n * 1.2))
    else:
        n = 1
    results = []
    for i in range(n):
        newDate = start + timedelta(random.randint(0,daysBetween))
        results.append(newDate)
    results.sort()
    for i in range(len(results)):
        results[i] = str(results[i].month) + '/' + str(results[i].day) + '/' + str(results[i].year)
    if len(results) == 1:
        return results[0]
    else:
        return results

for i in range(N):
    assetInfo = random.choice(asset_names)
    install_date = randomDate(INSTALLATION_START_DATE, INSTALLATION_END_DATE)
    #error logs & service & work order repots generated
    error_logs = randomDate(install_date, INSTALLATION_END_DATE, assetInfo["time_between_service"] / 24)
    service_reports = []
    work_orders = []
    for j in range(len(error_logs)):
        days_to_work_order = random.randint(0,7)
        days_to_service = random.randint(0,7)
        day = error_logs[j]
        error_logs[j] = {
                "Logger Name": random.choice([random.choice(employee_names), "Automated Error Logging"]),
                "Log Description": "This is a random operational log",
                "Log Date": day
            }
        work_orders.append({
                "Filer Name": random.choice(employee_names),
                "File Date": addDaysToDate(day, days_to_work_order),
                "Completion Date": addDaysToDate(day, days_to_work_order + days_to_service),
                "Description": "This is a random work order description"
            })
        service_reports.append({
                "Servicer Name": random.choice(employee_names),
                "Service Description": "This is a random service description",
                "Date Serviced": addDaysToDate(day, days_to_work_order + days_to_service),
                "Cost": {
                    "$numberInt": random.randint(assetInfo["cost"] // 100, assetInfo["cost"] // 2),
                },
                "Service Reason": "This is a random service reason"
            
            })
        
        
    #operational logs
    operational_logs = randomDate(install_date, INSTALLATION_END_DATE, assetInfo["operation_rate"])[-10:]

    for j in range(len(operational_logs)):
        operational_logs[j] = {
                "Logger Name": random.choice(employee_names),
                "Log Description": "This is a random operational log",
                "Log Date": operational_logs[j]
            }

    asset = {
        "Asset ID": {
            "$numberInt": i,
        },
        "Asset Type": assetInfo["name"],
        "Floor": {
            "$numberInt": random.randint(0,MAX_FLOOR)
        },
        "Room": {
            "$numberInt": random.randint(0, MAX_ROOM)
        },
        "Installation Date": install_date,
        "Manufacturer": "Manufacturer_" + str(random.randint(1,5)),
        "Operational Time (hrs)": {
            "$numberInt": str(random.randint(1,50000))
        },
        "Criticality Level": {
            "$numberInt": assetInfo["criticality_level"]
        },
        "Error Logs": error_logs,
        "Operational Logs": operational_logs,
        "Service Reports": service_reports,
        "Time Between Services": {
            "$numberInt": assetInfo["time_between_service"]
        },
        "Work Orders": work_orders,
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
        },
        "location" : {
            "type": "Point",
            "coordinates": ["",""]
        }
    }

    assets.append(asset)

#store assets
# Serializing json
json_object = json.dumps(assets, indent=2)
 
# Writing to sample.json
with open("dataset.json", "w") as outfile:
    outfile.write(json_object)


