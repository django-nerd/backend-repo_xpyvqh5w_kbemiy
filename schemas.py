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

from pydantic import BaseModel, Field, EmailStr
from typing import Optional, Literal

# Example schemas (retain for reference)
class User(BaseModel):
    name: str = Field(..., description="Full name")
    email: EmailStr = Field(..., description="Email address")
    address: str = Field(..., description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")

class Product(BaseModel):
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in GBP")
    category: str = Field(..., description="Product category")
    in_stock: bool = Field(True, description="Whether product is in stock")

# Verdure-specific schemas used by the app
class TradeAccount(BaseModel):
    company_name: str = Field(..., description="Company legal name")
    contact_name: str = Field(..., description="Primary contact name")
    email: EmailStr = Field(..., description="Work email")
    phone: str = Field(..., description="Work phone number")
    company_size: Optional[Literal["1-5","6-20","21-50","51-200","200+"]] = Field(None, description="Company size bracket")
    monthly_volume_estimate_l: Optional[int] = Field(None, ge=0, description="Estimated monthly usage in litres")
    address: Optional[str] = Field(None, description="Business address")
    notes: Optional[str] = Field(None, description="Any additional information")

class QuoteRequest(BaseModel):
    company_name: str = Field(..., description="Company name")
    contact_name: str = Field(..., description="Contact person")
    email: EmailStr = Field(..., description="Email for the quote")
    phone: Optional[str] = Field(None, description="Phone number")
    quantity_bottles: int = Field(..., ge=1, description="Number of bottles requested")
    delivery_postcode: Optional[str] = Field(None, description="Delivery postcode")
    need_by_days: Optional[int] = Field(None, ge=0, description="When the product is needed (days)")
    notes: Optional[str] = Field(None, description="Project details or notes")
