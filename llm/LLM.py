import os
import openai
from dotenv import load_dotenv

from langchain import PromptTemplate, OpenAI, LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.schema import HumanMessage


class Agent:
    chat: ChatOpenAI
    llm_chain: LLMChain

    def __init__(self):
        load_dotenv()
        OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

        llm = OpenAI(openai_api_key=OPENAI_API_KEY, temperature=0.4)
        memory = ConversationBufferMemory(memory_key="chat_history")

        prompt = PromptTemplate(input_variables=["chat_history", "human_input"],
                                template="You are Zemfira having a conversation with a fan. Zemfira's speaking style blends candidness, intellect, and emotion, reflecting her non-conformist and introspective personality. Known for straightforward commentary, she challenges norms with intellectual depth, often referencing literature and philosophy. Her statements convey rebellion, authenticity, and empowerment, while maintaining a mysterious aura. She infuses wit and humor, delivering reflective insights with concise impact. In interviews, her soft-spoken, intimate manner draws listeners in. She tends to be quite rude when speaking with people. \n\n{chat_history}\nHuman: {human_input}\nChatbot:")
        self.llm_chain = LLMChain(llm=llm, prompt=prompt, verbose=True, memory=memory)

    def aget_reply(self, msg):
        resp = self.llm_chain.predict(human_input=msg)

        return resp
