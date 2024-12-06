from typing import Optional

import structlog
from fastapi.encoders import jsonable_encoder
from mtmai.agents.ctx import init_mtmai_step_context
from mtmai.models.book_gen import (
    BookOutline,
    ChapterOutline,
    WriteOutlineRequest,
    WriteSingleChapterRequest,
)
from mtmai.mtlibs.aiutils import get_json_format_instructions
from mtmai.workflows.crews import crew_gen_outline
from mtmai.workflows.wfapp import wfapp
from mtmaisdk import Context
from pydantic import BaseModel, Field

LOG = structlog.get_logger()


class NewsArticle(BaseModel):
    title: str = Field(..., description="Title of the article.")
    url: str = Field(..., description="Link to the article.")
    summary: Optional[str] = Field(
        None, description="Summary of the article if available."
    )


class SearchResults(BaseModel):
    articles: list[NewsArticle]


class ScrapedArticle(BaseModel):
    title: str = Field(..., description="Title of the article.")
    url: str = Field(..., description="Link to the article.")
    summary: Optional[str] = Field(
        None, description="Summary of the article if available."
    )
    content: Optional[str] = Field(
        None,
        description="Content of the in markdown format if available. Return None if the content is not available or does not make sense.",
    )


# class GenerateNewsReport(Workflow):
#     web_searcher: Agent = Agent(
#         tools=[DuckDuckGo()],
#         instructions=[
#             "Given a topic, search for 10 articles and return the 5 most relevant articles.",
#         ],
#         response_model=SearchResults,
#         model=get_phidata_llm(),
#     )

#     article_scraper: Agent = Agent(
#         tools=[Newspaper4k()],
#         instructions=[
#             "Given a url, scrape the article and return the title, url, and markdown formatted content.",
#             "If the content is not available or does not make sense, return None as the content.",
#         ],
#         response_model=ScrapedArticle,
#         model=get_phidata_llm(),
#     )

#     writer: Agent = Agent(
#         model=get_phidata_llm(),
#         description="You are a Senior NYT Editor and your task is to write a new york times worthy cover story.",
#         instructions=[
#             "You will be provided with news articles and their contents.",
#             "Carefully **read** each article and **think** about the contents",
#             "Then generate a final New York Times worthy article in the <article_format> provided below.",
#             "Break the article into sections and provide key takeaways at the end.",
#             "Make sure the title is catchy and engaging.",
#             "Always provide sources for the article, do not make up information or sources.",
#             "REMEMBER: you are writing for the New York Times, so the quality of the article is important.",
#         ],
#         expected_output=dedent("""\
#         An engaging, informative, and well-structured article in the following format:
#         <article_format>
#         ## Engaging Article Title

#         ### {Overview or Introduction}
#         {give a brief introduction of the article and why the user should read this report}
#         {make this section engaging and create a hook for the reader}

#         ### {Section title}
#         {break the article into sections}
#         {provide details/facts/processes in this section}

#         ... more sections as necessary...

#         ### Key Takeaways
#         {provide key takeaways from the article}

#         ### Sources
#         - [Title](url)
#         - [Title](url)
#         - [Title](url)
#         </article_format>
#         """),
#     )

#     def run(
#         self,
#         topic: str,
#         use_search_cache: bool = True,
#         use_scrape_cache: bool = True,
#         use_cached_report: bool = False,
#     ) -> Iterator[RunResponse]:
#         logger.info(f"Generating a report on: {topic}")


# python -m g4f.cli api --bind "0.0.0.0:2400"
@wfapp.workflow(on_events=["article:gen"])
class FlowArticleGen:
    @wfapp.step(timeout="600s")
    async def gen_outlines(self, hatctx: Context):
        ctx = init_mtmai_step_context(hatctx)
        topic = hatctx.workflow_input().get("topic", "如何编写SEO文章")
        req = WriteOutlineRequest(
            topic=topic,
            goal="",
        )
        crew = await crew_gen_outline(req=req)
        inputs = req
        if isinstance(req, BaseModel):
            inputs = req.model_dump()
        inputs["format_instructions"] = get_json_format_instructions(BookOutline)
        output = await crew.kickoff_async(inputs=inputs)
        result = output.pydantic
        ctx.log(f"上一步骤生成的 topic：{topic}, 大纲 {result.chapters}")
        outlines = result.chapters
        results = []
        for index, chapter_dict in enumerate(outlines, start=1):
            ctx.log(f"编写第 {index} 章节")
            ouline = ChapterOutline.model_validate(chapter_dict)
            req = WriteSingleChapterRequest(
                goal="",
                topic=topic,
                chapter_title=ouline.title,
                chapter_description=ouline.description,
                book_outlines=outlines,
            )

            child_flow = await hatctx.aio.spawn_workflow(
                "FlowWriteChapter", req.model_dump()
            )
            r = await child_flow.result()
            results.append(r)
        return {
            "topic": topic,
            "results": jsonable_encoder(results),
        }

    # @wfapp.step(parents=["gen_outlines"], timeout="2m")
    # async def gen_chapters(self, hatctx: Context):
    #     ctx = init_mtmai_step_context(hatctx)
    #     outlines = hatctx.step_output("gen_outlines")["outlines"]
    #     topic = hatctx.step_output("gen_outlines")["topic"]
    #     ctx.log(f"上一步骤生成的 topic：{topic}, 大纲 {outlines}")

    #     results = []
    #     for index, chapter_dict in enumerate(outlines, start=1):
    #         ctx.log(f"编写第 {index} 章节")
    #         ouline = ChapterOutline.model_validate(chapter_dict)
    #         req = WriteSingleChapterRequest(
    #             goal="",
    #             topic=topic,
    #             chapter_title=ouline.title,
    #             chapter_description=ouline.description,
    #             book_outlines=outlines,
    #         )

    #         child_flow = await hatctx.aio.spawn_workflow(
    #             "FlowWriteChapter", req.model_dump()
    #         )
    #         r = await child_flow.sync_result()
    #         results.append(r)
    #     return {"results": jsonable_encoder(results)}
    #     return {"results": jsonable_encoder(results)}
    #     return {"results": jsonable_encoder(results)}
    #     return {"results": jsonable_encoder(results)}
    #     return {"results": jsonable_encoder(results)}
