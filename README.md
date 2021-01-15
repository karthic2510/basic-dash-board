# Building a basic monitoring dashboard

This git repository provides an overview of two aspects of data analysis:

* Data visualisation using a combination of pandas, numpy, seaborn and matplotlib to monitor and analyse user accounts
* Using dash and plotly to build a basic dashboard prototype to help answer these questions in an interactive manner

I built these as part of a fun and educational assignment with a mentor and the final required output is the PDF file called "Data Visualization exercise".This refined output, built using powerpoint and output from python, is for presenting to an audience and walking them through the analysis. 

The dash app, however, is an early stage prototype built out of personal interest. I wanted to test building an app using dash and therefore did not focus on aesthetics beyond the bare necessities. 
However, considering the ease with which dash apps can be built and iterated, for someone with experience in HTML, creating a clean, aesthetically pleasing dashboard should be quite easy. 

For raw code look at the file "Collective Health.ipynb" and "Collective Health.html"

For code on building the dash app, look at

* "app.py" which is simplified and lightweight.
* "dashboard_app.py" which was a more bulkier app using the original datasets instead of the final dataset. This meant data wrangling happened in the app, in real-time.
* Procfile which is a requirement for hosting the app on heroku
* requirements.txt which informs the heroku dynos on which packages are required for the app to run and needs to be installed to the server. 

For playing around with the app, visit [here](https://dash-sales-app.herokuapp.com/).