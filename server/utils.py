import asyncio


def end_gracefully_tasks(loop):
    to_cancel = asyncio.all_tasks(loop)

    for task in to_cancel:
        task.cancel()

    loop.run_until_complete(
        asyncio.gather(*to_cancel, loop=loop, return_exceptions=True))

    for task in to_cancel:
        if task.cancelled():
            continue
        if task.exception() is not None:
            loop.call_exception_handler({
                'message': 'unhandled exception during shutdown',
                'exception': task.exception(),
                'task': task,
            })
