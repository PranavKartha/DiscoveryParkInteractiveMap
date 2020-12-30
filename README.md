# Data_Analysis
## STEPS
* In project level(DiscoveryParkPattern) virtual venv -p python3 venv (to create virtual environment)
* go into DiscoveryParkPattern
* source venv/bin/activate (to activate virtual environment)
* pip install
    * Django==3.0.7
    * nltk
    * pandas
    * wordcloud
    * mysqlclient (might need export LIBRARY_PATH=$LIBRARY_PATH:/usr/local/opt/openssl/lib/)
    * matplotlib (for graph)
    * streamlit
    * seaborn
* SQL database application is needed (ex: MySQL)
* python commands ( in first main folder level)
    * python manage.py makemigrations ( to combine with SQL app)
    * python manage.py migrate ( to complete the process)
    * python manage.py runserver ( to activate web server)
    * ( open other terminal and activate environment and enter code to run streamlit server)streamlit run streamlit-main.py
## Files/Folder touches
* Static folder, allows Django to load external css, image and javascript
* templates folder, store pages and allow view.py to load differnt page
* park/models.py, for creating database schema and validator
* park/urls.py, controls the path between pages and store or modify data
* parkviews.py, the main file that controls all the functions to render or data modification
* setting.py in the second main folder, the following code is to make connection with the MySQL database
```DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'InteractionPatternDB',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': 'localhost',
        'PORT': '3306',
    }
} 
```
* streamlit-main.py, this is the main file for the streamlit viewer for the data analysis.

