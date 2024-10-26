import os

from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from dotenv import load_dotenv

import logging

load_dotenv()
os.environ['USER_AGENT'] = 'MyCustomUserAgent'




class Chain:
    def __init__(self):
        self.llm = ChatGroq(temperature=0, groq_api_key=os.getenv("GROQ_API_KEY"), model_name="llama3-8b-8192")

    def extract_patient_guide(self, cleaned_text,query):

        prompt_extract = PromptTemplate.from_template(
            """
            ### SCRAPED TEXT:
            {page_data}
            ### INSTRUCTION:
            **Task:** Given the text above and the user query: "{query}", provide a concise and informative response based on the text. 
            ### OUTPUT: JSON ONLY:
            """
        )
        chain_extract = prompt_extract | self.llm

        res = chain_extract.invoke(input={"page_data": cleaned_text,"query":query})
        try:
            json_parser = JsonOutputParser()
            res = json_parser.parse(res.content)
        except OutputParserException:
            raise OutputParserException("Context too big. Unable to parse jobs.")
        return res if isinstance(res, list) else [res]



# ### SCRAPED TEXT FROM WEBSITE:
#             {page_data}
#             ### INSTRUCTION:
#             The scraped text is from the health related website.
#             ### INSTRUCTION:
#             **Task:**
#             Given the text above and the user query: "{query}",
#             provide a concise and informative response, directly answering the query based on the information in the text.
#             It should not be more than 300 words.
#             ### VALID JSON (NO PREAMBLE):