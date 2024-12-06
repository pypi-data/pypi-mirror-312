import time

import structlog
from mtmai.workflows.wfapp import wfapp
from mtmaisdk import Context

LOG = structlog.get_logger()


@wfapp.workflow(on_events=["showtimer"])
class DemoTimerFlow:
    @wfapp.step()
    def start(self, context: Context):
        for i in range(10):
            context.put_stream(f"DemoTimerFlow start {i}\n")
        return {
            "status": "reading hatchet docs",
        }

    @wfapp.step(parents=["start"])
    def hello_flow_step2(self, context: Context):
        context.put_stream("hello from DemoTimerFlow load_docs")
        for i in range(10):
            context.put_stream(f"load_docs {i}\n")
            time.sleep(0.01)
        return {
            "status": "making sense of the docs",
        }

    @wfapp.step(parents=["hello_flow_step2"])
    def hello_flow_step3(self, context: Context):
        context.put_stream("<ul>")
        context.put_stream("<li>stream1</li>")
        context.put_stream("<li>stream2</li>")
        context.put_stream("<li>stream3</li>")
        context.put_stream("</ul>")
        return {
            "status": "making sense of the docs",
        }
