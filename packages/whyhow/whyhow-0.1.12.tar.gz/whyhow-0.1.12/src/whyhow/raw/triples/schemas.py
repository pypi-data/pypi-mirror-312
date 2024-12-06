"""Collection of Pydantic models for the triple routers."""

from typing import Literal

from whyhow.raw.autogen import (
    TaskResponse,
    TripleChunksResponse,
    TripleCreate,
    TriplesCreate,
    TriplesResponse,
)
from whyhow.raw.base import (
    PathParameters,
    QueryParameters,
    RequestBody,
    ResponseBody,
)

# Auxiliary models
TripleCreateRaw = TripleCreate


# GET /triples/{triple_id}
class GetTriplePathParameters(PathParameters):
    """Path parameters for the get triple endpoint."""

    triple_id: str


class GetTripleResponseBody(ResponseBody, TriplesResponse):
    """Response body for the get triple endpoint."""


# GET /triples
class GetAllTriplesQueryParameters(QueryParameters):
    """Query parameters for the get all triples endpoint."""

    skip: int | None
    limit: int | None
    type: str | None
    graph_id: str | None
    graph_name: str | None
    chunk_ids: list[str] | None
    head_node_id: str | None
    tail_node_id: str | None
    order: Literal["ascending", "descending"] | None


class GetAllTriplesResponseBody(ResponseBody, TriplesResponse):
    """Response body for the get all triples endpoint."""


# POST /triples
class CreateTriplesRequestBody(RequestBody, TriplesCreate):
    """Request body for the create triple endpoint."""


class CreateTriplesResponseBody(ResponseBody, TaskResponse):
    """Response body for the create triple endpoint."""


# DELETE /triples/{triple_id}
class DeleteTriplePathParameters(PathParameters):
    """Path parameters for the delete triple endpoint."""

    triple_id: str


class DeleteTripleResponseBody(ResponseBody, TriplesResponse):
    """Response body for the delete triple endpoint."""


# GET /triples/{triple_id}/chunks
class GetTripleChunksPathParameters(PathParameters):
    """Path parameters for the get triple chunks endpoint."""

    triple_id: str
    skip: int | None
    limit: int | None
    order: Literal["ascending", "descending"] | None


class GetTripleChunksResponseBody(ResponseBody, TripleChunksResponse):
    """Response body for the get triple chunks endpoint."""
