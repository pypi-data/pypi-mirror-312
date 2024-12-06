"""Triples resource."""

import time
from typing import Any, AsyncIterator, Iterator

from whyhow.raw import (
    TripleCreateNodeRaw,
    acreate_triple,
    adelete_triple,
    aget_all_triples,
    aget_graph,
    aget_triple,
    aget_triple_chunks,
    create_triple,
    delete_triple,
    get_all_triples,
    get_graph,
    get_triple,
    get_triple_chunks,
)
from whyhow.resources.base import AsyncResource, Resource, validate
from whyhow.schemas import Chunk, ChunkMetadata, Node, Relation, Triple


class TriplesResource(Resource):
    """Triples resource."""

    def get(self, triple_id: str, embeddings: bool = False) -> Triple:
        """Get a triples.

        Parameters
        ----------
        triple_id : str
            The triple ID.
        embeddings : bool, optional
            Whether to include embeddings in the response.

        Returns
        -------
        Triple
            The triple.
        """
        result = get_triple(self.client, triple_id, embeddings=embeddings)
        body = validate(result)

        triple = Triple(
            triple_id=body.triples[0].field_id,
            created_at=body.triples[0].created_at,
            updated_at=body.triples[0].updated_at,
            head=Node(node_id=body.triples[0].head_node),
            tail=Node(node_id=body.triples[0].tail_node),
            relation=Relation(name=body.triples[0].type),
            properties=body.triples[0].properties,
            chunk_ids=body.triples[0].chunks,
            graph_id=body.triples[0].graph,
            embedding=body.triples[0].embedding,
        )

        return triple

    def get_all(
        self,
        limit: int = 10,
        type: str | None = None,
        graph_id: str | None = None,
        graph_name: str | None = None,
        chunk_ids: list[str] | None = None,
        head_node_id: str | None = None,
        tail_node_id: str | None = None,
        embeddings: bool = False,
        task_id: str | None = None,
    ) -> Iterator[Triple]:
        """Iterate over all triples.

        Parameters
        ----------
        limit : int, optional
            The maximum number of triples to fetch in each request.
        type : str, optional
            The type of the triple to filter by.
        graph_id : str, optional
            The graph ID to filter by.
        graph_name : str, optional
            The graph name to filter by.
        chunk_ids : list[str], optional
            The IDs of the chunks to filter by.
        head_node_id : str, optional
            The head node ID to filter by.
        tail_node_id : str, optional
            The tail node ID to filter by.
        embeddings : bool, optional
            Whether to include embeddings in the response.

        Yields
        ------
        Triple
            A triple.
        """
        skip = 0
        while True:
            result = get_all_triples(
                self.client,
                limit=limit,
                skip=skip,
                type=type,
                graph_id=graph_id,
                graph_name=graph_name,
                chunk_ids=chunk_ids,
                head_node_id=head_node_id,
                tail_node_id=tail_node_id,
                embeddings=embeddings,
                task_id=task_id,
            )
            body = validate(result)

            for triple in body.triples:
                skip += 1
                yield Triple(
                    triple_id=triple.field_id,
                    created_at=triple.created_at,
                    updated_at=triple.updated_at,
                    head=Node(node_id=triple.head_node),
                    tail=Node(node_id=triple.tail_node),
                    relation=Relation(name=triple.type),
                    properties=triple.properties,
                    chunk_ids=triple.chunks,
                    graph_id=triple.graph,
                    embedding=triple.embedding,
                )

            if len(body.triples) < limit:
                break

    def create(
        self,
        graph_id: str,
        head: Node | str,
        tail: Node | str,
        relation: Relation,
        properties: dict[str, Any] | None = None,
        chunks: list[str] | None = None,
        strict_mode: bool | None = None,
        timeout: int = 120,
        poll_interval: int = 5,
    ) -> Iterator[Triple]:
        """Create a triple.

        Parameters
        ----------
        graph_id : str
            The graph ID.
        head_node : Node | str
            The head node.
        tail_node : Node | str
            The tail node.
        type : str, optional
            The type of the triple.
        properties : dict[str, Any], optional
            The properties of the triple.
        chunks : list[str], optional
            The IDs of the chunks.
        strict_mode : bool, optional
            Whether to use strict mode.

        Returns
        -------
        Task
            The task.
        """
        head_node_raw: TripleCreateNodeRaw | str
        if isinstance(head, Node):
            if head.name is None:
                raise ValueError("Node name is required.")
            head_node_raw = TripleCreateNodeRaw(
                name=head.name,
                type=head.label,
                properties=head.properties,
            )
        else:
            head_node_raw = head

        tail_node_raw: TripleCreateNodeRaw | str
        if isinstance(tail, Node):
            if tail.name is None:
                raise ValueError("Node name is required.")
            tail_node_raw = TripleCreateNodeRaw(
                name=tail.name,
                type=tail.label,
                properties=tail.properties,
            )
        else:
            tail_node_raw = tail

        result = create_triple(
            self.client,
            graph_id,
            head_node_raw,
            tail_node_raw,
            relation.name,
            properties,
            chunks,
            strict_mode,
        )
        body = validate(result)

        task_id = body.task.field_id

        raw_response = get_graph(self.client, graph_id)
        graph_response = validate(raw_response)
        graph = graph_response.graphs[0]

        # Poll the graph status to see when the triples have been added

        start_time = time.time()
        while not (graph.status == "ready" or graph.status == "failed"):
            if time.time() - start_time > timeout:
                raise TimeoutError(
                    f"Graph {graph.field_id} did not complete within {timeout} seconds"
                )

            time.sleep(poll_interval)

            raw_response = get_graph(self.client, graph_id)
            graph_response = validate(raw_response)
            graph = graph_response.graphs[0]

        # Once the graph is build, go get the triple that was added according to its task_id

        return self.get_all(graph_id=graph_id, task_id=task_id)

    def delete(self, triple_id: str) -> Triple:
        """Delete a triple.

        Parameters
        ----------
        triple_id : str
            The triple ID.

        Returns
        -------
        Triple
            The deleted triple.
        """
        result = delete_triple(self.client, triple_id)
        body = validate(result)

        triple = Triple(
            triple_id=body.triples[0].field_id,
            created_at=body.triples[0].created_at,
            updated_at=body.triples[0].updated_at,
            head=Node(node_id=body.triples[0].head_node),
            tail=Node(node_id=body.triples[0].tail_node),
            relation=Relation(name=body.triples[0].type),
            properties=body.triples[0].properties,
            chunk_ids=body.triples[0].chunks,
            graph_id=body.triples[0].graph,
            embedding=body.triples[0].embedding,
        )

        return triple

    def get_chunks(self, triple_id: str) -> list[Chunk]:
        """Get the chunks of a triple.

        Parameters
        ----------
        triple_id : str
            The triple ID.

        Returns
        -------
        list[Chunk]
            The chunks.
        """
        result = get_triple_chunks(self.client, triple_id)

        body = validate(result)

        chunks = []
        for raw_chunk in body.chunks:
            if raw_chunk.document is None:
                document_id_ = None
            else:
                document_id_ = raw_chunk.document.field_id

            chunks.append(
                Chunk(
                    chunk_id=raw_chunk.field_id,
                    created_at=raw_chunk.created_at,
                    updated_at=raw_chunk.updated_at,
                    document_id=document_id_,
                    workspace_ids=[w.field_id for w in raw_chunk.workspaces],
                    metadata=ChunkMetadata(
                        language=raw_chunk.metadata.language,
                        length=raw_chunk.metadata.length,
                        size=raw_chunk.metadata.size,
                        data_source_type=raw_chunk.metadata.data_source_type,
                        index=raw_chunk.metadata.index,
                        page=raw_chunk.metadata.page,
                        start=raw_chunk.metadata.start,
                        end=raw_chunk.metadata.end,
                    ),
                    content=raw_chunk.content.root,
                    embedding=raw_chunk.embedding,
                    tags=raw_chunk.tags,
                    user_metadata=raw_chunk.user_metadata,
                )
            )

        return chunks


