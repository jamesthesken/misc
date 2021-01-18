# db-runner
Run the Python script to collect data from a remote API, do some processing, and insert into a PostgreSQL database. 

## Build/Run 
Make sure a PostgreSQL DB is running on your server. Then build/run the Python image:

```
docker build -t db-runner .
docker run --rm db-runner

```