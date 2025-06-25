import uuid
from datetime import datetime, timezone
from typing import Optional

from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database

from src.models import Request

from ..exceptions import RequestRepositoryError
from ..request_repository import RequestRepository


class MongoDBRequestRepository(RequestRepository):
    """
    MongoDB implementation of the RequestRepository interface.
    """

    def __init__(self, connection_string: str, database_name: str = "email_classification"):
        """
        Initialize the repository with MongoDB connection.

        Args:
            connection_string: MongoDB connection string
            database_name: Name of the database to use
        """
        try:
            self.client = MongoClient(connection_string)
            self.database: Database = self.client[database_name]
            self.collection: Collection = self.database["requests"]
        except Exception as e:
            raise RequestRepositoryError(
                f"Failed to connect to MongoDB: {str(e)}", RequestRepositoryError.CONNECTION_ERROR, {"connection_string": connection_string, "database_name": database_name}
            ) from e

    async def create(self, request: Request) -> Request:
        """
        Create a new request record.

        Args:
            request: Request entity to create

        Returns:
            Request: The created request entity

        Raises:
            RequestRepositoryError: When database operation fails
        """
        try:
            # Convert entity to dictionary for storage
            request_data = request.to_dict()

            # Add metadata if not present
            if not request_data.get("id"):
                request_data["id"] = str(uuid.uuid4())
                request.id = request_data["id"]

            if not request_data.get("created_at"):
                request_data["created_at"] = datetime.now(timezone.utc)
                request.created_at = request_data["created_at"]

            if not request_data.get("updated_at"):
                request_data["updated_at"] = datetime.now(timezone.utc)
                request.updated_at = request_data["updated_at"]

            # Insert into database
            result = self.collection.insert_one(request_data)

            if result.inserted_id:
                return request
            else:
                raise RequestRepositoryError("Failed to create request", RequestRepositoryError.CREATE_ERROR)

        except RequestRepositoryError:
            raise
        except Exception as e:
            raise RequestRepositoryError(f"Error creating request: {str(e)}", RequestRepositoryError.CREATE_ERROR, {"original_error": str(e)}) from e

    async def get_by_id(self, request_id: str) -> Optional[Request]:
        """
        Retrieve a request by its ID.

        Args:
            request_id: The ID of the request to retrieve

        Returns:
            Request | None: The request entity or None if not found

        Raises:
            RequestRepositoryError: When database operation fails
        """
        try:
            request_data = self.collection.find_one({"id": request_id})
            if request_data:
                return Request.from_dict(request_data)
            return None
        except Exception as e:
            raise RequestRepositoryError(f"Error retrieving request {request_id}: {str(e)}", RequestRepositoryError.READ_ERROR, {"request_id": request_id, "original_error": str(e)}) from e

    async def update(self, request: Request) -> bool:
        """
        Update an existing request.

        Args:
            request: Request entity to update

        Returns:
            bool: True if update was successful, False otherwise

        Raises:
            RequestRepositoryError: When database operation fails
        """
        try:
            # Update the timestamp
            request.updated_at = datetime.now(timezone.utc)

            # Convert entity to dictionary for storage
            update_data = request.to_dict()

            result = self.collection.update_one({"id": request.id}, {"$set": update_data})

            return result.modified_count > 0
        except Exception as e:
            raise RequestRepositoryError(f"Error updating request {request.id}: {str(e)}", RequestRepositoryError.UPDATE_ERROR, {"request_id": request.id, "original_error": str(e)}) from e

    async def exists(self, request_id: str) -> bool:
        """
        Check if a request exists.

        Args:
            request_id: The ID of the request to check

        Returns:
            bool: True if request exists, False otherwise

        Raises:
            RequestRepositoryError: When database operation fails
        """
        try:
            count = self.collection.count_documents({"id": request_id})
            return count > 0
        except Exception as e:
            raise RequestRepositoryError(f"Error checking if request {request_id} exists: {str(e)}", RequestRepositoryError.READ_ERROR, {"request_id": request_id, "original_error": str(e)}) from e

    def close(self):
        """
        Close the database connection.
        """
        if self.client:
            self.client.close()
