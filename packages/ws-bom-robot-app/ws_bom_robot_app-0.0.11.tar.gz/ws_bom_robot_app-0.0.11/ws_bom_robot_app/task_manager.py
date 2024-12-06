import inspect
import asyncio, os
from datetime import datetime, timedelta
from enum import Enum
from typing import Annotated, Literal, TypeVar, Optional, Dict, Union, Any
from pydantic import BaseModel, ConfigDict, Field, computed_field
from uuid import uuid4
from fastapi import APIRouter, HTTPException
from ws_bom_robot_app.config import config
from ws_bom_robot_app.llm.models.base import IdentifiableEntity
from ws_bom_robot_app.llm.utils.webhooks import WebhookNotifier
from ws_bom_robot_app.util import _log
from sqlalchemy import create_engine, Column, String, JSON, DateTime, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from abc import ABC, abstractmethod

T = TypeVar('T')

#region models
class TaskStatistics(BaseModel):
    class TaskStatisticExecutionTime(BaseModel):
        min: str
        max: str
        avg: str
    retention_days: float = config.robot_task_retention_days
    total: int
    pending: int
    completed: int
    failure: int
    exec_time: TaskStatisticExecutionTime

class TaskHeader(BaseModel):
    x_ws_bom_msg_type: Optional[str] = None
    x_ws_bom_webhooks: Optional[str] = None
    model_config = ConfigDict(
        extra='allow'
    )

class TaskMetaData(BaseModel):
    start_time: str
    end_time: Optional[str] = None
    @computed_field
    @property
    def elapsed_time(self) -> Union[str, None]:
        return str((datetime.now() if not self.end_time else datetime.fromisoformat(self.end_time)) - datetime.fromisoformat(self.start_time))
    source: Optional[str] = None
    pid: Optional[int] = None

class TaskStatus(IdentifiableEntity):
    type: Optional[str] = None
    status: Literal["pending", "completed", "failure"]
    result: Optional[T] = None
    metadata: TaskMetaData = None
    error: Optional[str] = None
    model_config = ConfigDict(
        arbitrary_types_allowed=True
    )

class TaskEntry(IdentifiableEntity):
    task: Annotated[asyncio.Task, Field(default=None, validate_default=False)] = None
    headers: TaskHeader | None = None
    status: Union[TaskStatus, None] = None
    def _get_coroutine_name(self, coroutine: asyncio.coroutines) -> str:
        if inspect.iscoroutine(coroutine):
            return coroutine.cr_code.co_name
        return "<unknown>"
    def __init__(self, **data):
        #separate task from data to handle asyncio.Task
        task = data.pop('task',None)
        super().__init__(**data)
        #bypass pydantic validation
        object.__setattr__(self, 'task', task)
        #init status
        if not self.status:
          self.status = TaskStatus(
              id=self.id,
              type=self.headers.x_ws_bom_msg_type if self.headers and self.headers.x_ws_bom_msg_type else self._get_coroutine_name(task._coro) if task else None,
              status="pending",
              metadata=TaskMetaData(
                 start_time=str(datetime.now().isoformat()),
                 source=self._get_coroutine_name(task._coro) if task else None,
                 pid=os.getpid())
              )
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        validate_assignment=True
    )

#endregion

#region interface
class TaskManagerStrategy(ABC):
    @abstractmethod
    def create_task(self, coroutine, headers: TaskHeader | None = None) -> IdentifiableEntity:
        pass

    @abstractmethod
    def update_task_status(self, task: TaskEntry) -> None:
        """Hook for additional behavior, such as persisting the task status."""
        pass

    @abstractmethod
    def get_task(self, id: str) -> TaskStatus | None:
        pass

    @abstractmethod
    def get_tasks(self) -> list[TaskStatus] | None:
        pass

    @abstractmethod
    def remove_task(self, id: str) -> None:
        pass

    @abstractmethod
    def cleanup_task(self) -> None:
        pass

    @abstractmethod
    def stats(self) -> TaskStatistics:
        pass

    def task_cleanup_rule(self, task: TaskEntry) -> bool:
        return task.status.status in {"completed", "failure"} and datetime.fromisoformat(task.status.metadata.end_time) < datetime.now() - timedelta(days=config.robot_task_retention_days)

    def task_done_callback(self, task_entry: TaskEntry, headers: TaskHeader | None = None) -> callable:
        def callback(task: asyncio.Task):
            try:
                result = task_entry.task.result()
                task_entry.status.status = "completed"
                task_entry.status.result = result
            except Exception as e:
                task_entry.status.status = "failure"
                task_entry.status.error = str(e)
            finally:
                task_entry.status.metadata.end_time = str(datetime.now().isoformat())
                #strategy-specific behavior
                self.update_task_status(task_entry)
                #notify webhooks
                if headers and headers.x_ws_bom_webhooks:
                      asyncio.create_task(
                          WebhookNotifier().notify_webhook(task_entry.status,headers.x_ws_bom_webhooks)
                          )
        return callback
    def create_task_entry(self, coroutine: asyncio.coroutines, headers: TaskHeader | None = None) -> TaskEntry:
        task = TaskEntry(
            id=str(uuid4()),
            task=asyncio.create_task(coroutine),
            headers=headers)
        task.task.add_done_callback(self.task_done_callback(task, headers))
        return task

    def stats(self) -> TaskStatistics:
        def __string_to_timedelta(value: str) -> timedelta:
            if "." in value:
                time_format = "%H:%M:%S.%f"
            else:
                time_format = "%H:%M:%S"
            time_obj = datetime.strptime(value, time_format)
            return timedelta(hours=time_obj.hour, minutes=time_obj.minute, seconds=time_obj.second, microseconds=time_obj.microsecond)
        def __timedelta_to_string(td):
            hours, remainder = divmod(td.total_seconds(), 3600)
            minutes, seconds = divmod(remainder, 60)
            return f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}.{td.microseconds}"
        _all = self.get_tasks()
        _not_pending = _all and [task for task in _all if task.status != "pending"]
        _total_not_pending = len(_not_pending)
        elapsed_times = [__string_to_timedelta(task.metadata.elapsed_time) for task in _not_pending]
        _avg_exec_time = sum(elapsed_times, timedelta()) / _total_not_pending if _total_not_pending > 0 else timedelta()
        _min_exec_time = min(elapsed_times) if _total_not_pending > 0 else timedelta()
        _max_exec_time = max(elapsed_times) if _total_not_pending > 0 else timedelta()
        return TaskStatistics(
            total= _all and len(_all) or 0,
            pending=_all and len([task for task in _all if task.status == "pending"]) or 0,
            completed=_all and len([task for task in _all if task.status == "completed"]) or 0,
            failure=_all and len([task for task in _all if task.status == "failure"]) or 0,
            exec_time=TaskStatistics.TaskStatisticExecutionTime(
                min=__timedelta_to_string(_min_exec_time),
                max=__timedelta_to_string(_max_exec_time),
                avg=__timedelta_to_string(_avg_exec_time)
            )
        )

