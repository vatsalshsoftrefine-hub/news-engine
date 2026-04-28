def success_response(data=None, message="Success"):
    """
    Standard success response
    """
    return {
        "status": "success",
        "message": message,
        "data": data
    }


def error_response(message="Something went wrong"):
    """
    Standard error response
    """
    return {
        "status": "error",
        "message": message
    }