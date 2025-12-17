from bson import ObjectId
from datetime import datetime, timezone


def create_location(db, company_id, street, building, floor, city):
    location = {
        "companyId": ObjectId(company_id),
        "address": {
            "street": street,
            "building": building,
            "floor": floor,
            "city": city
        },
        "createdAt": datetime.now(timezone.utc)
    }
    result = db.locations.insert_one(location)
    print(f"Inserted location with _id: {result.inserted_id}")
    return result.inserted_id


def read_locations(db, filter={}):
    return list(db.locations.find(filter))


def update_location(db, location_id, update_fields):
    result = db.locations.update_one(
        {"_id": ObjectId(location_id)},
        {"$set": update_fields}
    )
    print(f"Matched {result.matched_count}, Modified {result.modified_count}")


def delete_location(db, location_id):
    result = db.locations.delete_one(
        {"_id": ObjectId(location_id)}
    )
    print(f"Deleted {result.deleted_count} location")
