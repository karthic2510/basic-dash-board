# Building a basic monitoring dashboard

This git provides an overview of two aspects of data analysis:

* Data visualisation using a combination of pandas, numpy, seaborn and matplotlib to monitor and analyse user accounts
* Using dash and plotly to build a very fundamental dashboard to help answer these questions in an interactive manner

I built these as part of a fun and educational assignment with a mentor and the final required output is the PDF file called Data Visualization exercise. This was a more refined output using powerpoint so that I could present to an audience. 
The dash app however is extremely unrefined. I wanted to test out building an app and therefore did not spend much time on refining the HTML and CSS aspects. However, considering the ease with which dash apps can be built and iterated, for someone with experience in HTML, creating a clean, aesthetically pleasing dashboard should be quite easy. 

For actual, messy code look at the file "Collective Health.ipynb" and "Collective Health.html"

For code on building the dash app, look at

* "app.py" which is more simplified
* "dashboard_app.py" which was a more bulkier app which used the original datasets instead of the final dataset
* Procfile which is a requirement for hosting it on heroku
* requirements.txt which is also a requirement for hosting it on heroku

For playing around with the app, visit [here](https://dash-sales-app.herokuapp.com/).