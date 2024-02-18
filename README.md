
<h1 align="center"> <p>QAGenius</p></h1>
<h3 align="center">
    <p>State-of-the-art Parameter-Efficient Fine-Tuning (PEFT) methods</p>
</h3>


# Running the project:

1. clone the repository: `git clone https://github.com/Ubaidb936/QAGenius.git`
2. Cd into QAGenius: `cd QAGenius`
3. run `pip install -r requirements.txt` to install dependencies...
4. run  `huggingface-cli login` and supply your HuggingFace token. If you do not have one, here is  how to set it up: https://huggingface.co/settings/tokens
5. Set up the variables in the Config.py like pdfPath, hf_token 
6. run `python generateQNA.py`. It saves the  Questin answer dataset generated from the input pdf to file_path in Config.py
7. run `uploadDataSetToHub.py`, if you want to push the dataset to hugginface Hub.
