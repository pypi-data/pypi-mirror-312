from typing import Self, override

import asyncer
from azure.storage.queue.aio import QueueClient, QueueServiceClient

from azaux.storage_resource_manager import StorageResourceManager


class QueueManager(StorageResourceManager):
    """Class to manage sending messages to a given queue from the Queue Storage account.

    :param queue: The name of the queue.
    :param account: The name of the Azure Storage account.
    :param api_key: The API key for the Azure Storage account.
    """

    def __init__(self, queue: str, account: str, api_key: str) -> None:
        self.queue = queue
        super().__init__(account, api_key)
        self._service_client_cache: QueueServiceClient | None = None
        self._client_cache: QueueClient | None = None

    @override
    async def __aenter__(self) -> Self:
        await self._get_service_client().__aenter__()
        return self

    @override
    async def __aexit__(self, *args: object) -> None:
        await self._get_service_client().__aexit__(*args)
        self._service_client_cache = None
        self._client_cache = None

    @override
    def get_endpoint(self) -> str:
        return self._get_endpoint("queue")

    def _get_service_client(self) -> QueueServiceClient:
        if not self._service_client_cache:
            self._service_client_cache = QueueServiceClient(
                self.get_endpoint(), credential=self.api_key
            )
        return self._service_client_cache

    def _get_client(self) -> QueueClient:
        if not self._client_cache:
            self._client_cache = self._get_service_client().get_queue_client(self.queue)
        return self._client_cache

    async def send_messages(self, instance_inputs: list[str]) -> None:
        """Send messages to the queue.

        :param instance_inputs: The list of messages to send to the queue.
        """
        async with asyncer.create_task_group() as tg:
            for input_msg in instance_inputs:
                tg.soonify(self._get_client().send_message)(input_msg)
