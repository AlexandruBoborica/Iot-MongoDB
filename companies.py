from pymongo import MongoClient
import datetime
from bson import ObjectId
import string


def create_company(db  : MongoClient, name : string , industry : string):
    company_to_be_added = {
        "name": name,
        "industry" : industry,
        "createdAt" : datetime.datetime.now(datetime.timezone.utc)
    }

    result = db.companies.insert_one(company_to_be_added)
    return result.inserted_id


def read_companies(db, filter={}):
    companies = list(db.companies.find(filter))
    return companies

def update_company(db, company_id, update_fields):
    result = db.companies.update_one(
        {"_id": ObjectId(company_id)},
        {"$set": update_fields}
    )
    print(f"Matched {result.matched_count}, Modified {result.modified_count}")

def delete_company(db, company_id):
    result = db.companies.delete_one({"_id": ObjectId(company_id)})
    print(f"Deleted {result.deleted_count} company(s)")