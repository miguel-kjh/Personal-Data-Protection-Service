![Version](https://img.shields.io/badge/version-1.2-brightgreen.svg?style=flat-square)
![Version](https://img.shields.io/badge/release-beta-green.svg?style=flat-square)

# NameSearcher-WebService
Name Searcher is a web service dedicated to the handling of formatted files (pdf, docx, exel, html). Its objectives are simple is to locate, and ultimately process, textual entities known as names belonging to people. This service is dedicated to the search and management of Spanish names.
**It is still under development**

  ## Tools
  - Spacy: library dedicated to natural language processing, the entity recognizer is used to search for names.
  - Flask: Python library to create and manage wed services.
  - SQlite: Relational database, lightweight and easy to use.
  
  ## Web service interface
     - /search/version -> show api version
     - /search/file/encode -> process files
     - /search/file/list-names -> send a JSON with a list of the names found in the file
     - /search/file/tagger-html -> tag names in html files
     - /search/file/csv-file -> find names and send the list in a CSV file
 
 ## License
 Licensed under the Apache License, Version 2.0. Copyright 2019 Miguel Ángel Medina Ramírez.
