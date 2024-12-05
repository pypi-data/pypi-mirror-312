#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : utils
# @Time         : 2024/11/29 16:22
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 通用异步设计，兼容oneapi监控

from celery.result import AsyncResult

from meutils.pipe import *
from meutils.schemas.task_types import TaskResponse

from meutils.db.orm import update_or_insert
from meutils.schemas.db.oneapi_types import OneapiTask


async def create_task(async_task, request: Union[BaseModel, dict]):
    if not isinstance(request, dict):
        request = request.model_dump()

    result = async_task.apply_async(kwargs={"request": request})
    task_id = result.id
    return TaskResponse(task_id=task_id)


async def get_task(
        task_id: str,
        remote_get_task: Optional[Callable] = None,
        filter_kwargs: Optional[dict] = None
):
    result = AsyncResult(id=task_id)

    if result.ready():
        if result.successful():
            data = result.get()  # system_fingerprint
            token = data.pop("system_fingerprint", None)  # 远程任务 token/apikey

            response = TaskResponse(
                task_id=task_id,

                message="Task completed successfully",
                status=result.status,
                data=data
            )

            if remote_get_task:  # 获取远程任务
                response: TaskResponse = await remote_get_task(task_id, token)  # todo: 缓存一份

                if not isinstance(data, dict):
                    data = data.model_dump()
                response.__dict__.update(data)

        else:
            response = TaskResponse(
                task_id=task_id,

                code=1,
                message=str(result.result),
                status=result.status,
            )
    else:
        response = TaskResponse(
            task_id=task_id,

            message="Task is still running",
            status=result.status,
        )

    # 更新到数据库：异步任务
    update_fn = partial(update_oneapi_from_response, task_response=response)
    asyncio.create_task(update_or_insert(OneapiTask, filter_kwargs, update_fn))  # 测试是否会执行

    return response


# todo: 可以设计更通用的
async def update_oneapi_from_response(task: OneapiTask, task_response: TaskResponse):
    if task.status in {"SUCCESS", "FAILURE"}: return False  # 跳出轮询，不再更新

    task.data = task_response.model_dump(exclude_none=True, exclude={"system_fingerprint"})
    task.status = task_response.status
    task.progress = time.time() // 10 % 100

    if task.status == "SUCCESS":
        task.progress = "100%"
    elif task.status == "FAILURE":
        task.fail_reason = "查看详情"

    task.updated_at = int(time.time())
    task.finish_time = int(time.time())  # 不是实际时间


if __name__ == '__main__':
    pass
