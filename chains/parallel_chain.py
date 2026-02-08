from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel



# load
load_dotenv()

# model2 llama 
model1 = ChatGroq(
    model="llama-3.1-8b-instant"
)

# model2 allam
model2 = ChatGroq(
    model="allam-2-7b",
    temperature=0.7
)


promp1 = PromptTemplate(
    template="geerate short and simple notes for {text}",
    input_variables=['text']
)
 
 
promp2 = PromptTemplate(
    template="geerate 5 short questions from  this {text}",
    input_variables=['text']
)

promp3 = PromptTemplate(
    template="merge provided notes and quiz into single doc.\n notes->{notes} and quiz->{quiz}",
    input_variables=['notes', 'quiz']
)


parser = StrOutputParser()

parller_chain = RunnableParallel(
    {
        'notes' : promp1 | model2 | parser,
        'quiz'  : promp2 | model1 | parser
    }
    
)

# merging with model1
merge_chain = promp3 | model1 | parser

chain = parller_chain | merge_chain



# text
text = """
In LangChain, chains act as step-by-step workflows that complete tasks in sequence. Each step can use an LLM to process or transform data and then interact with external tools if needed. Built-in chains are like ready-made templates for common tasks. They link together LLMs, prompts and tools using pre-defined logic, helping developers save time by avoiding manual setup for every step.
Common Built-in Chains:
LLMChain: The most basic chain. It simply takes an input, formats it using a prompt and passes it to an LLM to get a response.
Sequential Chains: These link multiple sub-chains together, where the output of one step automatically becomes the input for the next. It's great for breaking down a complex problem.
Example: Step 1 generates a list of travel ideas and Step 2 uses that list to create a detailed itinerary.
Limitation
Less Flexible: Great for standard tasks but hard to modify for custom workflows.
Can Be Slow: Workflows with many steps or external API calls may take longer to execute.
Debugging is Hard: When something goes wrong in a long multi-step chain, figuring out where the issue is can be tricky.
"""


result =  chain.invoke({'text':text})

print(result)

chain.get_graph().print_ascii()