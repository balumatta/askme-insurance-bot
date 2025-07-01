import asyncio
import time

from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser

from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field


class OpenAILLM:
    def __init__(self, openai_api_key, llm_model=None, temperature=0):
        self.openai_api_key = openai_api_key
        self.llm_model = llm_model if llm_model else "gpt-4o-mini"
        self.temperature = temperature

    def get_prompt(self, prompt_str, parser_required=False):
        # Define the prompt template
        if parser_required:
            prompt_str += "output format instruction : {format_instruction}"

        prompt = PromptTemplate.from_template(prompt_str)
        return prompt

    def get_llm_chain(self, prompt, openai_llm, output_parser=None):
        if output_parser:
            chain = prompt | openai_llm | output_parser
        else:
            chain = prompt | openai_llm

        return chain

    def get_output_parser(self, pydantic_object):
        output_parser = JsonOutputParser(pydantic_object=pydantic_object)
        return output_parser

    async def get_response(self, prompt_str, prompt_arguments, parser_required=False, **parser_info):
        try:
            output_parser = None
            if parser_required:
                pydantic_object = parser_info.get('pydantic_object', None)
                if not pydantic_object or isinstance(pydantic_object, BaseModel):
                    raise Exception('Pydantic Object is mandatory if parser_required=True')

                output_parser = self.get_output_parser(pydantic_object)
                prompt_arguments['format_instruction'] = output_parser.get_format_instructions()

            prompt = self.get_prompt(prompt_str, parser_required)
            llm = ChatOpenAI(
                model="gpt-4o-mini", temperature=self.temperature,
                openai_api_key=self.openai_api_key,
                model_kwargs={"response_format": {"type": "json_object"}},
            )
            chain = self.get_llm_chain(prompt, openai_llm=llm, output_parser=output_parser)
            openai_response = chain.invoke(prompt_arguments)
            return openai_response
        except Exception as e:
            print(str(e))
