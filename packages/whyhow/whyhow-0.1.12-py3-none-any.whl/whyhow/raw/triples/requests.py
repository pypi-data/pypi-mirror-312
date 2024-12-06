"""Requests for the triples endpoints."""

from typing import Any, Literal

from httpx import AsyncClient, Client

from whyhow.raw.base import ErrorReturnType, SuccessReturnType, asend, send
from whyhow.raw.graphs.schemas import TripleCreateNodeRaw
from whyhow.raw.triples.schemas import (
    CreateTriplesRequestBody,
    CreateTriplesResponseBody,
    DeleteTriplePathParameters,
    DeleteTripleResponseBody,
    GetAllTriplesQueryParameters,
    GetAllTriplesResponseBody,
    GetTripleChunksPathParameters,
    GetTripleChunksResponseBody,
    GetTriplePathParameters,
    GetTripleResponseBody,
    TripleCreateRaw,
)


# sync functions
def get_triple(
    client: Client, triple_id: str, embeddings: bool = False
) -> SuccessReturnType[GetTripleResponseBody] | ErrorReturnType:
    """Get a triple by its ID."""
    url = "/triples/{triple_id}"
    if not embeddings:
        url += "?embeddings=false"
    path_parameters = GetTriplePathParameters(triple_id=triple_id)

    return send(
        client=client,
        url=url,
        method="get",
        path_parameters=path_parameters,
        response_body_schema=GetTripleResponseBody,
    )


def get_all_triples(
    client: Client,
    skip: int | None = None,
    limit: int | None = None,
    type: str | None = None,
    graph_id: str | None = None,
    graph_name: str | None = None,
    chunk_ids: list[str] | None = None,
    head_node_id: str | None = None,
    tail_node_id: str | None = None,
    order: Literal["ascending", "descending"] | None = None,
    embeddings: bool = False,
    task_id: str | None = None,
) -> SuccessReturnType[GetAllTriplesResponseBody] | ErrorReturnType:
    """Get all triples."""
    url = "/triples"
    query_params = []

    if not embeddings:
        query_params.append("embeddings=false")
    if task_id:
        query_params.append(f"task_id={task_id}")

    if query_params:
        url += "?" + "&".join(query_params)
    query_parameters = GetAllTriplesQueryParameters(
        skip=skip,
        limit=limit,
        type=type,
        graph_id=graph_id,
        graph_name=graph_name,
        chunk_ids=chunk_ids,
        head_node_id=head_node_id,
        tail_node_id=tail_node_id,
        order=order,
    )

    return send(
        client=client,
        url=url,
        method="get",
        query_parameters=query_parameters,
        response_body_schema=GetAllTriplesResponseBody,
    )


def create_triple(
    client: Client,
    graph_id: str,
    head_node: TripleCreateNodeRaw | str,
    tail_node: TripleCreateNodeRaw | str,
    type: str | None = None,
    properties: dict[str, Any] | None = None,
    chunks: list[str] | None = None,
    strict_mode: bool | None = None,
) -> SuccessReturnType[CreateTriplesResponseBody] | ErrorReturnType:
    """Create a triple."""
    url = "/triples"
    body = CreateTriplesRequestBody(
        graph=graph_id,
        strict_mode=strict_mode,
        triples=[
            TripleCreateRaw(
                head_node=head_node,
                tail_node=tail_node,
                type=type,
                properties=properties,
                chunks=chunks,
            )
        ],
    )

    return send(
        client=client,
        url=url,
        method="post",
        request_body=body,
        response_body_schema=CreateTriplesResponseBody,
    )


def delete_triple(
    client: Client,
    triple_id: str,
) -> SuccessReturnType[DeleteTripleResponseBody] | ErrorReturnType:
    """Delete a triple by its ID."""
    url = "/triples/{triple_id}"
    path_parameters = DeleteTriplePathParameters(triple_id=triple_id)

    return send(
        client=client,
        url=url,
        method="delete",
        path_parameters=path_parameters,
        response_body_schema=DeleteTripleResponseBody,
    )


