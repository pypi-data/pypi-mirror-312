"""Schemas for the tasks endpoint."""

from whyhow.raw.autogen import TaskResponse
from whyhow.raw.base import PathParameters, ResponseBody


# GET /tasks/{task_id}
class GetTaskPathParameters(PathParameters):
    """Path parameters for the get task endpoint."""

    task_id: str


class GetTaskResponseBody(ResponseBody, TaskResponse):
    """Get task response body."""
