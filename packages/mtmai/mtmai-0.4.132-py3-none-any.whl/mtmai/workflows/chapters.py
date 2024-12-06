from textwrap import dedent

from crewai import Agent, Crew, Process, Task
from crewai_tools import SerperDevTool
from json_repair import repair_json
from mtmai.agents.ctx import init_mtmai_step_context, mtmai_context
from mtmai.models.book_gen import Chapter, WriteSingleChapterRequest
from mtmai.mtlibs.aiutils import get_json_format_instructions
from mtmai.workflows.wfapp import wfapp
from mtmaisdk import Context

search_tool = SerperDevTool()

default_max_rpm = 60


@wfapp.workflow(on_events=["gen:chapter"])
class FlowWriteChapter:
    @wfapp.step(timeout="5m", retries=3)
    async def gen_chapter(self, hatctx: Context):
        ctx = init_mtmai_step_context(hatctx)
        ctx.log("开始生成章节正文")
        req = WriteSingleChapterRequest.model_validate(hatctx.workflow_input())
        crew = await write_book_chapter_crew(req=req)
        inputs = req.model_dump()
        inputs["format_instructions"] = get_json_format_instructions(Chapter)
        output = await crew.kickoff_async(inputs=inputs)
        if not output:
            raise ValueError("章节生成失败 因输出为空")
        if not output.pydantic:
            output.pydantic = Chapter.model_validate_json(repair_json(output.raw))
        if not output.pydantic:
            raise ValueError(
                f"章节生成失败,原因是 output.pydantic 没有正确的输出格式,原始内容: \n========\n{output.raw}\n========\n"
            )
        ctx.log("生成章节正文完成")
        return output.pydantic.model_dump()


async def write_book_chapter_crew(*, req: WriteSingleChapterRequest):
    """生成文章一个章节"""
    llm = await mtmai_context.get_crawai_llm()

    researcher_agent = Agent(
        role="Research Agent",
        goal=dedent("""Gather comprehensive information about {topic} and {chapter_title} that will be used to enhance the content of the chapter.
Here is some additional information about the author's desired goal for the book and the chapter:\n\n {goal}
Here is the outline description for the chapter:\n\n {chapter_description}"""),
        backstory=dedent("""You are an experienced researcher skilled in finding the most relevant and up-to-date information on any given topic.
Your job is to provide insightful data that supports and enriches the writing process for the chapter."""),
        # tools=[],
        tools=[search_tool],
        llm=llm,
        max_rpm=default_max_rpm,
    )

    writer_agent = Agent(
        role="Chapter Writer",
        goal=dedent("""Write a well-structured chapter for the book based on the provided chapter title, goal, and outline.
The chapter should be written in markdown format and contain around 3,000 words."""),
        backstory=dedent("""You are an exceptional writer, known for producing engaging, well-researched, and informative content.
You excel at transforming complex ideas into readable and well-organized chapters."""),
        llm=llm,
        max_rpm=default_max_rpm,
    )

    research_chapter_task = Task(
        description=dedent("""Research the provided chapter topic, title, and outline to gather additional content that will be helpful in writing the chapter.
Ensure you focus on reliable, high-quality sources of information.

Here is some additional information about the author's desired goal for the book and the chapter:\n\n {goal}
Here is the outline description for the chapter:\n\n {chapter_description}

When researching, consider the following key points:
- you need to gather enough information to write a 3,000-word chapter
- The chapter you are researching needs to fit in well with the rest of the chapters in the book.

Here is the outline of the entire book:\n\n
{book_outlines}"""),
        expected_output="A set of additional insights and information that can be used in writing the chapter.",
        agent=researcher_agent,
    )

    write_chapter_task = Task(
        description=dedent("""Write a well-structured chapter based on the chapter title, goal, and outline description.
Each chapter should be written in markdown and should contain around 3,000 words.

Here is the topic for the book: {topic}
Here is the title of the chapter: {chapter_title}
Here is the outline description for the chapter:\n\n {chapter_description}

Important notes:
- The chapter you are writing needs to fit in well with the rest of the chapters in the book.

Here is the outline of the entire book:\n\n
{book_outlines}"""),
        agent=writer_agent,
        expected_output="A markdown-formatted chapter of around 3,000 words that covers the provided chapter title and outline description. \n\n {format_instructions}",
        output_pydantic=Chapter,
    )
    crew = Crew(
        agents=[researcher_agent, writer_agent],
        tasks=[research_chapter_task, write_chapter_task],
        process=Process.sequential,
        verbose=True,
    )
    return crew
