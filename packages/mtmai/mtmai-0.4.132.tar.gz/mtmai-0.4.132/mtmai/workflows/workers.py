import asyncio

from mtmai.workflows.basicrag import BasicRagWorkflow
from mtmai.workflows.bloggen import BlogGen
from mtmai.workflows.chapters import FlowWriteChapter
from mtmai.workflows.flow_articlegen import FlowArticleGen
from mtmai.workflows.mcpexample import FlowMcpClientExample
from mtmai.workflows.showtimer import DemoTimerFlow
from mtmai.workflows.wfapp import wfapp


async def deploy_mtmai_workers(backend_url: str):
    # 获取配置文件
    # response = httpx.get("http://localhost:8383/api/v1/worker/config")
    # hatchet = Hatchet(debug=True)

    # list: WorkflowList = await wfapp.rest.aio.default_api.worker_config()
    worker = wfapp.worker("pyworker")
    worker.register_workflow(BasicRagWorkflow())
    worker.register_workflow(DemoTimerFlow())
    worker.register_workflow(FlowMcpClientExample())
    worker.register_workflow(FlowArticleGen())
    worker.register_workflow(FlowWriteChapter())
    worker.register_workflow(BlogGen())

    await worker.async_start()

    while True:
        await asyncio.sleep(1)
