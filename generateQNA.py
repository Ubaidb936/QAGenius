import config 
import shutil
import requests
from urllib.parse import urlparse
import config
import sys
from tqdm.notebook import tqdm
import pandas as pd
from typing import Optional, List, Tuple
from langchain_core.language_models import BaseChatModel
import json
import datasets
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document as LangchainDocument
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.llms import HuggingFaceHub
from langchain_community.chat_models import ChatHuggingFace
import os
import random
import time

pdfPath = config.pdfPath
hf_token = config.hf_token
model_id = config.model_id
title = config.title
file_path = config.file_path


##ensuring the config.py variables are set
if pdfPath is None:
    raise ValueError("pdfPath is None. Please set the  pdf path in config.py.")

if hf_token is None:
    raise ValueError("hf_token is None. Please set the huggingFace token in config.py.")

if model_id is None:
    raise ValueError("model_id is None. Please set the model_id in config.py.")

if title is None:
    raise ValueError("title is None. Please set the title of the Pdf in config.py.")

if file_path is None:
    raise ValueError("file_path is None. Please set the local file_path in config.py.")


os.environ['HUGGINGFACEHUB_API_TOKEN'] = hf_token


#Loading the pdf
try:
    loader = PyPDFLoader(pdfPath)
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=2000,
        chunk_overlap=200,
        add_start_index=True,
        separators=["\n\n", "\n", ".", " ", ""],
    )
    langchain_docs = loader.load_and_split(text_splitter=text_splitter)
except Exception as e:
    print("An error occurred:", e)





#loading the hugginFace LLM
llm = HuggingFaceHub(
    repo_id= model_id,
    task="text-generation",
    # huggingfacehub_api_token = hf_token,
    model_kwargs={
        "max_new_tokens": 512,
        "top_k": 30,
        "temperature": 0.1,
        "repetition_penalty": 1.03,
    },
)
chat_model = ChatHuggingFace(llm=llm, token = False)



##creating the prompt and QA agent.
from langchain.prompts import ChatPromptTemplate
QA_generation_prompt = """
Your task is to develop factoid questions and  answers from  a given context.
Your factoid question should be answerable with a specific, concise piece of factual information from the context.
Your factoid question should be formulated in the same style as questions users could ask in a search engine.
This means that your factoid question MUST NOT mention something like "according to the passage" or "context".

Provide your answer as follows:

Output:::
Factoid question: (your factoid question)
Answer: (your answer to the factoid question)



Now here is the context.

Context: {context}\n
Output:::"""

QA_generation_prompt = ChatPromptTemplate.from_template(QA_generation_prompt)
QA_generation_agent = QA_generation_prompt | chat_model



##Generating the QNA.........
MAX_GENERATIONS  = len(langchain_docs)
start_time = time.time()
i = 1
N_GENERATIONS = (
    MAX_GENERATIONS
     #4 #We intentionally generate only 10 QA couples here for cost and time considerations
)

print("-----------------Generating  QNA couples....")
outputs = []
for context in random.sample(langchain_docs, N_GENERATIONS):
    # Generate QA couple
    print("Generating datapoint {}/{} in progress.....".format(i, N_GENERATIONS))
    i+=1
    output_QA_couple = QA_generation_agent.invoke({"context": context.page_content}).content
    try:
        question = output_QA_couple.split("Factoid question: ")[2].split("Answer: ")[0]
        answer = output_QA_couple.split("Answer: ")[2]
        index = answer.find("Factoid question:")
        answer = answer[:index].strip()
        outputs.append(
            {
                "context": context.page_content,
                "question": question,
                "answer": answer,
                "source_doc": context.metadata["source"],
            }
        )
    except:
        continue





## groundedness_agent and relevance_agent on the QNA
question_groundedness_critique_prompt = """
You will be given a context and a question.
Your task is to provide a 'total rating' scoring how well one can answer the given question unambiguously with the given context.
Give your answer on a scale of 1 to 5, where 1 means that the question is not answerable at all given the context, and 5 means that the question is clearly and unambiguously answerable with the context.

Provide your answer as follows:

Answer:::
Evaluation: (your rationale for the rating)
Total rating: (your rating)

Now here are the question and context.

Question: {question}\n
Context: {context}\n
Answer::: """

question_relevance_critique_prompt = """
You will be given a question.
Your task is to provide a 'total rating' representing how useful this question can be to  {title}\n
Give your answer on a scale of 1 to 5, where 1 means that the question is not useful at all, and 5 means that the question is extremely useful.

Provide your answer as follows:

Answer:::
Evaluation: (your rationale for the rating)
Total rating: (your rating)

Now here is the question.

Question: {question}\n
Answer::: """

question_groundedness_critique_prompt = ChatPromptTemplate.from_template(
    question_groundedness_critique_prompt
)
question_groundedness_critique_agent = question_groundedness_critique_prompt | chat_model

question_relevance_critique_prompt = ChatPromptTemplate.from_template(
    question_relevance_critique_prompt
)
question_relevance_critique_agent = question_relevance_critique_prompt | chat_model

i = 1
##Generating groundedness_score and relevance_score  for each QuestionAnswer...............
print("------------------------Generating groundedness_score and relevance_score  for each QNA..............")
for output in outputs:
    print("Evaluating datapoint {}/{} in progress.....".format(i, N_GENERATIONS))
    i+=1
    # Critique the generated QA couple
    question_groundedness_evaluation = question_groundedness_critique_agent.invoke(
        {"context": output["context"], "question": output["question"]}
    ).content
    question_relevance_evaluation = question_relevance_critique_agent.invoke(
        {"title": title, "question": output["question"]}
    ).content
    try:
        groundedness_score = int(question_groundedness_evaluation.split("Total rating: ")[2][0])
        groundedness_eval = question_groundedness_evaluation.split("Total rating: ")[1].split(
            "Evaluation: "
        )[1]
        relevance_score = int(question_relevance_evaluation.split("Total rating: ")[2][0])
        relevance_eval = question_relevance_evaluation.split("Total rating: ")[1].split(
            "Evaluation: "
        )[1]
        output.update(
            {
                "groundedness_score": groundedness_score,
                "groundedness_eval": groundedness_eval,
                "relevance_score": relevance_score,
                "relevance_eval": relevance_eval,
            }
        )
    except:
        continue

end_time = time.time()
elapsed_time = end_time - start_time

print(f"Time taken to generate and evaluate {N_GENERATIONS} datapoints is : {elapsed_time/60} mins")


##Filtering the QA based on the scores.....
print("----------------------------filtering the Generated QNA based on groundedness_score and relevance_score..................")
generated_questions = pd.DataFrame.from_dict(outputs)
generated_questions = generated_questions.loc[
    (generated_questions["groundedness_score"] >= 3)
    & (generated_questions["relevance_score"] >= 3)
]


##Saving the dataset  locally as cv
print("----------------saving qna dataset locally as csv......." )
generated_questions.to_csv(file_path, index=False)
print("--------------------DataFrame has been saved to:", file_path)