#endregion

#memory implementation
class MemoryTaskManagerStrategy(TaskManagerStrategy):
    def __init__(self):
        self.tasks: Dict[str, TaskEntry] = {}

    def create_task(self, coroutine: asyncio.coroutines, headers: TaskHeader | None = None) -> IdentifiableEntity:
        task = self.create_task_entry(coroutine, headers)
        self.tasks[task.id] = task
        return IdentifiableEntity(id=task.id)

    def update_task_status(self, task: TaskEntry) -> None:
        """no-op for memory strategy."""
        pass

    def get_task(self, id: str) -> TaskStatus | None:
        if _task := self.tasks.get(id):
            return _task
        return None

    def get_tasks(self) -> list[TaskStatus] | None:
        return [task.status for task in self.tasks.values()]

    def remove_task(self, id: str) -> None:
        if id in self.tasks:
            del self.tasks[id]

    def cleanup_task(self):
        keys = [task.id for task in self.tasks.values() if self.task_cleanup_rule(task)]
        for key in keys:
            self.remove_task(key)

#endregion

#db implementation
Base = declarative_base()
class TaskEntryModel(Base):
    __tablename__ = "entry"
    id = Column(String, primary_key=True)
    status = Column(JSON)
    model_config = ConfigDict(
        arbitrary_types_allowed=True
    )
class DatabaseTaskManagerStrategy(TaskManagerStrategy):
    def __init__(self, db_url: str = "sqlite:///.data/db/tasks.sqlite"):
        self.engine = create_engine(db_url)
        self.Session = sessionmaker(bind=self.engine)
        Base.metadata.create_all(self.engine)

    def create_task(self, coroutine: asyncio.coroutines, headers: TaskHeader | None = None) -> IdentifiableEntity:
        task = self.create_task_entry(coroutine, headers)
        with self.Session() as session:
            session.add(TaskEntryModel(id=task.id, status=task.status.model_dump()))
            session.commit()
        return IdentifiableEntity(id=task.id)

    def update_task_status(self, task: TaskEntry) -> None:
        with self.Session() as session:
          session.query(TaskEntryModel).filter_by(id=task.id).update(
              {"status": task.status.model_dump()}
          )
          session.commit()

    def get_task(self, id: str) -> TaskStatus | None:
        with self.Session() as session:
            task = session.query(TaskEntryModel).filter_by(id=id).first()
            if task:
                return TaskEntry(**task.__dict__)
        return None

    def get_tasks(self) -> list[TaskStatus] | None:
        with self.Session() as session:
            tasks = session.query(TaskEntryModel).all()
            if tasks:
                return [TaskEntry(**task.__dict__).status for task in tasks]
        return None

    def remove_task(self, id: str) -> None:
        with self.Session() as session:
            session.query(TaskEntryModel).filter_by(id=id).delete()
            session.commit()

    def cleanup_task(self):
        with self.Session() as session:
            for task in session.query(TaskEntryModel).all():
                _task = TaskEntry(**task.__dict__)
                if self.task_cleanup_rule(_task):
                    session.query(TaskEntryModel).filter_by(id=task.id).delete()
            session.commit()
#endregion

# global instance
def __get_taskmanager_strategy() -> TaskManagerStrategy:
    if config.runtime_options().is_multi_process:
        return DatabaseTaskManagerStrategy()
    return MemoryTaskManagerStrategy()
task_manager = __get_taskmanager_strategy()
_log.info(f"Task manager strategy: {task_manager.__class__.__name__}")

#region api
router = APIRouter(prefix="/api/task", tags=["task"])

@router.get("/status/{id}")
async def _status_task(id: str) -> TaskStatus:
    task = task_manager.get_task(id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task.status

@router.get("/status")
async def _status_task_list() -> list[TaskStatus]:
    return task_manager.get_tasks()

@router.delete("/status/{id}")
async def _remove_task(id: str):
   task_manager.remove_task(id)
   return {"success":"ok"}

@router.delete("/cleanup")
async def _remove_task_list():
    task_manager.cleanup_task()
    return {"success":"ok"}

@router.get("/stats")
async def _stats() -> TaskStatistics:
    return task_manager.stats()
#endregion
