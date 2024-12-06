import re
from abc import ABC, abstractmethod
from typing import Literal, Self

from azure.core.credentials import AzureNamedKeyCredential


class StorageResourceManager(ABC):
    """Abstract class for managing storage resources in Azure Storage.

    :param account: The name of the Azure Storage account.
    :param api_key: The API key for the Azure Storage account.
    """

    class InvalidConnectionStringError(ValueError):
        """Exception raised when an Azure Storage connection string is invalid."""

        def __init__(self, connection_string: str) -> None:
            """Initialize the InvalidConnectionStringError class."""
            self.connection_string = connection_string
            super().__init__(
                f"Invalid Azure Storage connection string: {connection_string}"
            )

    def __init__(self, account: str, api_key: str) -> None:
        """Initialize the StorageResourceManager class."""
        self.account = account
        self.api_key = api_key

    @abstractmethod
    async def __aenter__(self) -> Self:
        pass

    @abstractmethod
    async def __aexit__(self, *args: object) -> None:
        pass

    def get_creds(self) -> AzureNamedKeyCredential:
        """Return the credentials for the storage resource."""
        return AzureNamedKeyCredential(self.account, self.api_key)

    def _get_endpoint(self, resource_type: Literal["blob", "queue", "table"]) -> str:
        """Return the endpoint URL for the storage resource."""
        return f"https://{self.account}.{resource_type}.core.windows.net"

    @abstractmethod
    def get_endpoint(self) -> str:
        """Return the endpoint URL for the storage resource."""

    @classmethod
    def from_connection_string(cls, connection_string: str) -> Self:
        """Create a new instance from an Azure Storage connection string.

        :param connection_string: The Azure Storage connection string.
        :return: A new instance of the AzureNamedKeyCredential class.
        :raise InvalidConnectionStringError: If the connection string is invalid.
        """
        pattern = r"DefaultEndpointsProtocol=(.*);AccountName=(.*);AccountKey=(.*);"
        match = re.match(pattern, connection_string)
        if not match:
            raise cls.InvalidConnectionStringError(connection_string)
        _, account, key = match.groups()
        return cls(account, key)
