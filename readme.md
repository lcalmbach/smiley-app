# Smiley-app 😃 😐 🤬
Traffic velocity measurements with friendly smiley feedback to the drivers is considered a preventive mean for encouringing defensive driving. This app is a prototype for a smiley feedback system for the city of basel. The app is offers several tools to explore this interesting dataset and to gain better insight into the question wheter smiley measurements are effective for calming traffic. 

The app is developed in Python with the Streamlit framework. statstical analysis is done with pandas the scipy modules. the app is available at https://share.streamlit.io/lcalmbch/smiley-app/main/app.py. 
To install the app locally in order adapt it to your own needs, proceed as follows:

git clone 



# Datasource
measurements: https://data.bs.ch/explore/dataset/100268/
stations: https://data.bs.ch/explore/dataset/100286/
the single measurements contain over 6mio rows, so the columns are reduced to the ones related to the measurements. All stations columns are available in a separate download and can be merged with the velocity measurements as needed in the code.

download url for the measurements:
```
https://data.bs.ch/api/explore/v2.1/catalog/datasets/100268/exports/csv?lang=de&timezone=Europe%2FZurich&use_labels=false&delimiter=%3B&select=zyklus,phase,id_standort,messung_datum,messung_zeit,v_einfahrt,v_ausfahrt,v_delta,geschwindigkeit&where=messung_jahr=2023
```