#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : kling
# @Time         : 2024/11/28 16:18
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 注册任务

from meutils.pipe import *
from meutils.async_utils import async_to_sync_pro
from meutils.decorators.retry import retrying
from meutils.async_task import worker, shared_task

from meutils.apis.kling import kolors_virtual_try_on


@shared_task(pydantic=True, retry_kwargs={'max_retries': 5, 'countdown': 10})
@async_to_sync_pro
async def create_task(request: kolors_virtual_try_on.TryOnRequest, **kwargs):
    response = await kolors_virtual_try_on.create_task(request)
    return response


# celery_task


if __name__ == '__main__':
    pass
    # create_task.apply_async()
    # kling.create_task.apply_async(kwargs={"request": request.model_dump()})
