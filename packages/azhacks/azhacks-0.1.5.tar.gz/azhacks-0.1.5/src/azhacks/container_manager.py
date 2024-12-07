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
        self, folder: Path, blob_folder: Path | None = None, pattern: str = "**/*"
    ) -> list[BlobClient]:
        """Sync a folder with a blob storage container folder.

        :param folder: The folder to sync with the blob storage container.
        :param blob_folder: The folder in the blob storage to sync with.
        If not provided, the files will be synced to the root of the container.
        :param pattern: The pattern to match files in the folder.
        """
        blob_folder = blob_folder or Path()
        client = self._get_client()
        blob_prefix = blob_folder.name + "/" if str(blob_folder) else ""
        existing_blobs = {blb.name async for blb in client.list_blobs(blob_prefix)}
        tasks: list[asyncer.SoonValue[BlobClient]] = []
        async with asyncer.create_task_group() as tg:
            for pth in folder.glob(pattern):
                blob_path = blob_folder / pth.relative_to(folder)
                if pth.is_file() and blob_path not in existing_blobs:
                    tasks.append(tg.soonify(self.upload)(pth, blob_path))
        return [t.value for t in tasks]

    async def download_bytes(self, blob_path: Path) -> bytes:
        """Retrieve data from a given blob file within the container."""
        client = self._get_client()
        downloader = await client.download_blob(str(blob_path), encoding=None)
        return await downloader.readall()  # NOTE: to decode bytes.decode(encoding)

    async def download(self, blob_path: Path, save_path: Path | None = None) -> None:
        """Download a blob from the container to a file."""
        save_path = save_path or Path.cwd() / blob_path
        async with await anyio.open_file(save_path, mode="wb") as f:
            await f.write(await self.download_bytes(blob_path))

    async def download_folder(
        self, blob_folder: Path, save_folder: Path | None = None
    ) -> None:
        """Download all blobs in a folder from the container to a local folder.

        :param blob_folder: The folder in the blob storage to download from.
        If not provided, all blobs in the container will be downloaded.
        :param save_folder: The folder to save the downloaded blobs to.
        If not provided, the blobs will be downloaded to the current working
        directory.
        """
        blob_prefix = blob_folder.name + "/" if blob_folder else ""
        save_folder = save_folder or Path.cwd()
        async with asyncer.create_task_group() as tg:
            async for blob in self._get_client().list_blobs(blob_prefix):
                filepath = save_folder / blob.name
                await anyio.Path(filepath.parent).mkdir(parents=True, exist_ok=True)
                tg.soonify(self.download)(Path(blob.name), filepath)

    async def download_all(self, save_folder: Path) -> None:
        """Download all blobs in the container to a local folder."""
        await self.download_folder(Path(), save_folder)
