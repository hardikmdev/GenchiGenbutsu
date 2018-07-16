# Project Title
<Genchi Genbutsu> 

# Idea Description
A Middleware/platform to serve data to Chatbot.
    - Parsing of Project Data
    - Translation of Project Data to a Database
    - Training the ChatBot from Database.
    - Query analyzer -> keywords based data analysis  to form query inputs
    - Data traversing -> Search for the keywords in the repository, identify the statements containing the keyword
    - Finding Answer Suitability -> Based on previous feedback for question-answer (if any) filter out the most probable results from the document, also fetch the content on which the query keyword is dependent for references.
    - Resultant output and follow on analysis
    - Rank the Data in database via a closed loop feedback to every interaction.


## Idea Abstract
Problem: 


Proposed Solution: 
An Application interface, that resembles, A chat bot, when asked a question will traverse specific documents (excel, doc, pdf) accessed via a central repository, process the text and find the most probable/suitable answer with references.
The bot will be a self learning entity and use algorithms which will filter answers and references based on the previous question-answer feedback.

Provide an interactive interface, A chat bot, when asked a question will travers all the specific documents (excel, doc, pdf) stored in a central repository, process the text and find the most probable/suitable answer.
The bot will be a self learning entity which will filter answer based on the previous question-answer feedback.


We will be providing an architecture and support solutions with following :
    - Database creation 
    - Database translation
    - Query Building
    - Solution Ranking