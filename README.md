# Data Modeling with PostgreSQL

This project involves a startup called ***Sparkify*** they nedeed to analyze the data they've been collecting on songs and user activity on their new music streaming app, with the main objective being to understand what songs users are listening to. They wanted to create a Postgres database with tables designed to optimize queries on song play analysis. My task was to create a database schema and ETL pipeline for this analysis. 

## Postgres Schema Design and ETL pipeline

This data model is using the Star Schema approach it has one *fact* table (songplays), and 4 *dimension* tables (users, songs, artists, time). The `DROP`, `CREATE`, `INSERT`, and `SELECT` queries are defined in **sql_queries.py**. In addition the file **create_tables.py** uses the following functions `create_database`, `drop_tables`, and `create_tables` to create the database sparkifydb with the required tables.

![](postgres_schema_diagram.png?raw=true)

Extract, transform, load processes in **etl.py** populate the songs and artists tables with data derived from the JSON song files, using the following datasets [Million Songs Dataset](https://labrosa.ee.columbia.edu/millionsong/) and the second dataset consists of log files in JSON format generated by this [Event Simulator](https://github.com/Interana/eventsim) based on the songs in the million songs dataset.