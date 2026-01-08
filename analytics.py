from bson import ObjectId



# Devices per Location


def devices_per_location_aggregation(db):
    pipeline = [
        {
            "$group": {
                "_id": "$locationId",
                "deviceCount": {"$sum": 1}
            }
        },
        {
            "$lookup": {
                "from": "locations",
                "localField": "_id",
                "foreignField": "_id",
                "as": "location"
            }
        },
        {"$unwind": "$location"},
        {
            "$project": {
                "_id": 0,
                "Location": {
                    "$concat": [
                        "$location.address.city", ", ",
                        "$location.address.street", ", ",
                        "$location.address.building"
                    ]
                },
                "Devices": "$deviceCount"
            }
        },
        {"$sort": {"Devices": -1}}
    ]

    return list(db.devices.aggregate(pipeline))



 #Average Readings per Device

def avg_readings_per_device_aggregation(db):
    pipeline = [
        {
            "$project": {
                "deviceId": 1,
                "valuesArray": {"$objectToArray": "$values"}
            }
        },
        {"$unwind": "$valuesArray"},
        {
            "$group": {
                "_id": {
                    "deviceId": "$deviceId",
                    "metric": "$valuesArray.k"
                },
                "avgValue": {"$avg": "$valuesArray.v"}
            }
        },
        {
            "$lookup": {
                "from": "devices",
                "localField": "_id.deviceId",
                "foreignField": "_id",
                "as": "device"
            }
        },
        {"$unwind": "$device"},
        {
            "$project": {
                "_id": 0,
                "Device": "$device.name",
                "Metric": "$_id.metric",
                "Average Value": {
                    "$round": ["$avgValue", 2]
                }
            }
        },
        {"$sort": {"Device": 1, "Metric": 1}}
    ]

    return list(db.readings.aggregate(pipeline))



#  Average Readings per Device Type

def avg_readings_per_device_type_aggregation(db):
    pipeline = [
        {
            "$lookup": {
                "from": "devices",
                "localField": "deviceId",
                "foreignField": "_id",
                "as": "device"
            }
        },
        {"$unwind": "$device"},
        {
            "$lookup": {
                "from": "deviceTypes",
                "localField": "device.deviceTypeId",
                "foreignField": "_id",
                "as": "deviceType"
            }
        },
        {"$unwind": "$deviceType"},
        {
            "$project": {
                "deviceType": "$deviceType.name",
                "valuesArray": {"$objectToArray": "$values"}
            }
        },
        {"$unwind": "$valuesArray"},
        {
            "$group": {
                "_id": {
                    "deviceType": "$deviceType",
                    "metric": "$valuesArray.k"
                },
                "avgValue": {"$avg": "$valuesArray.v"}
            }
        },
        {
            "$project": {
                "_id": 0,
                "Device Type": "$_id.deviceType",
                "Metric": "$_id.metric",
                "Average Value": {
                    "$round": ["$avgValue", 2]
                }
            }
        },
        {"$sort": {"Device Type": 1, "Metric": 1}}
    ]

    return list(db.readings.aggregate(pipeline))
