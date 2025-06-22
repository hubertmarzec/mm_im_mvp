import uuid
from datetime import datetime, timezone
from typing import Any

from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database

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

    async def create(self, request_data: dict[str, Any]) -> str:
        """
        Create a new request record.

        Args:
            request_data: Dictionary containing request data

        Returns:
            str: The ID of the created request

        Raises:
            RequestRepositoryError: When database operation fails
        """
        try:
            # Add metadata
            request_data["id"] = str(uuid.uuid4())
            request_data["created_at"] = datetime.now(timezone.utc)
            request_data["updated_at"] = datetime.now(timezone.utc)
            request_data["status"] = request_data.get("status", "pending")

            # Insert into database
            result = self.collection.insert_one(request_data)

            if result.inserted_id:
                return request_data["id"]
            else:
                raise RequestRepositoryError("Failed to create request", RequestRepositoryError.CREATE_ERROR)

        except RequestRepositoryError:
            raise
        except Exception as e:
            raise RequestRepositoryError(f"Error creating request: {str(e)}", RequestRepositoryError.CREATE_ERROR, {"original_error": str(e)}) from e

    async def get_by_id(self, request_id: str) -> dict[str, Any] | None:
        """
        Retrieve a request by its ID.

        Args:
            request_id: The ID of the request to retrieve

        Returns:
            dict[str, Any] | None: The request data or None if not found

        Raises:
            RequestRepositoryError: When database operation fails
        """
        try:
            request = self.collection.find_one({"id": request_id})
            return request
        except Exception as e:
            raise RequestRepositoryError(f"Error retrieving request {request_id}: {str(e)}", RequestRepositoryError.READ_ERROR, {"request_id": request_id, "original_error": str(e)}) from e

    async def update(self, request_id: str, update_data: dict[str, Any]) -> bool:
        """
        Update an existing request.

        Args:
            request_id: The ID of the request to update
            update_data: Dictionary containing fields to update

        Returns:
            bool: True if update was successful, False otherwise

        Raises:
            RequestRepositoryError: When database operation fails
        """
        try:
            # Add updated timestamp
            update_data["updated_at"] = datetime.now(timezone.utc)

            result = self.collection.update_one({"id": request_id}, {"$set": update_data})

            return result.modified_count > 0
        except Exception as e:
            raise RequestRepositoryError(f"Error updating request {request_id}: {str(e)}", RequestRepositoryError.UPDATE_ERROR, {"request_id": request_id, "original_error": str(e)}) from e

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
