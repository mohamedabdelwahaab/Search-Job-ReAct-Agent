from dotenv import load_dotenv
load_dotenv()

from langchain_classic import hub
from langchain_classic.agents import AgentExecutor
from langchain_classic.agents.react.agent import create_react_agent
from langchain_ollama import ChatOllama
from langchain_tavily import TavilySearch
from langchain_classic.prompts import PromptTemplate
from langchain_classic.output_parsers import PydanticOutputParser
from langchain_core.runnables import RunnableLambda

from schemas import AgentResponse, Source
from prompts import REACT_PROMPT_WITH_FORMAT_INSTRUCTIONS


tools = [TavilySearch()]
llm = ChatOllama(model='gemma3:4b', temperature=0)
llm_structurd = llm.with_structured_output(AgentResponse)
react_prompt = hub.pull("hwchase17/react")

# output_parser = PydanticOutputParser(pydantic_object=AgentResponse)

react_prompt_formatted = PromptTemplate(
    input_variables=["input", "agent_scratchpad", "tools", "tool_names", "format_instructions"],
    template=REACT_PROMPT_WITH_FORMAT_INSTRUCTIONS,
).partial(format_instructions='')#output_parser.get_format_instructions()

agent = create_react_agent(llm, tools,prompt= react_prompt_formatted)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)
extract_output = RunnableLambda(lambda x:x['output'])
# parser_output = RunnableLambda(lambda x: output_parser.parse(x))

chain = agent_executor | extract_output | llm_structurd    # | parser_output


def main():
    result = chain.invoke(
        {"input": "Search for 3 jobs and Internships related to LLMs in Egypt on LinkedIn and provide me with the links and list their deitails."}
        )
    print(result)
    
    
if __name__ == "__main__":
    main()