from textwrap import dedent

from crewai import LLM, Agent, Crew, Process, Task
from mtmai.agents.ctx import init_mtmai_step_context
from mtmai.agents.tools.tools import get_tools
from mtmai.mtlibs.aiutils import get_json_format_instructions
from mtmai.workflows.crews import call_crew
from mtmai.workflows.flowbase.helper import get_wf_log_callbacks
from mtmai.workflows.wfapp import wfapp
from mtmaisdk import Context
from pydantic import BaseModel

default_max_rpm = 600


class GenBlogTopicsOutput(BaseModel):
    topics: list[str] = "主题列表，按优先级更好的方前面"


@wfapp.workflow(on_events=["blog:gen"])
class BlogGen:
    """博客生成系统"""

    @wfapp.step(timeout="10m", retries=3)
    async def gen_topic(self, hatctx: Context):
        ctx = init_mtmai_step_context(hatctx)
        input = hatctx.workflow_input()
        callback = get_wf_log_callbacks(hatctx)
        llm = LLM(
            model="openai/llama3.1-70b",
            # temperature=llm_item.temperature or None,
            base_url="https://llama3-1-70b.lepton.run/api/v1/",
            api_key="iByWYsIUIBe6qRYBswhLVPRyiVKkYb8r",
            num_retries=5,
            logger_fn=callback,
        )
        researcher_agent = Agent(
            role="Research Agent",
            backstory=dedent("""You're a seasoned researcher, known for gathering the best sources and understanding the key elements of any topic.
    You aim to collect all relevant information so the book outline can be accurate and informative."""),
            goal=dedent("""通过调用搜索工具发现跟博客描述相关的热点主题\n\n"""),
            tools=get_tools("search_engine"),
            llm=llm,
            verbose=True,
            max_retry_limit=100,
            max_rpm=60,
            step_callback=callback,
            task_callback=callback,
        )

        format_instructions = get_json_format_instructions(GenBlogTopicsOutput)
        format_instructions = format_instructions.replace("{", "{{").replace("}", "}}")

        research_topic_task = Task(
            description=dedent(
                dedent(
                    """blog description:
                        {description}
                        现在需要编写新的博客文章，需要主题


                        """
                )
            ),
            expected_output="3 个候选 topics，用于下一步的博客文章创作"
            "按推荐优先级，将更好的放到前面"
            "必须使用严格的JSON输出最终结果，不做任何寒暄、解释，需要严格是JSON格式: "
            + format_instructions,
            agent=researcher_agent,
            output_pydantic=GenBlogTopicsOutput,
            callback=callback,
        )

        crew = Crew(
            agents=[researcher_agent],
            tasks=[research_topic_task],
            process=Process.sequential,
            verbose=True,
            step_callback=callback,
            task_callback=callback,
        )

        return await call_crew(crew, input)

    @wfapp.step(timeout="10m", retries=3, parents=["gen_topic"])
    async def gen_post(self, hatctx: Context):
        ctx = init_mtmai_step_context(hatctx)
        topics = hatctx.step_output("gen_topic").get("topics")
        ctx.log(f"挑选第一个主题生成文章 {topics}")
        flow_article = await hatctx.aio.spawn_workflow(
            "FlowArticleGen",
            {
                "topic": topics[0],
            },
        )
        post = await flow_article.result()

        return {"post": post}
