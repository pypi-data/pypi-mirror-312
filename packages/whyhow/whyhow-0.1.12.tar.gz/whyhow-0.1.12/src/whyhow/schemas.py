"""User facing pyndantic models."""

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field


class ChunkMetadata(BaseModel):
    """
    Chunk metadata model.

    Attributes
    ----------
    language : str , optional
        The chunk language.
    length : int, optional
        The chunk length.
    size : int, optional
        The chunk size.
    data_source_type : str, optional
        The chunk data source type.
    index : int, optional
        The chunk index.
    page : int, optional
        The chunk page.
    start : int, optional
        The chunk start.
    end : int, optional
        The chunk end.
    """

    language: str | None = None
    length: int | None = None
    size: int | None = None
    data_source_type: str | None = None
    index: int | None = None
    page: int | None = None
    start: int | None = None
    end: int | None = None


class Chunk(BaseModel):
    """
    Chunk model.

    Attributes
    ----------
    chunk_id
        The chunk ID.
    created_at
        The creation datetime.
    updated_at
        The update datetime.
    document_id
        The document ID.
    workspace_ids
        The workspace IDs.
    metadata
        The chunk metadata.
    content
        The chunk content.
    embedding
        The chunk embedding.
    tags
        The chunk tags.
    user_metadata
        The chunk user metadata.
    """

    chunk_id: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    document_id: str | None = None
    workspace_ids: list[str] | None = None
    metadata: ChunkMetadata | None = None
    content: str | dict[str, Any]
    embedding: list[float] | None = None
    tags: dict[str, list[str]] | list[str] = Field(default_factory=dict)  # type: ignore
    user_metadata: dict[str, Any] = Field(default_factory=dict)


class DocumentMetadata(BaseModel):
    """
    Document metadata model.

    Attributes
    ----------
    size : int
        The document size.
    format : str
        The document format.
    filename : str
        The document filename.
    """

    size: int
    format: Literal["csv", "json", "pdf", "txt"]
    filename: str


class Document(BaseModel):
    """
    Document model.

    Attributes
    ----------
    document_id : str
        The document ID.
    created_at : datetime, optional
        The creation datetime.
    updated_at : datetime, optional
        The update datetime.
    workspace_ids : list[str]
        The workspace IDs.
    metadata : DocumentMetadata
        The document metadata.
    status : str
        The document status.
    tags : dict[str, Any], optional
        The document tags.
    user_metadata : dict[str, Any], optional
        The document user metadata.
    """

    document_id: str
    created_at: datetime | None = None
    updated_at: datetime | None = None
    workspace_ids: list[str]
    metadata: DocumentMetadata
    status: Literal["uploaded", "processing", "processed", "failed"]
    tags: dict[str, list[str]] | None = None
    user_metadata: dict[str, Any] | None = None


class GraphErrorDetails(BaseModel):
    """
    Graph error details model.

    Attributes
    ----------
    message : str
        The error message.
    created_at : datetime, optional
        The creation datetime.
    level : str
        The error level.
    """

    message: str
    created_at: datetime | None = None
    level: Literal["error", "critical"]


class MergeNodesRule(BaseModel):
    """
    Merge nodes rule type model.

    Attributes
    ----------
    rule_type: str
        The type of the rule.
    from_node_names: list[str]
        A list of node names from which to merge.
    to_node_name: str
        The name of the node to which others will be merged.
    node_type: str
        The type of the node.
    """

    rule_type: str
    from_node_names: list[str]
    to_node_name: str
    node_type: str


class Rule(BaseModel):
    """
    Rule model.

    Attributes
    ----------
    rule_id : str
        The ID of the field associated with the rule.
    workspace_id : str
        The ID of the workspace to which the rule belongs.
    rule : MergeNodesRule
        The rule details, including type and node information.
    created_at : datetime
        The timestamp when the rule was created.
    updated_at : datetime
        The timestamp when the rule was last updated.
    """

    rule_id: str
    workspace_id: str
    rule: MergeNodesRule
    created_at: datetime | None
    updated_at: datetime | None
    created_by: str


class Graph(BaseModel):
    """
    Graph model.

    Attributes
    ----------
    graph_id : str
        The graph ID.
    name : str
        The graph name.
    workspace_id : str
        The workspace ID.
    created_at : datetime, optional
        The creation datetime.
    updated_at : datetime, optional
        The update datetime.
    schema_id : str, optional
        The schema ID.
    status : str
        The graph status.
    errors : list[GraphErrorDetails], optional
        The graph errors.
    public : bool, optional
        The graph public status.
    """

    graph_id: str
    name: str
    workspace_id: str
    created_at: datetime | None = None
    updated_at: datetime | None = None
    schema_id: str | None = None
    status: Literal["creating", "updating", "ready", "failed"]
    errors: list[GraphErrorDetails] | None = None
    public: bool | None = None


