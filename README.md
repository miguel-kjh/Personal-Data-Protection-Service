# NameSearcher-WedService
Name Searcher is a web service dedicated to the handling of formatted files (pdf, docx, exel, html). Its objectives are simple is to locate, and ultimately process, textual entities known as names belonging to people. This service is dedicated to the search and management of Spanish names.
**It is still under development**

  ## Tools
  - Spacy: library dedicated to natural language processing, the entity recognizer is used to search for names.
  - Flask: Python library to create and manage wed services.
  - SQlite: Relational database, lightweight and easy to use.
  
  ## Web service interface
     - /version -> show api version
     - /file/encode -> process files
     - /file/list-names -> send a JSON with a list of the names found in the file
     - /file/tagger-html -> tag names in html files
     - /file/csv-file -> find names and send the list in a CSV file
