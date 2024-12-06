from crewai.agents.parser import AgentAction, AgentFinish
from crewai_tools import SerperDevTool
from fastapi.encoders import jsonable_encoder
from mtmaisdk import Context

search_tool = SerperDevTool()

default_max_rpm = 60


def get_wf_log_callbacks(hatctx: Context):
    def mycallback(data: AgentAction | AgentFinish | dict):
        if isinstance(data, AgentAction):
            hatctx.log(f"AgentAction {data.text}")
        else:
            # print("其他回调信息类型", data)
            hatctx.log(f"其他回调信息类型:\n {jsonable_encoder( data)}")

    return mycallback


# def fw_llm_log_fn(hatctx: Context):
#     def ctx_log(model_call_dict):
#         hatctx.log(f"{model_call_dict}")

#     return ctx_log
