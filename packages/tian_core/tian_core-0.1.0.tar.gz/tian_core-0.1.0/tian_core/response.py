import json
from typing import Any, Dict
import datetime

from decimal import Decimal
from datetime import datetime

def serialize_list(data):

    serialized_data = []

    for item in data:
        if isinstance(item, dict):
            serialized_data.append(item)  # Dictionaries are already serializable
        elif isinstance(item, (list, tuple)):
            # Recursively serialize nested lists or tuples
            serialized_data.append(serialize_list(item))
        else:
            try:
                # Attempt to convert to dict if it's an object
                serialized_data.append(item.to_dict())
            except AttributeError:
                # Handle non-serializable elements
                serialized_data.append(str(item))

    return serialized_data


def custom_serializer(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    if isinstance(obj, datetime):
        return obj.isoformat()  # Convert datetime to ISO 8601 format string
    raise TypeError(f"Type {type(obj).__name__} not serializable")
    
def message_response(status: str, message: str = None, data: Any = None) -> Dict[str, Any]:
    """Construct a response dictionary with status, message, and data.

    :param status: Status of the response
    :param message: Optional message to include in the response
    :param data: Optional data to include in the response
    :return: A dictionary with 'status', 'message', and 'result' keys
    """
    
    #
    if data is None:
       return {
            "status": status, 
            "message": message, 
            "result": "No thing here!"
        }

    if isinstance(data, dict):
        return {
            "status": status, 
            "message": message, 
            "result": json.loads(json.dumps(data, default=custom_serializer)) #TODO
        }

    # TODO: Implement a better way to serialize data
    data_serializable = []
    for item in data:
        if isinstance(item, dict):
            data_serializable.append(item)
        else:
            try:
                # Attempt to convert to dict if it's an object
                data_serializable.append(item.to_dict())
            except AttributeError:
                # Handle any non-dict, non-object elements
                data_serializable.append(str(item))
    return {
        "status": status, 
        "message": message, 
        "result": serialize_list(data)
    }



def validation_error(status, errors):
    response_object = {"status": status, "errors": errors}

    return response_object


def err_resp(msg, reason, code):
    err = message_response(False, msg)
    err["error_reason"] = reason
    return err, code


def internal_err_resp():
    err = message_response(False, "Something went wrong during the process!")
    err["error_reason"] = "server_error"
    return err, 500