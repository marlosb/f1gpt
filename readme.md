# F1GTP

An AI that gets Formula 1 data and write twitter posts about it. The intent is to inspire similar projects using data from Formula 1 and other sources (maybe Forza?).

## Requirements
- Python (tested on version 3.10.0)
- an environment variable named OPENAI_API_KEY with your Azure OpenAI API key
- all libraries in requirements.txt

## Usage (examples)

The main.py file is only an example of how to use the code. The examples are hard coded. You must use a different code to use it.

To run from command line:

```bash
python main.py <option>
```
Where option can be: 
 - 'event' : Create a post about race weekend with event name, location, date and time.
 - 'session' : Create a post about a session (either pratice or qualify) with session with fastest drivers names, times. Also create a chart.png file with the comparison of the best lap of the 2 fastest drivers.
 - 'race' : Create a post about race results with the top 3 drivers names, times and laps. 
 - 'range' : Create a detailed post with comparison of the two fastest driver in a specific section of the lap. Also create a chart.png file with this comparison.

 ## Details

 Each option (event, session, race and range) are 'skills' from this AI. Anyone can extend this AI by creating new prompts and code that feeds this prompts with data. The 'skills' are made of a prompt file and a class/method that supply information to the prompt.

 - prompts/: directory with prompts files (txt) used instruct the model and generate the text. If you want to create new skills, you must create a new prompt file in this directory.
 - f1gpt/__init__.py: blank init file to make the directory a python module.
 - f1gpt/briefiers.py: classes that consume data and generate the information to feed the prompts, which I called briefing. If you want to create new skills, you must create a new class in this file.
 - f1gpt/call.py: class that calls the azure OpenAI API and generate the text.
 - f1gpt/connectors.py: classes that connect to the data sources and return the data. If you want to use a different data source, you must create a new class in this file. To use existing briefers you must ensure that object from new classes have same attributes from existing class.
 - f1gpt/plotter.py: class that generates the charts.
 - f1gpt/prompts.py: class that reads the prompt files and generate prompt objects from langchain framework.

 ## See results

 [https://twitter.com/F1gpt_analysis](https://twitter.com/F1gpt_analysis)
