"""Internal utility functions."""

import json
from datetime import datetime
from typing import Any

from .schemas import Chunk, Node, Relation, Triple


def _create_graph_from_knowledge_table(
    client: Any, file_path: str, workspace_name: str, graph_name: str
) -> str:
    """
    Create a graph from a knowledge table file.

    This internal function handles the process of creating a graph
    from a knowledge table file, including data loading, structuring,
    and uploading to the specified workspace.

    Parameters
    ----------
    client
        The client object used for API interactions.
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
    print(f"Starting graph creation from knowledge table: {file_path}")

    # 1. Import the file
    with open(file_path, "r") as f:
        data = json.load(f)
    print(f"Loaded data from {file_path}")

    # 2. Structure the chunks and triples
    formatted_chunks = [
        Chunk(
            content=c["content"],
            user_metadata={
                "table_chunk_id": c["chunk_id"],
                "table_triple_id": c["triple_id"],
                "page": c["page"],
            },
        )
        for c in data["chunks"]
    ]
    print(f"Structured {len(formatted_chunks)} chunks")

    workspaces = list(client.workspaces.get_all(name=workspace_name))
    workspace = next(iter(workspaces), None)
    if not workspace:
        workspace = client.workspaces.create(name=workspace_name)
        print(f"Created new workspace: {workspace_name}")
    else:
        print(f"Using existing workspace: {workspace_name}")

    # 3. Upload the chunks to the workspace
    created_chunks = client.chunks.create(
        workspace_id=workspace.workspace_id, chunks=formatted_chunks
    )
    print(f"Uploaded {len(created_chunks)} chunks.")

    # for all chunks, get the triple_id in the user_metadata, then assign that chunk id to the triple
    formatted_triples = []

    for t in data["triples"]:
        chunk_ids = [
            c.chunk_id
            for c in created_chunks
            if "table_triple_id"
            in c.user_metadata.get(workspace.workspace_id, {})
            and c.user_metadata[workspace.workspace_id]["table_triple_id"]
            == t["triple_id"]
        ]
        formatted_triples.append(
            Triple(
                head=Node(
                    label=t["head"]["label"],
                    name=t["head"]["name"].strip("'\""),
                    properties=t["head"].get("properties", {}),
                ),
                tail=Node(
                    label=t["tail"]["label"],
                    name=t["tail"]["name"].strip("'\""),
                    properties=t["tail"].get("properties", {}),
                ),
                relation=Relation(name=t["relation"]["name"]),
                chunk_ids=chunk_ids,
            )
        )

    print(f"Structured {len(formatted_triples)} triples")

    graph = client.graphs.create_graph_from_triples(
        name=graph_name,
        workspace_id=workspace.workspace_id,
        triples=formatted_triples,
    )

    print("Successfully created graph from knowledge table.")
    return graph.graph_id


def _export_all_data(client: Any, workspace_id: str | None = None) -> str:
    """
    Output all of your WhyHow data to a JSON file.

    This internal function handles the process of exporting all of
    your WhyHow data to a JSON file.

    Parameters
    ----------
    client
        The client object used for API interactions.

    Returns
    -------
    str
        Message indicating whether or not the export succeeded.
    """
    print("Starting export of WhyHow data.")

    class DateTimeEncoder(json.JSONEncoder):
        def default(self, obj: Any) -> Any:
            if isinstance(obj, datetime):
                return obj.isoformat()
            return super().default(obj)

    out = []

    if workspace_id is None:
        workspaces = client.workspaces.get_all()
    else:
        workspace = client.workspaces.get(workspace_id=workspace_id)
        workspaces = [workspace]

    for w in list(workspaces):
        print(f"Processing workspace {w.workspace_id} ({w.name})")
        workspace_data = {
            "workspace_id": w.workspace_id,
            "name": w.name,
            "chunks": [],
            "graphs": [],
        }

        # Process chunks
        try:
            chunks = client.chunks.get_all(workspace_id=w.workspace_id)
            for c in list(chunks):
                chunk_data = c.model_dump()
                chunk_data["created_at"] = (
                    chunk_data["created_at"].isoformat()
                    if isinstance(chunk_data["created_at"], datetime)
                    else chunk_data["created_at"]
                )
                chunk_data["updated_at"] = (
                    chunk_data["updated_at"].isoformat()
                    if isinstance(chunk_data["updated_at"], datetime)
                    else chunk_data["updated_at"]
                )
                workspace_data["chunks"].append(chunk_data)
        except Exception as e:
            print(
                f"Error processing chunks for workspace {w.workspace_id}: {e}"
            )

        # Process graphs
        try:
            graphs = client.graphs.get_all(workspace_id=w.workspace_id)
            for g in list(graphs):
                try:
                    graph_data = g.model_dump()
                    graph_data["created_at"] = (
                        graph_data["created_at"].isoformat()
                        if isinstance(graph_data["created_at"], datetime)
                        else graph_data["created_at"]
                    )
                    graph_data["updated_at"] = (
                        graph_data["updated_at"].isoformat()
                        if isinstance(graph_data["updated_at"], datetime)
                        else graph_data["updated_at"]
                    )
                    graph_data["triples"] = []
                    graph_data["nodes"] = []

                    # Process schema
                    try:
                        schema = client.schemas.get(schema_id=g.schema_id)

                        schema_data = schema.model_dump()
                        schema_data["created_at"] = (
                            schema_data["created_at"].isoformat()
                            if isinstance(schema_data["created_at"], datetime)
                            else schema_data["created_at"]
                        )
                        schema_data["updated_at"] = (
                            schema_data["updated_at"].isoformat()
                            if isinstance(schema_data["updated_at"], datetime)
                            else schema_data["updated_at"]
                        )
                        graph_data["schema"] = schema_data
                    except Exception as e:
                        print(
                            f"Error processing schema for graph {g.graph_id}: {e}"
                        )

                    # Process triples
                    try:
                        triples = client.graphs.get_all_triples(
                            graph_id=g.graph_id
                        )
                        for t in list(triples):
                            triple_data = t.model_dump()
                            triple_data["created_at"] = (
                                triple_data["created_at"].isoformat()
                                if isinstance(
                                    triple_data["created_at"], datetime
                                )
                                else triple_data["created_at"]
                            )
                            triple_data["updated_at"] = (
                                triple_data["updated_at"].isoformat()
                                if isinstance(
                                    triple_data["updated_at"], datetime
                                )
                                else triple_data["updated_at"]
                            )
                            graph_data["triples"].append(triple_data)
                    except Exception as e:
                        print(
                            f"Error processing triples for graph {g.graph_id}: {e}"
                        )

                    # Process nodes
                    try:
                        nodes = client.nodes.get_all(graph_id=g.graph_id)
                        for n in list(nodes):
                            node_data = n.model_dump()
                            node_data["created_at"] = (
                                node_data["created_at"].isoformat()
                                if isinstance(
                                    node_data["created_at"], datetime
                                )
                                else node_data["created_at"]
                            )
                            node_data["updated_at"] = (
                                node_data["updated_at"].isoformat()
                                if isinstance(
                                    node_data["updated_at"], datetime
                                )
                                else node_data["updated_at"]
                            )
                            graph_data["nodes"].append(node_data)
                    except Exception as e:
                        print(
                            f"Error processing nodes for graph {g.graph_id}: {e}"
                        )

                    workspace_data["graphs"].append(graph_data)

                except Exception as e:
                    print(
                        f"Error processing graph {g.graph_id} in workspace {w.workspace_id}: {e}"
                    )
        except Exception as e:
            print(f"Error fetching graphs for workspace {w.workspace_id}: {e}")

        # Aappend workspace data
        out.append(workspace_data)

    try:

        # Clean JSON
        clean_json_output = json.dumps(out, indent=4, cls=DateTimeEncoder)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Write the JSON output to the file
        with open(f"whyhow_dump_{timestamp}.json", "w") as file:
            file.write(clean_json_output)
        return f"Exported data to whyhow_dump_{timestamp}.json"
    except Exception as e:
        print(f"Error writing JSON output to file: {e}")
        return f"Data export failed: {e}"
