from pathlib import Path
from typing import Self, TypedDict, Unpack, override

import anyio
import asyncer
from azure.storage.blob.aio import BlobServiceClient, ContainerClient
from azure.storage.blob.aio._blob_client_async import BlobClient

from azhacks.storage_resource_manager import StorageResourceManager


class ServiceKwargs(TypedDict, total=False):
    secondary_hostname: str
    max_block_size: int
    max_single_put_size: int
    min_large_block_upload_threshold: int
    use_byte_buffer: bool
    max_page_size: int
    max_single_get_size: int
    max_chunk_get_size: int
    audience: str


class ContainerManager(StorageResourceManager):
    """Class to manage retrieving blob data from a given blob file.

    :param container: The name of the container.
    :param account: The name of the Azure Storage account.
    :param api_key: The API key for the Azure Storage account.
    """

    def __init__(
        self,
        container: str,
        account: str,
        api_key: str,
        **kwargs: Unpack[ServiceKwargs],
    ) -> None:
        self.container = container
        super().__init__(account, api_key)
        self.kwargs = kwargs
        self._service_client_cache: BlobServiceClient | None = None
        self._client_cache: ContainerClient | None = None

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
        return self._get_endpoint("blob")

    def _get_service_client(self) -> BlobServiceClient:
        if not self._service_client_cache:
            self._service_client_cache = BlobServiceClient(
                self.get_endpoint(), credential=self.api_key, **self.kwargs
            )
        return self._service_client_cache

    def _get_client(self) -> ContainerClient:
        if not self._client_cache:
            service_client = self._get_service_client()
            self._client_cache = service_client.get_container_client(self.container)
        return self._client_cache

    async def download(self, blob_path: Path) -> bytes:
        """Retrieve data from a given blob file within the container.

        :param blob_path: The path of the blob file.
        :param use_chunks: Whether to use chunking to download the blob.
        :return: The content of the blob.
        """
        downloader = await self._get_client().download_blob(
            str(blob_path), encoding=None
        )
        return await downloader.readall()  # NOTE: to decode bytes.decode(encoding)

    async def download_to_file(self, blob_path: Path, filepath: Path) -> None:
        """Download a blob from the container to a file."""
        async with await anyio.open_file(filepath, mode="wb") as f:
            await f.write(await self.download(blob_path))

    async def upload(self, filepath: Path, blob_path: Path | None = None) -> BlobClient:
        """Upload a file to a blob.

        :param filepath: The path to the file to upload.
        :param blob_path: The path in the blob storage to upload to.
        :return: The BlobClient for the uploaded blob.
        """
        async with await anyio.open_file(filepath, mode="rb") as f:
            blob_name = str(blob_path or filepath)
            return await self._get_client().upload_blob(blob_name, f)

    async def sync_blobs(
        self, filepaths: list[Path], blob_paths: list[Path] | None = None
    ) -> list[BlobClient]:
        """Upload files only if they don't already exist in the blob storage.

        :param filepaths: The paths to the files to upload.
        :param blob_paths: The paths in the blob storage to upload to.
        :return: The BlobClients for the uploaded blobs.
        """
        soon_values: list[asyncer.SoonValue[BlobClient]] = []
        async with asyncer.create_task_group() as tg:
            for i, pth in enumerate(filepaths):
                blb = blob_paths[i] if blob_paths else pth
                blob_client = self._get_client().get_blob_client(blb.as_posix())
                if not await blob_client.exists():
                    soon_values.append(tg.soonify(self.upload)(pth, blb))
        return [sv.value for sv in soon_values]

    async def sync_with_folder(
        self, folder: Path, pattern: str = "**/*"
    ) -> list[BlobClient]:
        """Sync a folder with the blob storage container."""
        existing_blobs = {
            blb.name async for blb in self._get_client().list_blobs(folder.name + "/")
        }
        tasks: list[asyncer.SoonValue[BlobClient]] = []
        async with asyncer.create_task_group() as tg:
            for pth in folder.glob(pattern):
                if pth.is_file():
                    blb_path = pth.relative_to(folder.parent)
                    if str(blb_path) not in existing_blobs:
                        tasks.append(tg.soonify(self.upload)(pth, blb_path))
        return [t.value for t in tasks]
