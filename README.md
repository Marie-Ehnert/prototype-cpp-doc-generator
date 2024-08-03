## About the project
This repository contains the code for a functional prototype of a documentation generator using large language models. This program is part of my Bachelors Thesis to investigate the application of an AI driven documentation framework tailored towards C++ syntax. The tool is currently only able to document a single cpp file and not a complete C++ project. 

The original inspiration to create this prototype stems from the `RepoAgent` project on GitHub which is why the concept is heavily inspired by their own built framework! Please checkout their page for a more sophisticated version that documents whole python projects with the power of AI models.

Link to RepoAgent
* https://github.com/OpenBMB/RepoAgent

## Concept

The program works as follows, it ...

* statically __analyzes__ the syntax tree of the given source code
* __extracts__ code components and their meta-information based on identifying the correct nodes in the tree
    + components encompass classes, methods and functions 
* uses `DoxyGen` to analyze reference relationships of the individual code components
* __formats__ a prompt template with the resulting Information for each code component
* sequentially __sends__ chat completion __API__ __request__ to your local `ollama` models to __generate__ __documentation__
* __creates__ a markdown documentation file in the folder of the given cpp file

## Usage

> Important Note: 
> this  program requires the script language `python` and the package manager `pip` to be installed on your machine!
***

__Before__ running the program you need follow these steps!


1.  install dependencies with `pip` in your virtual environment or globally!  

    ```
    pip install -r requirements.txt
    ```

2.  install and configure `ollama` in order to run AI models locally on your machine
    - https://github.com/ollama/ollama/blob/main/README.md#quickstart

3. install `DoxyGen`on your machine
    - https://www.doxygen.nl/manual/install.html

4. open the `Doxyfile` of this project and navigate to the line of `OUTPUT_DIRECTORY` to enter a path where DoxyGen can store its generated files!

5. open `chat_config.toml` and edit the two lines underneath `[doxygen_config]` to represent your just configured specs of `DoxyGen`

Done, Happy Generating!

## Running the program
In order to start generating documentation for your C++ source code you have to navigate your terminal to the directory of this project!

Make sure `ollama` runs in the background process!
Type `ollama serve`in your terminal to start the application

Next type the following command:
```
    python3 main.py
````
if you are using an older version of python then enter ...

```
    python main.py
````

Now the program will ask you to enter a file path pointing to your desired source file!

Next you have to specify which AI model shall be used for generating documentation. 
> Hint: to find out by what name your installed model goes by enter `ollama list` and pick your model name as input!

Now the documentation process will start!