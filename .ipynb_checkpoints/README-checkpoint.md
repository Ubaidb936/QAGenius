
<h1 align="center"> <p>QAGenius 📚</p></h1>
<h3 align="left">
    <p align="left"> 
        QAGenius gives you the power to generate a Question-and-answer dataset from a supplied PDF document using HuggingFace Language Models and Langchain.
   </p>
</h3>

Every data point (question and answer) generated is judged and filtered out based on groundedness and relevance scores. 

* groundedness: how well one can answer the given question unambiguously with the given context(context: PDF document)?
* relevance:  how useful this question can be to what pdf is about?
        
                
### UseCases

Generated Datasets can be used to:

* Instruction Fine-tuning Language Models wih supplied PDF document.
* Perform retrieval-augmented-generation(RAG) evaluation and Benchmarking.
* create study materials, quizzes and practice tests based on the content of the PDF document.     


### Running the project:

1. clone the repository: `git clone https://github.com/Ubaidb936/QAGenius.git`
2. Cd into QAGenius:  `cd QAGenius`
3. create a new virtual env using this command `python3 -m venv venv` for linux/mac and `python -m venv venv` for windows.
4. to activate the venv run source `venv/bin/activate` for macOS
5. run `pip install -r requirements.txt` to install dependencies...
6. run  `huggingface-cli login` and supply your HuggingFace token. If you do not have one, here is  how to set it up: https://huggingface.co/settings/tokens
7. Set up the variables in the Config.py like pdfPath, hf_token 
8. run `python generateQNA.py`. It saves the  Questin answer dataset generated from the input pdf to file_path in Config.py
9. run `uploadDataSetToHub.py`, if you want to push the dataset to hugginface Hub.

