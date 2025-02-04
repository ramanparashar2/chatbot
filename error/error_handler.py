import logging
import requests
from fastapi import HTTPException
from fastapi.responses import JSONResponse

from error.exceptions import NotFoundError, BadRequestError, UnauthorizedError, InternalServerError


# Slack webhook URL (replace with your own)
SLACK_WEBHOOK_URL = "your-slack-webhook-url"

class ErrorHandler:
    @staticmethod
    def log_and_notify(e: Exception):
        # Log the error to a file
        # logging.error(f"An error occurred: {str(e)}")

        # Send the error to Slack
        # ErrorHandler.notify_slack(str(e))
        pass

    @staticmethod
    def notify_slack(message: str):
        """Send error details to Slack."""
        # payload = {
        #     "text": f"Error Occurred: {message}"
        # }
        # requests.post(SLACK_WEBHOOK_URL, json=payload)
        pass

    @staticmethod
    def handle_exception(e: Exception):
        """Handles the exception by categorizing and responding appropriately."""
        # Log and notify about the exception
        ErrorHandler.log_and_notify(e)

        # Handle known exceptions (custom logic can go here)
        if isinstance(e, NotFoundError):
            raise HTTPException(status_code=404, detail={"message": "Not Found", "error": str(e), "status_code": 404})
        elif isinstance(e, BadRequestError):
            raise HTTPException(status_code=400, detail={"message": "Bad Request", "error": str(e), "status_code": 400})
        elif isinstance(e, UnauthorizedError):
            raise HTTPException(status_code=401, detail={"message": "Unauthorized", "error": str(e), "status_code": 401})
        else:
            raise HTTPException(status_code=500, detail={"message": "Internal Server Error", "error": str(e), "status_code": 500})
