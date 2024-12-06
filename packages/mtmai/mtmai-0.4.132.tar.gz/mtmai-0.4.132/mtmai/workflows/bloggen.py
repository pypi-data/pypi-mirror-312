from crewai_tools import SerperDevTool
from mtmai.agents.ctx import init_mtmai_step_context
from mtmai.models.book_gen import BlogState
from mtmai.mtlibs.aiutils import repaire_json
from mtmai.workflows.crews import GenBlogTopicsOutput, crew_gen_article_topic
from mtmai.workflows.wfapp import wfapp
from mtmaisdk import Context

search_tool = SerperDevTool()

default_max_rpm = 60


def get_bloginfo_by_id(blog_id: str):
    state = BlogState(
        description="专注于广州美食的博客, 以健康美食、点心类为主，特点是结合本地风俗向受众提供时令点心的做法",
        seo_keywords="广州美食|广州早点",
        day_published_count=0,
        day_publish_count_hint=10,
    )
    return state


@wfapp.workflow(on_events=["blog:gen"])
class BlogGen:
    """博客生成系统"""

    @wfapp.step(timeout="10m", retries=3)
    async def gen_topic(self, hatctx: Context):
        ctx = init_mtmai_step_context(hatctx)
        ctx.log("开始博客日更任务")
        blog_state = get_bloginfo_by_id("fake_blog_id")
        if blog_state.day_publish_count_hint <= blog_state.day_published_count:
            ctx.log("日更数量到达，停止任务")
            return {
                "message": "ok",
            }

        # 根据 blog 基本信息，生成 topic
        crew = await crew_gen_article_topic()

        output = await crew.kickoff_async(inputs=blog_state.model_dump())
        if not output:
            raise ValueError("主题生成失败 因输出为空")
        if not output.pydantic:
            output.pydantic = GenBlogTopicsOutput.model_validate_json(
                repaire_json(output.raw)
            )
        if not output.pydantic:
            raise ValueError(
                f"主题生成失败,原因是 output.pydantic 没有正确的输出格式,原始内容: \n========\n{output.raw}\n========\n"
            )
        return output.pydantic.model_dump()

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
