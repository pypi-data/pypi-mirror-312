import datetime
import logging

from fastapi import APIRouter
from pydantic_db_backend.backend import Backend

from eventix.functions.task import task_post, task_by_unique_key, task_reschedule
from eventix.pydantic.task import TEventixTask

log = logging.getLogger(__name__)

router = APIRouter(tags=["task"])


@router.post("/task")
async def route_task_post(task: TEventixTask) -> TEventixTask:
    return task_post(task)


@router.get("/task/{uid}")
async def route_task_get(uid: str) -> TEventixTask:
    # noinspection PyTypeChecker
    return Backend.client().get_instance(TEventixTask, uid)


@router.delete("/task/{uid}")
async def route_task_delete(uid: str) -> None:
    return Backend.client().delete_uid(TEventixTask, uid)


@router.get("/task/{uid}/reschedule")
async def route_task_reschedule_get(uid: str, eta: datetime.datetime | None = None):
    return task_reschedule(uid, eta)


@router.get("/task/by_unique_key/{unique_key}")
async def route_task_(unique_key: str) -> TEventixTask:
    return task_by_unique_key(unique_key=unique_key)


@router.delete("/task/by_unique_key/{unique_key}")
async def route_task_(unique_key: str) -> None:
    uid = task_by_unique_key(unique_key=unique_key).uid
    return Backend.client().delete_uid(TEventixTask, uid)


@router.put("/task/{uid}")
async def route_task_put(uid: str, task: TEventixTask) -> TEventixTask:
    task.uid = uid  # overwrite uid
    # noinspection PyTypeChecker
    return Backend.client().put_instance(task)
