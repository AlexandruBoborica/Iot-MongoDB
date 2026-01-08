def create_indexes(db):
    print("Creating indexes...")

 
    db.devices.create_index("companyId")
    db.devices.create_index("locationId")
    db.devices.create_index("deviceTypeId")

    # Readings collection
    db.readings.create_index("deviceId")
    db.readings.create_index("timestamp")
    db.readings.create_index(
        [("deviceId", 1), ("timestamp", -1)]
    )

  
    db.locations.create_index("companyId")

    print("Indexes created successfully")