class Node(BaseModel):
    """
    Node model.

    Attributes
    ----------
    node_id : str
        The node ID. It can be None since we allow for the user to also
        create nodes and only then send them to the server (that will
        generate the node ID).
    label : str, optional
        The node label.
    name : str, optional
        The node name.
    chunk_ids : list[str], optional
        The chunk IDs.
    properties : dict[str, Any], optional
        The node properties.
    created_at : datetime, optional
        The creation datetime.
    updated_at : datetime, optional
        The update datetime.
    graph_id : str, optional
        The graph ID.
    """

    node_id: str | None = None
    label: str | None = None
    name: str | None = None
    chunk_ids: list[str] | None = None
    properties: dict[str, Any] | Any | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    graph_id: str | None = None


class Relation(BaseModel):
    """
    Relation model.

    Attributes
    ----------
    name : str
        The relation name.
    properties : dict[str, Any], optional
        The relation properties.
    """

    name: str
    properties: dict[str, Any] | Any | None = None


class Task(BaseModel):
    """
    Task model.

    Attributes
    ----------
    task_id : str | None, optional
        The task ID.
    start_time : datetime | None, optional
        The start time of the task.
    end_time : datetime | None, optional
        The end time of the task.
    status : str
        The status of the task.
    result : str | None, optional
        The result of the task.
    """

    task_id: str | None = None
    start_time: datetime | None = None
    end_time: datetime | None = None
    status: str
    result: str | None = None


class Triple(BaseModel):
    """
    Triple model.

    Attributes
    ----------
    triple_id : str, optional
        The triple ID. It can be None since we allow for the user to also
        create triples and only then send them to the server (that will
        generate the triple ID).
    head : Node
        The head node.
    tail : Node
        The tail node.
    relation : Relation
        The relation.
    chunk_ids : list[str], optional
        The chunk IDs.
    created_at : datetime, optional
        The creation datetime.
    updated_at : datetime, optional
        The update datetime.
    properties : dict[str, Any], optional
        The triple properties.
    graph_id : str, optional
        The graph ID.
    embedding : list[float], optional
        The triple embedding.
    """

    triple_id: str | None = None
    head: Node
    tail: Node
    relation: Relation
    chunk_ids: list[str] | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    properties: dict[str, Any] | None = None
    graph_id: str | None = None
    embedding: list[float] | None = None

    model_config = ConfigDict(extra="forbid")


class Query(BaseModel):
    """
    Query model.

    Attributes
    ----------
    query_id : str
        The query ID.
    graph_id : str
        The graph ID.
    answer : str, optional
        The query answer.
    status : str
        The query status.
    nodes : list[Node]
        The query nodes.
    triples : list[Triple]
        The query triples.
    created_at : datetime, optional
        The creation datetime.
    updated_at : datetime, optional
        The update datetime.
    """

    query_id: str
    graph_id: str
    answer: str | None = None
    status: Literal["success", "pending", "failed"]
    nodes: list[Node]
    triples: list[Triple]
    created_at: datetime | None = None
    updated_at: datetime | None = None


class Workspace(BaseModel):
    """
    Workspace model.

    Attributes
    ----------
    workspace_id : str
        The workspace ID.
    name : str
        The workspace name.
    created_at : datetime, optional
        The creation datetime.
    updated_at : datetime, optional
        The update datetime.
    """

    workspace_id: str
    name: str
    created_at: datetime | None = None
    updated_at: datetime | None = None


class SchemaEntityField(BaseModel):
    """
    Entity field model.

    Attributes
    ----------
    name : str
        The field name.
    properties : list[str], optional
        The field properties.
    """

    name: str
    properties: list[str] = Field(default_factory=list)


class SchemaEntity(BaseModel):
    """
    Entity model.

    Attributes
    ----------
    name : str
        The entity name.
    description : str, optional
        The entity description.
    fields : list[SchemaEntityField], optional
        The entity fields.
    """

    name: str
    description: str = ""
    fields: list[SchemaEntityField] = Field(default_factory=list)


class SchemaRelation(BaseModel):
    """
    Relation model.

    Attributes
    ----------
    name : str
        The relation name.
    description : str, optional
        The relation description.
    """

    name: str
    description: str = ""


class SchemaTriplePattern(BaseModel):
    """
    Triple pattern model.

    Attributes
    ----------
    head : SchemaEntity
        The head entity.
    relation : SchemaRelation
        The relation.
    tail : SchemaEntity
        The tail entity.
    description : str
        The triple description.
    """

    head: SchemaEntity
    relation: SchemaRelation
    tail: SchemaEntity
    description: str


class Schema(BaseModel):
    """
    Schema model.

    Attributes
    ----------
    schema_id : str
        The schema ID.
    name : str
        The schema name.
    entities : list[SchemaEntity]
        The schema entities.
    relations : list[SchemaRelation]
        The schema relations.
    patterns : list[SchemaTriplePattern]
        The schema patterns.
    workspace_id : str
        The workspace ID.
    created_at : datetime, optional
        The creation datetime.
    updated_at : datetime, optional
        The update datetime.
    """

    schema_id: str
    name: str
    entities: list[SchemaEntity]
    relations: list[SchemaRelation]
    patterns: list[SchemaTriplePattern]
    workspace_id: str
    created_at: datetime | None = None
    updated_at: datetime | None = None


class GraphChunk(BaseModel):
    """
    Graph chunk model.

    Attributes
    ----------
    chunk : Chunk
        The chunk.
    triples : list[Triple]
        The triples.
    """

    chunk: Chunk
    triples: list[Triple]
