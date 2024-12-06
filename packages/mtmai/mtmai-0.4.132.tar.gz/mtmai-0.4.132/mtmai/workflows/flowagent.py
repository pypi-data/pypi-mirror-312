from crewai import Crew
from fastapi.encoders import jsonable_encoder
from mtmai.agents.ctx import init_mtmai_step_context
from mtmai.workflows.crews import crew_gen_outline
from mtmai.workflows.wfapp import wfapp
from mtmaisdk import Context
from pydantic import BaseModel


class AgentCallRequest(BaseModel):
    name: str
    input: any


@wfapp.workflow(on_events=["crew:call"])
class CrewCall:
    @wfapp.step(timeout="240s")
    async def call_crew(self, hatctx: Context):
        ctx = init_mtmai_step_context(hatctx)
        req = AgentCallRequest.model_validate(hatctx.workflow_input())

        agent = await get_agent_by_name(req.name)
        result = await agent.kickoff_async(req.input)
        return {"result": jsonable_encoder(result)}


async def get_agent_by_name(agent_name: str) -> Crew:
    if agent_name == "chatpter_writer":
        pass
    elif agent_name == "book_outline_writer":
        return crew_gen_outline()
    elif agent_name == "book_outline_writer":
        return await crew_gen_outline()
