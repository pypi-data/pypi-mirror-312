from textwrap import dedent

from crewai import Agent, Crew, Process, Task
from crewai_tools import SerperDevTool
from mtmai.agents.ctx import mtmai_context
from mtmai.models.book_gen import BookOutline, WriteOutlineRequest
from mtmai.mtlibs.aiutils import repaire_json
from pydantic import BaseModel

search_tool = SerperDevTool()


async def call_crew(
    crew: Crew, input: dict | BaseModel, pydanticOutput: None | BaseModel = None
):
    if isinstance(input, BaseModel):
        input = input.model_dump()
    output = await crew.kickoff_async(inputs=input)

    if not output:
        raise ValueError("调用 crew 失败，因输出内容是空的")
    if not output.pydantic:
        output.pydantic = GenBlogTopicsOutput.model_validate_json(
            repaire_json(output.raw)
        )
    if not output.pydantic:
        raise ValueError(
            f"调用 crew 失败，llm输出不是 json 格式: \n========\n{output.raw}\n========\n"
        )
    if pydanticOutput:
        return pydanticOutput.model_validate(output.pydantic)
    return output.pydantic


async def crew_gen_outline(*, req: WriteOutlineRequest) -> BookOutline:
    """生成文章大纲"""
    llm = await mtmai_context.get_crawai_llm()
    researcher_agent = Agent(
        role="Research Agent",
        goal=dedent("""Gather comprehensive information about {topic} that will be used to create an organized and well-structured book outline.
Here is some additional information about the author's desired goal for the book:\n\n {goal}"""),
        backstory=dedent("""You're a seasoned researcher, known for gathering the best sources and understanding the key elements of any topic.
You aim to collect all relevant information so the book outline can be accurate and informative."""),
        # tools=get_tools("search_engine"),
        # tools=[search_engine],
        tools=[search_tool],
        llm=llm,
        verbose=True,
        max_retry_limit=100,
        max_rpm=60,
    )
    outliner_agent = Agent(
        role="Book Outlining Agent",
        goal=dedent("""Based on the research, generate a book outline about the following topic: {topic}
The generated outline should include all chapters in sequential order and provide a title and description for each chapter.
Here is some additional information about the author's desired goal for the book:\n\n {goal}"""),
        backstory=dedent("""You are a skilled organizer, great at turning scattered information into a structured format.
Your goal is to create clear, concise chapter outlines with all key topics and subtopics covered."""),
        llm=llm,
        verbose=True,
    )

    research_topic_task = Task(
        description=dedent("""Research the provided topic of {topic} to gather the most important information that will
be useful in creating a book outline. Ensure you focus on high-quality, reliable sources.

Here is some additional information about the author's desired goal for the book:\n\n {goal}
        """),
        expected_output="A set of key points and important information about {topic} that will be used to create the outline.",
        agent=researcher_agent,
    )
    generate_outline_task = Task(
        description=dedent("""Create a book outline with chapters in sequential order based on the research findings.
Ensure that each chapter has a title and a brief description that highlights the topics and subtopics to be covered.
It's important to note that each chapter is only going to be 3,000 words or less.
Also, make sure that you do not duplicate any chapters or topics in the outline.

Here is some additional information about the author's desired goal for the book:\n\n {goal}"""),
        expected_output="An outline of chapters, with titles and descriptions of what each chapter will contain. Maximum of 3 chapters.  \n\n {format_instructions}",
        output_pydantic=BookOutline,
        agent=outliner_agent,
    )
    crew = Crew(
        agents=[researcher_agent, outliner_agent],
        tasks=[research_topic_task, generate_outline_task],
        process=Process.sequential,
        verbose=True,
    )
    return crew


class GenBlogTopicsOutput(BaseModel):
    topics: list[str] = "主题列表，按优先级更好的方前面"


# 根据网站介绍生成文章主题，主题将用于生成新的文章
async def crew_gen_article_topic() -> BookOutline:
    """为文章生成 生成文章主题"""
    llm = await mtmai_context.get_crawai_llm()
    researcher_agent = Agent(
        role="Research Agent",
        backstory=dedent("""You're a seasoned researcher, known for gathering the best sources and understanding the key elements of any topic.
You aim to collect all relevant information so the book outline can be accurate and informative."""),
        goal=dedent("""通过调用搜索工具发现跟博客描述相关的热点主题\n\n"""),
        tools=[search_tool],
        llm=llm,
        verbose=True,
        max_retry_limit=100,
        max_rpm=60,
    )

    research_topic_task = Task(
        description=dedent("""blog description:
                          {description}
                         现在需要编写新的博客文章，需要主题
                           """),
        expected_output="5 个候选 topics，用于下一步的博客文章创作, 按推荐优先级，将更好的放到前面",
        agent=researcher_agent,
        output_pydantic=GenBlogTopicsOutput,
    )

    crew = Crew(
        agents=[researcher_agent],
        tasks=[research_topic_task],
        process=Process.sequential,
        verbose=True,
    )
    return crew
