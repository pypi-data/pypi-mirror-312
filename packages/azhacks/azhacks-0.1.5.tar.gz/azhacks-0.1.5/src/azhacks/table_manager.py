from typing import Self, override

from azure.data.tables import TableEntity
from azure.data.tables.aio import TableClient, TableServiceClient

from azhacks.storage_resource_manager import StorageResourceManager


class TableManager(StorageResourceManager):
    """Class to manage table entities from a given table from the Table Storage."""

    def __init__(
        self,
        table: str,
        account: str,
        api_key: str,
    ) -> None:
        self.table = table
        super().__init__(account, api_key)
        self._service_client_cache: TableServiceClient | None = None
        self._client_cache: TableClient | None = None

    @override
    async def __aenter__(self) -> Self:
        await self._get_service_client().__aenter__()
        return self

    @override
    async def __aexit__(self, *args: object) -> None:
        await self._get_service_client().__aexit__(*args)
        self._service_client_cache = None
        self._client_cache = None

    def _get_service_client(self) -> TableServiceClient:
        if not self._service_client_cache:
            self._service_client_cache = TableServiceClient(
                self.get_endpoint(), credential=self.get_creds()
            )
        return self._service_client_cache

    def _get_client(self) -> TableClient:
        if not self._client_cache:
            self._client_cache = self._get_service_client().get_table_client(self.table)
        return self._client_cache

    @override
    def get_endpoint(self) -> str:
        return self._get_endpoint("table")

    async def upsert_entity(self, entity_data: dict) -> None:
        """Upload a table entity to the table storage account.

        :param entity_data: The data to be uploaded as a table entity.
        """
        await self._get_client().upsert_entity(entity=entity_data)

    async def retrieve_table_entities(self, query: str) -> list[TableEntity]:
        """Retrieve table entities from the table storage account.

        :param query: The query string to filter the table entities.
        """
        client = self._get_client()
        return [ent async for ent in client.query_entities(query_filter=str(query))]

    async def remove_table_entity(self, entity: TableEntity) -> None:
        """Remove a table entity from the table storage account.

        :param entity: The table entity to be removed.
        """
        await self._get_client().delete_entity(
            partition_key=entity["PartitionKey"], row_key=entity["RowKey"]
        )
