from pydantic import BaseModel, Field
from typing import Optional, List, Tuple, Union, Any, Dict
from uuid import UUID
from datetime import datetime, date
import traceback

class Entity(BaseModel):
    """Entity class definition using Pydantic"""

    id: int = Field(default=0)  # Keep as integer
    uuid: str =  Field(default_factory=str)
    created_by: Optional[str] = Field(default="System")
    updated_by: Optional[str] = Field(default="System")
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

    class Config:
        # Allow arbitrary types, and enable serialization of UUID and datetime
        arbitrary_types_allowed = True
        json_encoders = {
            UUID: str,
            datetime: lambda dt: dt.isoformat(),
        }

    def to_dict(self, skip_none: bool = True) -> dict:
        """Serialize object to dict."""
        return self.dict(exclude_none=skip_none)

    @classmethod
    def from_dict(cls, data: dict) -> 'Entity':
        """Create an instance from a dict."""
        return cls(**data)

    @classmethod
    def from_record(cls, fields: Union[List[Any], Tuple[Any, ...]], record: Tuple[Any, ...]) -> 'Entity':
        """Create an instance from a tuple given by the database driver."""
        try:
            if len(fields) != len(record):
                raise ValueError(f"Expected {len(fields)} fields but got {len(record)}")
            data = {}
            for index, field in enumerate(fields):
                try:
                    value = record[index]
                    # Handle datetime fields
                    if field in ['created_at', 'updated_at', 'deleted_at']:  # Specific check for datetime fields
                        if isinstance(value, str):  # If value is a string, try to convert to datetime
                            try:
                                data[field] = datetime.fromisoformat(value)  # Attempt to convert string to datetime
                            except ValueError:
                                data[field] = None  # If conversion fails, store None
                                continue  # Skip invalid datetime fields
                        elif isinstance(value, datetime):  # If already a datetime, store it
                            data[field] = value
                        else:
                            continue  # Skip if type is not datetime or string
                    if field in ['created_by', 'updated_by']:
                        data[field] = value

                    # Handle specific types like datetime, UUID, or bytes
                    if isinstance(value, datetime) or isinstance(value, date):
                        data[field] = value  # Store datetime directly
                    elif isinstance(value, (UUID, bytes)):
                        data[field] = str(value)
                    elif isinstance(value, str) or isinstance(value, int) or isinstance(value, float):
                        data[field] = value
                    elif isinstance(value, List):
                        if value is None or len(value) == 0:  # Skip None values
                            print(f"[WARNING] None value for field '{field}', skipping it.")
                            data[field] = []
                            continue
                        data[field] = [v for v in value if isinstance(v, Dict) or isinstance(v, int)]  # Ensure it's a list of dicts
                    else:
                        print(f"[WARNING] Invalid type for field '{field}', skipping it.") #TODO
                        print(f" Type of value: {type(value)}")
                        continue
                except Exception as field_error:
                    traceback.print_exc()
                    # Log field-specific errors but continue
                    print(f"[WARNING] Skipping field '{field}' due to error: {field_error}")
                    continue

            return cls(**data)
        except Exception as e:
            traceback.print_exc()
            return {}
        


    def __str__(self) -> str:
        """String conversion definition."""
        return str(self.to_dict(skip_none=False))

    def __repr__(self) -> str:
        """Entity representation."""
        return f"{self.__class__.__name__}({self.to_dict(skip_none=False)})"

class Command(BaseModel):
    """Entity class definition using Pydantic"""

    created_by: Optional[str] = "01-01-2021"
    updated_by: Optional[str] = "01-01-2021"
    created_at: Optional[datetime] = "01-01-2021"
    updated_at: Optional[datetime] = "01-01-2021"

    class Config:
        # Allow arbitrary types, and enable serialization of UUID and datetime
        arbitrary_types_allowed = True
        json_encoders = {
            UUID: str,
            datetime: lambda dt: dt.isoformat(),
        }

    def to_dict(self, skip_none: bool = True) -> dict:
        """Serialize object to dict."""
        return self.dict(exclude_none=skip_none)

    def __str__(self) -> str:
        """String conversion definition."""
        return str(self.to_dict(skip_none=False))

    def __repr__(self) -> str:
        """Entity representation."""
        return f"{self.__class__.__name__}({self.to_dict(skip_none=False)})"