def get_triple_chunks(
    client: Client,
    triple_id: str,
    skip: int | None = None,
    limit: int | None = None,
    order: Literal["ascending", "descending"] | None = None,
) -> SuccessReturnType[GetTripleChunksResponseBody] | ErrorReturnType:
    """Get all chunks for a triple by its ID."""
    url = "/triples/{triple_id}/chunks"
    path_parameters = GetTripleChunksPathParameters(
        triple_id=triple_id, skip=skip, limit=limit, order=order
    )

    return send(
        client=client,
        url=url,
        method="get",
        path_parameters=path_parameters,
        response_body_schema=GetTripleChunksResponseBody,
    )


# async functions
async def aget_triple(
    client: AsyncClient, triple_id: str, embeddings: bool = False
) -> SuccessReturnType[GetTripleResponseBody] | ErrorReturnType:
    """Get a node by its ID."""
    url = "/triples/{triple_id}"
    if not embeddings:
        url += "?embeddings=false"
    path_parameters = GetTriplePathParameters(triple_id=triple_id)

    return await asend(
        client=client,
        url=url,
        method="get",
        path_parameters=path_parameters,
        response_body_schema=GetTripleResponseBody,
    )


async def aget_all_triples(
    client: AsyncClient,
    skip: int | None = None,
    limit: int | None = None,
    type: str | None = None,
    graph_id: str | None = None,
    graph_name: str | None = None,
    chunk_ids: list[str] | None = None,
    head_node_id: str | None = None,
    tail_node_id: str | None = None,
    order: Literal["ascending", "descending"] | None = None,
    embeddings: bool = False,
    task_id: str | None = None,
) -> SuccessReturnType[GetAllTriplesResponseBody] | ErrorReturnType:
    """Get all triples."""
    url = "/triples"
    query_params = []

    if not embeddings:
        query_params.append("embeddings=false")
    if task_id:
        query_params.append(f"task_id={task_id}")

    if query_params:
        url += "?" + "&".join(query_params)
    query_parameters = GetAllTriplesQueryParameters(
        skip=skip,
        limit=limit,
        type=type,
        graph_id=graph_id,
        graph_name=graph_name,
        chunk_ids=chunk_ids,
        head_node_id=head_node_id,
        tail_node_id=tail_node_id,
        order=order,
    )

    return await asend(
        client=client,
        url=url,
        method="get",
        query_parameters=query_parameters,
        response_body_schema=GetAllTriplesResponseBody,
    )


async def acreate_triple(
    client: AsyncClient,
    graph_id: str,
    head_node: TripleCreateNodeRaw | str,
    tail_node: TripleCreateNodeRaw | str,
    type: str | None = None,
    properties: dict[str, Any] | None = None,
    chunks: list[str] | None = None,
    strict_mode: bool | None = None,
) -> SuccessReturnType[CreateTriplesResponseBody] | ErrorReturnType:
    """Create a triple."""
    url = "/triples"
    body = CreateTriplesRequestBody(
        graph=graph_id,
        strict_mode=strict_mode,
        triples=[
            TripleCreateRaw(
                head_node=head_node,
                tail_node=tail_node,
                type=type,
                properties=properties,
                chunks=chunks,
            )
        ],
    )

    return await asend(
        client=client,
        url=url,
        method="post",
        request_body=body,
        response_body_schema=CreateTriplesResponseBody,
    )


async def adelete_triple(
    client: AsyncClient,
    triple_id: str,
) -> SuccessReturnType[DeleteTripleResponseBody] | ErrorReturnType:
    """Delete a triple by its ID."""
    url = "/triples/{triple_id}"
    path_parameters = DeleteTriplePathParameters(triple_id=triple_id)

    return await asend(
        client=client,
        url=url,
        method="delete",
        path_parameters=path_parameters,
        response_body_schema=DeleteTripleResponseBody,
    )


async def aget_triple_chunks(
    client: AsyncClient,
    triple_id: str,
    skip: int | None = None,
    limit: int | None = None,
    order: Literal["ascending", "descending"] | None = None,
) -> SuccessReturnType[GetTripleChunksResponseBody] | ErrorReturnType:
    """Get all chunks for a triple by its ID."""
    url = "/triples/{triple_id}/chunks"
    path_parameters = GetTripleChunksPathParameters(
        triple_id=triple_id, skip=skip, limit=limit, order=order
    )

    return await asend(
        client=client,
        url=url,
        method="get",
        path_parameters=path_parameters,
        response_body_schema=GetTripleChunksResponseBody,
    )
