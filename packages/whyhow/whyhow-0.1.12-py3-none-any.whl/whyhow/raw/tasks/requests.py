"""Tasks."""

from whyhow.client import AsyncClient, Client
from whyhow.raw.base import ErrorReturnType, SuccessReturnType, asend, send
from whyhow.raw.tasks.schemas import GetTaskPathParameters, GetTaskResponseBody


# sync functions
def get_task(
    client: Client, task_id: str
) -> SuccessReturnType[GetTaskResponseBody] | ErrorReturnType:
    """Get a task by its ID."""
    url = "/tasks/{task_id}"
    path_parameters = GetTaskPathParameters(task_id=task_id)

    return send(
        client=client,
        method="get",
        url=url,
        path_parameters=path_parameters,
        response_body_schema=GetTaskResponseBody,
    )


# async functions
async def aget_task(
    client: AsyncClient, task_id: str
) -> SuccessReturnType[GetTaskResponseBody] | ErrorReturnType:
    """Get a task by its ID asynchronously."""
    url = "/tasks/{task_id}"
    path_parameters = GetTaskPathParameters(task_id=task_id)

    return await asend(
        client=client,
        method="get",
        url=url,
        path_parameters=path_parameters,
        response_body_schema=GetTaskResponseBody,
    )
