from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings, HuggingFaceInstructEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from langchain.agents import load_tools
from langchain.agents import initialize_agent, AgentExecutor
from langchain.agents import AgentType
from langchain.tools import BaseTool, StructuredTool, Tool, tool
from langchain.memory import ConversationBufferWindowMemory, ConversationBufferMemory
from langchain.chains import LLMChain, ConversationalRetrievalChain, ConversationChain
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv

class Conversation:
    def __init__(self, question: str, answer: str):
        self.question = question
        self.answer = answer
        
class Content:
    def __init__(self, last_question: str, last_answer: str, conversation: list):
        self.last_question = last_question
        self.last_answer = last_answer
        self.conversation = conversation
        
    def to_dict(self) -> dict:
        conversation_dict = [obj.__dict__ for obj in self.conversation]
        dict = {}
        dict["last_question"] = self.last_question
        dict["last_answer"] = self.last_answer
        dict["conversation"] = conversation_dict
        return dict
        
class ActivityAgent:

    def __init__(self):
        self.role: str = None
        self.vector_store: FAISS = None
        self.agent: AgentExecutor = None
        self.logs = []
        self.initialise_agent()

    def initialise_agent(self):
        self.add_log("ActivityAgent ===== initialize agent")
        load_dotenv()
        prompt = PromptTemplate(
            input_variables=["question"],
            template="{question}"
        )
        llm = OpenAI(temperature=0)
        memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        chain = LLMChain(llm=llm,prompt=prompt)

        policyTool = Tool.from_function(
            name="Policy Analyzer",
            description="Use this tools when you are asked about policies, terms and conditions or any questions related to organization or company",
            func=self.policy_intent
        )

        accountsTool = Tool.from_function(
            name="Accounts And Finances Analyzer",
            description="Use this tools when you are asked about any statistics, finances, accounts, earnings, profit, revenuce or any thing realted to accounts of the organization or company",
            func=self.account_intent
        )
    
        llmTool = Tool(
            name="Language Model", 
            description="use this tool for general purpose queries and logic", 
            func=chain.run
        )
        
        tools = [policyTool, accountsTool, llmTool]

        self.agent = initialize_agent(tools, 
                                llm, 
                                agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
                                verbose=True,
                                max_iterations=1, 
                                memory=memory,
                                early_stopping_method="generate")
    
    def policy_intent(self, input):
        self.add_log("> Intent Detected ==> Company Policies Information")
        docs = self.vector_store.similarity_search(input)
        return docs

    def account_intent(self, input):
        self.add_log("> Intent Detected ==> Company Finances")
        print("Current User role = ", self.role)
        if self.role == "admin":
            self.add_log("> Admin has access to Company Finances")
            return "This is privde information related to accounts"
        else:
            self.add_log("> Anyone other than admin has no right to access this information")
            return "Only admin of organisation have access to such information"
    
    def get_open_ai_vector_store(self, text_chunks) -> FAISS:
        embendings = OpenAIEmbeddings()
        self.vector_store = FAISS.from_texts(text_chunks, embedding=embendings)
        return self.vector_store
        
    def add_log(self, log: str):
        self.logs.append(log)
        print(log)
        
    def get_logs(self) -> list[str]:
        return self.logs
        
    def initialize_vector_store(self, text: str):
        self.add_log("ActivityAgent ===== initialize vector store")
        text_splitter = CharacterTextSplitter(
                separator="\n",
                chunk_size=1000,
                chunk_overlap=200,
                length_function=len
            )
        chunks = text_splitter.split_text(text)
        self.get_open_ai_vector_store(chunks)
        
    def ask_question(self, question: str) -> dict:
        print(f'Assking question: %s' % question)
        try:
            response = self.agent.run(input=question)
            memory_buffer = self.agent.memory.buffer
            
            conversation_list = []
            conversation = Conversation(question="", answer="")
            for i, message in enumerate(memory_buffer):
                if i % 2 == 0:
                    conversation.question = message.content
                else:
                    conversation.answer = message.content
                    conversation_list.append(conversation)
                    conversation = Conversation(question="", answer="")
            content = Content(last_question=question, last_answer=response, conversation=conversation_list)
            dict = content.to_dict()
            print(dict)
            return dict
        except ValueError as e:
            print(e)
            response = str(e)
            if not response.startswith("Could not parse LLM output: `"):
                raise e
            response = response.removeprefix("Could not parse LLM output: `").removesuffix("`")
            content = Content(last_question=question, last_answer=response, conversation=[])
            return content.to_dict()
    
    def save_role(self, role: str):
        print("ActivityAgent ===== role save")
        self.role = role

SharedActivityAgent = ActivityAgent()