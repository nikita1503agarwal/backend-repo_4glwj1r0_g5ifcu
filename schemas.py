"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field
from typing import Optional, List

# Real estate specific schemas

class Property(BaseModel):
    """
    Property listings schema
    Collection name: "property"
    """
    title: str = Field(..., description="Headline/title for the property")
    address: str = Field(..., description="Street address")
    city: str = Field(..., description="City")
    state: str = Field(..., description="State abbreviation")
    zip_code: str = Field(..., description="Zip/Postal code")
    price: int = Field(..., ge=0, description="Listing price in USD")
    beds: int = Field(..., ge=0, description="Bedrooms")
    baths: float = Field(..., ge=0, description="Bathrooms")
    sqft: Optional[int] = Field(None, ge=0, description="Square footage")
    lot_size: Optional[float] = Field(None, ge=0, description="Lot size (acres)")
    year_built: Optional[int] = Field(None, description="Year built")
    description: Optional[str] = Field(None, description="Long description")
    features: Optional[List[str]] = Field(default_factory=list, description="Key features")
    images: Optional[List[str]] = Field(default_factory=list, description="Image URLs")
    status: str = Field("For Sale", description="Status: For Sale, Sold, Pending, Off Market")
    type: str = Field("Single Family", description="Property type")

class Inquiry(BaseModel):
    """
    Buyer/seller inquiry submissions
    Collection name: "inquiry"
    """
    name: str = Field(..., description="Full name")
    email: str = Field(..., description="Email address")
    phone: Optional[str] = Field(None, description="Phone number")
    message: str = Field(..., description="Message from lead")
    property_id: Optional[str] = Field(None, description="Related property id if applicable")

# Example schemas (kept for reference of structure)
class User(BaseModel):
    name: str
    email: str
    address: str
    is_active: bool = True

class Product(BaseModel):
    title: str
    description: Optional[str] = None
    price: float
    category: str
    in_stock: bool = True
