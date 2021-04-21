# WikipediaBasedPersonaCategoriserEnricherAppDemo


1)Semantic Classifier App for Persona Enrichment. 


2)Uses Wikipedia Category hierarchy + Entities


3)Category Noise removal is also there.


Deploy this war file in Tomcat.

API Url will be as follows - 
"http://localhost:8080/SemanticClassifierv2/getTextAnalysis?text=" + text

Sample Application for noise removal and improve classification efficiency using ranked-categories.csv + All_hidden_categories.txt is also provided.

IAB segments classifier + Custom taxonomy support.

# Demo 

getTextAnalytics_url=https_%2F%2Fwww.thequint.com%2Fentertainment%2Fcelebrities%2Fanuradha-paudwal-dismisses-kerala-woman-claiming-to-be-her-daughter

```
[{"category": ["1954 births", "Living people", "Bollywood playback singers", "Indian female singers", "Marathi playback singers", "Filmfare Awards winners", "Kannada playback singers", "Place of birth missing (living people)", "Marathi-language singers"], "rho": 0.5088662, "Title": "Anuradha Paudwal", "nspot": "Anuradha Paudwal"}, {"category": ["Kerala", "States and territories of India", "States and territories established in 1956"], "rho": 0.453886, "Title": "Kerala", "nspot": "Kerala"}, {"category": ["Female mammals", "Females", "Gender", "Terms for females", "Women"], "rho": 0.14007062, "Title": "Woman", "nspot": "Woman"}]
```
