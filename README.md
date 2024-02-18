
<h1 align="center"> <p>QAGenius</p></h1>
<h3 align="center">
    <p> 
        QAGenius gives you the power to generate a Question-and-answer dataset from a supplied PDF document using HuggingFace Models and Langchain. Every data point (question and answer) is judged and filtered out based on groundedness and relevance scores. 
        groundedness: how well one can answer the given question unambiguously with the given context(context: PDF document)?
        relevance:  how useful this question can be to what pdf is about?
        
   </p>
</h3>


<h3 align="left">
# Running the project:

1. clone the repository: `git clone https://github.com/Ubaidb936/QAGenius.git`
2. Cd into QAGenius: `cd QAGenius`
3. run `pip install -r requirements.txt` to install dependencies...
4. run  `huggingface-cli login` and supply your HuggingFace token. If you do not have one, here is  how to set it up: https://huggingface.co/settings/tokens
5. Set up the variables in the Config.py like pdfPath, hf_token 
6. run `python generateQNA.py`. It saves the  Questin answer dataset generated from the input pdf to file_path in Config.py
7. run `uploadDataSetToHub.py`, if you want to push the dataset to hugginface Hub.
</h3>