class AsyncTriplesResource(AsyncResource):
    """Triples resource."""

    async def get(self, triple_id: str) -> Triple:
        """Get a triples.

        Parameters
        ----------
        triple_id : str
            The triple ID.

        Returns
        -------
        Triple
            The triple.
        """
        result = await aget_triple(self.client, triple_id)
        body = validate(result)

        triple = Triple(
            triple_id=body.triples[0].field_id,
            created_at=body.triples[0].created_at,
            updated_at=body.triples[0].updated_at,
            head=Node(node_id=body.triples[0].head_node),
            tail=Node(node_id=body.triples[0].tail_node),
            relation=Relation(name=body.triples[0].type),
            properties=body.triples[0].properties,
            chunk_ids=body.triples[0].chunks,
            graph_id=body.triples[0].graph,
            embedding=body.triples[0].embedding,
        )

        return triple

    async def get_all(
        self,
        limit: int = 10,
        type: str | None = None,
        graph_id: str | None = None,
        graph_name: str | None = None,
        chunk_ids: list[str] | None = None,
        head_node_id: str | None = None,
        tail_node_id: str | None = None,
        task_id: str | None = None,
    ) -> AsyncIterator[Triple]:
        """Iterate over all triples.

        Parameters
        ----------
        limit : int, optional
            The maximum number of triples to fetch in each request.
        type : str, optional
            The type of the triple to filter by.
        graph_id : str, optional
            The graph ID to filter by.
        graph_name : str, optional
            The graph name to filter by.
        chunk_ids : list[str], optional
            The IDs of the chunks to filter by.
        head_node_id : str, optional
            The head node ID to filter by.
        tail_node_id : str, optional
            The tail node ID to filter by.

        Yields
        ------
        Triple
            A triple.
        """
        skip = 0
        while True:
            result = await aget_all_triples(
                self.client,
                limit=limit,
                skip=skip,
                type=type,
                graph_id=graph_id,
                graph_name=graph_name,
                chunk_ids=chunk_ids,
                head_node_id=head_node_id,
                tail_node_id=tail_node_id,
                task_id=task_id,
            )
            body = validate(result)

            for triple in body.triples:
                skip += 1
                yield Triple(
                    triple_id=triple.field_id,
                    created_at=triple.created_at,
                    updated_at=triple.updated_at,
                    head=Node(node_id=triple.head_node),
                    tail=Node(node_id=triple.tail_node),
                    relation=Relation(name=triple.type),
                    properties=triple.properties,
                    chunk_ids=triple.chunks,
                    graph_id=triple.graph,
                    embedding=triple.embedding,
                )

            if len(body.triples) < limit:
                break

    async def create(
        self,
        graph_id: str,
        head: Node | str,
        tail: Node | str,
        relation: Relation,
        properties: dict[str, Any] | None = None,
        chunks: list[str] | None = None,
        strict_mode: bool | None = None,
        timeout: int = 120,
        poll_interval: int = 5,
    ) -> AsyncIterator[Triple]:
        """Create a triple.

        Parameters
        ----------
        graph_id : str
            The graph ID.
        head : Node | str
            The head node.
        tail : Node | str
            The tail node.
        relation : Relation | str
            The relation of the triple.
        properties : dict[str, Any], optional
            The properties of the triple.
        chunks : list[str], optional
            The IDs of the chunks.
        strict_mode : bool, optional
            Whether to use strict mode.
        timeout : int, optional
            The timeout for the operation in seconds. Default is 120 seconds.
        poll_interval : int, optional
            The interval to poll for the operation status in seconds. Default is 5 seconds.

        Returns
        -------
        Iterator[Triple]
            An iterator over the created triples.
        """
        head_node_raw: TripleCreateNodeRaw | str
        if isinstance(head, Node):
            if head.name is None:
                raise ValueError("Node name is required.")
            head_node_raw = TripleCreateNodeRaw(
                name=head.name,
                type=head.label,
                properties=head.properties,
            )
        else:
            head_node_raw = head

        tail_node_raw: TripleCreateNodeRaw | str
        if isinstance(tail, Node):
            if tail.name is None:
                raise ValueError("Node name is required.")
            tail_node_raw = TripleCreateNodeRaw(
                name=tail.name,
                type=tail.label,
                properties=tail.properties,
            )
        else:
            tail_node_raw = tail

        result = await acreate_triple(
            self.client,
            graph_id,
            head_node_raw,
            tail_node_raw,
            relation.name,
            properties,
            chunks,
            strict_mode,
        )
        body = validate(result)

        task_id = body.task.field_id

        raw_response = await aget_graph(self.client, graph_id)
        graph_response = validate(raw_response)
        graph = graph_response.graphs[0]

        # Poll the graph status to see when the triples have been added

        start_time = time.time()
        while not (graph.status == "ready" or graph.status == "failed"):
            if time.time() - start_time > timeout:
                raise TimeoutError(
                    f"Graph {graph.field_id} did not complete within {timeout} seconds"
                )

            time.sleep(poll_interval)

            raw_response = await aget_graph(self.client, graph_id)
            graph_response = validate(raw_response)
            graph = graph_response.graphs[0]

        # Once the graph is build, go get the triple that was added according to its task_id

        return self.get_all(graph_id=graph_id, task_id=task_id)

    async def delete(self, triple_id: str) -> Triple:
        """Delete a triple.

        Parameters
        ----------
        triple_id : str
            The triple ID.

        Returns
        -------
        Triple
            The deleted triple.
        """
        result = await adelete_triple(self.client, triple_id)
        body = validate(result)

        triple = Triple(
            triple_id=body.triples[0].field_id,
            created_at=body.triples[0].created_at,
            updated_at=body.triples[0].updated_at,
            head=Node(node_id=body.triples[0].head_node),
            tail=Node(node_id=body.triples[0].tail_node),
            relation=Relation(name=body.triples[0].type),
            properties=body.triples[0].properties,
            chunk_ids=body.triples[0].chunks,
            graph_id=body.triples[0].graph,
            embedding=body.triples[0].embedding,
        )

        return triple

    async def get_chunks(self, triple_id: str) -> list[Chunk]:
        """Get the chunks of a triple.

        Parameters
        ----------
        triple_id : str
            The triple ID.

        Returns
        -------
        list[Chunk]
            The chunks.
        """
        result = await aget_triple_chunks(self.client, triple_id)

        body = validate(result)

        chunks = []
        for raw_chunk in body.chunks:
            if raw_chunk.document is None:
                document_id_ = None
            else:
                document_id_ = raw_chunk.document.field_id

            chunks.append(
                Chunk(
                    chunk_id=raw_chunk.field_id,
                    created_at=raw_chunk.created_at,
                    updated_at=raw_chunk.updated_at,
                    document_id=document_id_,
                    workspace_ids=[w.field_id for w in raw_chunk.workspaces],
                    metadata=ChunkMetadata(
                        language=raw_chunk.metadata.language,
                        length=raw_chunk.metadata.length,
                        size=raw_chunk.metadata.size,
                        data_source_type=raw_chunk.metadata.data_source_type,
                        index=raw_chunk.metadata.index,
                        page=raw_chunk.metadata.page,
                        start=raw_chunk.metadata.start,
                        end=raw_chunk.metadata.end,
                    ),
                    content=raw_chunk.content.root,
                    embedding=raw_chunk.embedding,
                    tags=raw_chunk.tags,
                    user_metadata=raw_chunk.user_metadata,
                )
            )

        return chunks
