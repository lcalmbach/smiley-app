# Smiley-app 😃 😐 🤬
Traffic velocity measurements with friendly smiley feedback to the drivers is considered a preventive mean for encouringing defensive driving. This app is a prototype for a smiley feedback system for the city of basel. The app is offers several tools to explore this interesting dataset and to gain better insight into the question wheter smiley measurements are effective for calming traffic. 

The app is developed in Python with the Streamlit framework. statstical analysis is done with pandas the scipy modules. the app is available at https://share.streamlit.io/lcalmbch/smiley-app/main/app.py. 
To install the app locally in order adapt it to your own needs, proceed as follows:

```bash	
> git clone https://github.com/lcalmbach/smiley-app.git
> cd smiley-app
> py -m venv .venv
> .venv\Scripts\activate
> pip install -r requirements.txt
> streamlit run app.py
```


# Datasource
measurements: https://data.bs.ch/explore/dataset/100268/
stations: https://data.bs.ch/explore/dataset/100286/
the single measurements contain over 6mio rows, so the columns are reduced to the ones related to the measurements. All stations columns are available in a separate download and can be merged with the velocity measurements as needed in the code.

The entire datasets includes more than 6mio rows, so the columns are reduced to the ones related to the measurements. All stations columns are available in a separate download and can be merged with the velocity measurements as needed in the code. Downloading the full dataset is not recommended, as the download times out most of the time. Use the following url to download the data for a single year. The year can be changed by modifying the where clause at the end of the url:
```
https://data.bs.ch/api/explore/v2.1/catalog/datasets/100268/exports/csv?lang=de&timezone=Europe%2FZurich&use_labels=false&delimiter=%3B&select=zyklus,phase,id_standort,messung_datum,messung_zeit,v_einfahrt,v_ausfahrt,v_delta,geschwindigkeit&where=messung_jahr=2023
```

# Additional resources
- https://models.geo.bs.ch/Modellbeschreibungen/SY_SmileyGeschwindigkeitsanzeigen_KGDM_V1_0.pdf