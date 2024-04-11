from fastapi import FastAPI, HTTPException, Query
from pymongo import MongoClient
from typing import List
from fastapi import Query

app = FastAPI()

# connection to MongoDB atlas
client = MongoClient("mongodb+srv://synisoft:s6492628827@cluster0.flvotav.mongodb.net/")
db = client["address_book"]
addresses_collection = db["addresses"]


@app.post("/addresses/")
async def create_address(latitude: float, longitude: float, address: str):
    """
    Create a new address with coordinates and save it to MongoDB.
    """
    # Validation can be added here if needed
    new_address = {"latitude": latitude, "longitude": longitude, "address": address}
    result = addresses_collection.insert_one(new_address)
    return {"id": str(result.inserted_id), **new_address}


@app.put("/addresses/{address_id}")
async def update_address(address_id: str, latitude: float, longitude: float, address: str):
    """
    Update an existing address by ID.
    """
    # Validation can be added here if needed
    updated_address = {"latitude": latitude, "longitude": longitude, "address": address}
    result = addresses_collection.update_one({"_id": address_id}, {"$set": updated_address})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Address not found")
    return {"message": "Address updated successfully"}


@app.delete("/addresses/{address_id}")
async def delete_address(address_id: str):
    """
    Delete an address by ID.
    """
    result = addresses_collection.delete_one({"_id": address_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Address not found")
    return {"message": "Address deleted successfully"}




@app.get("/addresses/within_radius")
async def get_addresses_within_radius(latitude: float = Query(..., description="Latitude of location"),
                                      longitude: float = Query(..., description="Longitude of location"),
                                      radius: float = Query(..., description="Radius in meters")):
    """
    Get addresses within a given radius of a location.
    """
    # Implement geospatial query to find addresses within the specified radius
    # Use MongoDB's geospatial query operators to perform the search
    
    # Ex: Find addresses within radius using $near query
    addresses = addresses_collection.find({
        "location": {
            "$near": {
                "$geometry": {
                    "type": "Point",
                    "coordinates": [longitude, latitude]  # Note the order: [longitude, latitude]
                },
                "$maxDistance": radius
            }
        }
    })
    
    return list(addresses)


    # uvicorn main:app --reload (to run)
    # url/docs (FastAPI’s Swagger Doc - CURD)
    # the data will be saved in mongoDB atlas
    # the file name must be main.py

    
    #library used -  
    # FASTAPIs with Python 3.7+,
    # Pymango to interact with MongoDB databases, 
    # typing to implementation to specify function parameter and return types.

