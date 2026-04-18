import inspect

async def run_validator(v, value):
    if inspect.iscoroutinefunction(v):
        return await v(value)
    return v(value)