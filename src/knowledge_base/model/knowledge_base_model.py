from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class ContentCollectorModel(BaseModel):
    firstName: str
    middleName: Optional[str] = None
    lastName: Optional[str] = None
    email: str
    profileImage: Optional[str] = None
    password: str
    isActive: Optional[bool] = False
    lastActive: Optional[datetime] = None
    primaryPhone: Optional[str] = None
    alternatePhone: Optional[str] = None
    createdAt: datetime = datetime.utcnow()
    updatedAt: datetime = datetime.utcnow()

    class Config:
        title = "User Model"
        description = "A schema representing a user in the system."
        json_schema_extra  = {
            "example": {
                "firstName": "John",
                "middleName": "M.",
                "lastName": "Doe",
                "email": "john.doe@example.com",
                "profileImage": "https://example.com/john.jpg",
                "password": "strongpassword123",
                "isActive": True,
                "lastActive": "2025-01-15T08:00:00Z",
                "primaryPhone": "+1234567890",
                "alternatePhone": "+0987654321",
                "createdAt": "2025-01-10T10:00:00Z",
                "updatedAt": "2025-01-16T12:00:00Z"
            }
        }
