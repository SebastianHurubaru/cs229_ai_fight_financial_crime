# cs229_ai_fight_financial_crime
CS229 Final Project: An AI approach to fighting financial crime using the UK companies register

1. Corporate informations are downloaded from Company `house, the UK companies registrar.

2. Data from companies is of poor quality and required corrections:
(i) names  of countries are not standardized and sometimes name of cities or postcodes are entered instead. Use NLP  to recognize countries names and clean-up the database.
(ii) identical names of individuals and corporate entities are treated wrongly as separate entities in the Company House Database, requiring multiple searches to take place to correct this issue.

3. We convert  the raw inputs of the model (nationality and status corporate/individual of the officers and the beneficial owners) for each corporate using a bag of words approach into a vector of size 492, representing (245 countries+ one unknown)* 2. We multiply by 2 to represent an individual officer and a corporate officer.

Given the number of countries, we also created two other vectors:
(i) a vector with regions and also included the European Union list of tax havens (American Samoa, Belize, Dominica, Fiji, Guam, Marshall Islands, Oman, Samoa, Trinidad and Tobago, United Arab Emirates, Vanuatu,
US Virgin Islands the "Blacklist") as at 17 May 2019: https://ec.europa.eu/taxation_customs/sites/taxation/files/eu_list_update_17_05_2019_en.pdf
(ii) a vector with a mix of regions and individual countries (aggregating Africa, Antarctica, North America, South America, Asia, other Oceania and Middle-East), and providing detailed countries for Europe, Eastern Europe and Central Asia, and Caribbean.

4.Snorkel

5. The dataset has been split between train  [], dev [], and test [].

6. The following models have been applied on the train and dev datasets.
-SVM;
-...


7. The most promising models were [model1], [model2] and [model3], with the following results:
[insert table]

On the test, we obtained the following performance:
[insert table]

8. Discussion and conclusion
