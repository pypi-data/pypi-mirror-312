"""Implementation of the client logic."""

import os
from types import TracebackType
from typing import Any, Generator

from httpx import AsyncClient, Auth, Client, Request, Response

from whyhow.resources import (
    AsyncChunksResource,
    AsyncDocumentsResource,
    AsyncGraphsResource,
    AsyncNodesResource,
    AsyncSchemasResource,
    AsyncTriplesResource,
    AsyncWorkspacesResource,
    ChunksResource,
    DocumentsResource,
    GraphsResource,
    NodesResource,
    SchemasResource,
    TriplesResource,
    WorkspacesResource,
)

from .utils import _create_graph_from_knowledge_table, _export_all_data

BASE_URL = "https://api.whyhow.ai"


class _APIKeyAuth(Auth):
    """Auth class for the API key."""

    def __init__(
        self,
        api_key: str,
    ) -> None:
        """Initialize the auth object."""
        self.api_key = api_key

    def auth_flow(
        self, request: Request
    ) -> Generator[Request, Response, None]:
        """Add the API key to the request."""
        request.headers["x-api-key"] = self.api_key

        yield request


class WhyHow:
    """
    Synchronous client for the WhyHow API.

    Parameters
    ----------
    api_key : str, optional
        The API key to use for authentication. If not provided, the
        WHYHOW_API_KEY environment variable will be used.

    base_url : str, optional
        The base URL for the API.

    httpx_kwargs : dict, optional
        Additional keyword arguments to pass to the httpx client.

    Attributes
    ----------
    httpx_client : httpx.Client
        A synchronous httpx client.
    """

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str | None = None,
        httpx_kwargs: dict[str, Any] | None = None,
    ) -> None:
        """Initialize the client."""
        if base_url is None:
            base_url = BASE_URL

        base_url = base_url.rstrip("/")

        if httpx_kwargs is None:
            httpx_kwargs = {}

        if api_key is None:
            api_key = os.environ.get("WHYHOW_API_KEY")

            if api_key is None:
                raise ValueError("WHYHOW_API_KEY must be set.")

        auth = _APIKeyAuth(
            api_key=api_key,
        )

        if "base_url" in httpx_kwargs:
            raise ValueError("base_url cannot be set in httpx_kwargs.")

        httpx_kwargs["timeout"] = httpx_kwargs.get("timeout", 30)

        self.httpx_client = Client(  # nosec B113
            base_url=base_url,
            auth=auth,
            **httpx_kwargs,
        )

        self.chunks = ChunksResource(client=self.httpx_client)
        self.documents = DocumentsResource(client=self.httpx_client)
        self.graphs = GraphsResource(client=self.httpx_client)
        self.schemas = SchemasResource(client=self.httpx_client)
        self.workspaces = WorkspacesResource(client=self.httpx_client)
        self.nodes = NodesResource(client=self.httpx_client)
        self.triples = TriplesResource(client=self.httpx_client)

    def close(self) -> None:
        """Close the client."""
        self.httpx_client.close()

    def __enter__(self) -> "WhyHow":
        """Enter the context manager."""
        self.httpx_client.__enter__()
        return self

    def create_graph_from_knowledge_table(
        self, file_path: str, workspace_name: str, graph_name: str
    ) -> str:
        """
        Create a graph from a knowledge table file.

        Parameters
        ----------
        file_path : str
            Path to the knowledge table file.
        workspace_name : str
            Name of the workspace to use or create.
        graph_name : str
            Name for the graph to be created.

        Returns
        -------
        str
            The ID of the created graph.
        """
        return _create_graph_from_knowledge_table(
            self, file_path, workspace_name, graph_name
        )

    def export_all(self, workspace_id: str | None = None) -> str:
        """
        Output all of your WhyHow data to a JSON file.

        Returns
        -------
        str
            Success or failure message.
        """
        return _export_all_data(self, workspace_id)

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        """Exit the context manager."""
        self.httpx_client.__exit__(exc_type, exc_value, traceback)


class AsyncWhyHow:
    """
    Asynchronous client for the WhyHow API.

    Parameters
    ----------
    api_key : str, optional
        The API key to use for authentication. If not provided, the
        WHYHOW_API_KEY environment variable will be used.

    base_url : str, optional
        The base URL for the API.

    httpx_kwargs : dict, optional
        Additional keyword arguments to pass to the httpx async client.

    Attributes
    ----------
    httpx_client : httpx.AsyncClient
        An async httpx client.
    """

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str | None = None,
        httpx_kwargs: dict[str, Any] | None = None,
    ) -> None:
        """Initialize the client."""
        if base_url is None:
            base_url = BASE_URL

        base_url = base_url.rstrip("/")

        if httpx_kwargs is None:
            httpx_kwargs = {}

        if api_key is None:
            api_key = os.environ.get("WHYHOW_API_KEY")

            if api_key is None:
                raise ValueError("WHYHOW_API_KEY must be set.")

        auth = _APIKeyAuth(
            api_key=api_key,
        )

        if "base_url" in httpx_kwargs:
            raise ValueError("base_url cannot be set in httpx_kwargs.")

        httpx_kwargs["timeout"] = httpx_kwargs.get("timeout", 30)

        self.httpx_client = AsyncClient(  # nosec B113
            base_url=base_url,
            auth=auth,
            **httpx_kwargs,
        )

        self.chunks = AsyncChunksResource(client=self.httpx_client)
        self.documents = AsyncDocumentsResource(client=self.httpx_client)
        self.graphs = AsyncGraphsResource(client=self.httpx_client)
        self.schemas = AsyncSchemasResource(client=self.httpx_client)
        self.workspaces = AsyncWorkspacesResource(client=self.httpx_client)
        self.nodes = AsyncNodesResource(client=self.httpx_client)
        self.triples = AsyncTriplesResource(client=self.httpx_client)

    async def close(self) -> None:
        """Close the async client."""
        await self.httpx_client.aclose()

    async def __aenter__(self) -> "AsyncWhyHow":
        """Enter the async context manager."""
        await self.httpx_client.__aenter__()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        """Exit the async context manager."""
        await self.httpx_client.__aexit__(exc_type, exc_value, traceback)
