This is a sample service for audit logging. It provides two HTTP endpoints:
 - POST `/write`
   - `event_type` is required
   - Use `event_fields` for saving any other data 
 - GET `/search`
   - `event_type` and `time_start` are required
   - `time_stop` is optional
   - `query_params` is optional and used for filtering by `event_fields` saved while writing events

There is basic auth implemented for both endpoints. `username` and `password` is hardcoded for now (duck-taped). You can change it however you like.
See below for example use

# Run in local

1. Install and start mongo db community version. You can pass this step if you have a running mongo db instance in your
   local.

- (Recommended) Instructions for
  Docker: https://www.mongodb.com/docs/manual/tutorial/install-mongodb-community-with-docker/
- Intructions for linux: https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-ubuntu/

2. Install required packages
    ```zsh
    pip install -r requirements.txt
    ```
3. Start uvicorn Server in the root directory of the project
    ```zsh
    uvicorn main:app --reload
    ```
4. Add events
    ```zsh
   curl --location 'http://127.0.0.1:8000/write' \
   --header 'Content-Type: application/json' \
   --header 'Authorization: Basic YWRtaW46cGFzc3dvcmQ=' \
   --data '{"event_type": "create_account", "event_fields": {"name": "alperen", "age": 50}}'
    ```
5. Search events
    ```zsh
   curl --location --request GET 'http://127.0.0.1:8000/search' \
   --header 'Content-Type: application/json' \
   --header 'Authorization: Basic YWRtaW46cGFzc3dvcmQ=' \
   --data '{"event_type": "create_account", "time_start": "2020-09-15T15:53:00+05:00", "query_params": {"name": "alperen"}}'
    ```

    ```zsh
   curl --location --request GET 'http://127.0.0.1:8000/search' \
   --header 'Content-Type: application/json' \
   --header 'Authorization: Basic YWRtaW46cGFzc3dvcmQ=' \
   --data '{"event_type": "create_account", "time_start": "2000-09-15T15:53:00+05:00", "query_params": {"age": 50}}'
    ```

# Design Discussion

- Since the data schema is unknown (even-specific fields), NoSQL is a better choice than SQL. For example, PostgreSQL
  support jsonb type to keep json data, but it is not that performant.
    - MongoDB's write performance is pretty fascinating at the first look. Having indexes on many fields will affect
      write operation performance negatively. So, I just added indices on the common fields.
    - Before MongoDB, I tried to use Time Series Databases because they have performant write capabilities but unknown
      data schema caused some issues while searching. I tried InfluxDB and it creates multiple documents for one write
      if
      the doc has multiple fields. So, writing queries was complex, even it did not seem possible to do what we're
      trying
      to do here.
        - So, one more +1 for MongoDB for simplicity
- I chose FastAPI since it is easy to use
- I did not create a lot of directories because the number of files is not even 10

# TODO

- Investigate use of Time Series Databases
- Unit/integration tests
- Implement better auth
- Send logs to an external service
- Get secrets from environment instead of hardcoded variables.
- Enhance search capability. For example, age > 40

# Test

I added only load tests for now because they are end-to-end when manually checking the db and logs, then see nothing goes
wrong.

### Load Test

1. Run `locust` command in `load_test`
2. Click on the url in the terminal
3. Enter parameters and local service URL (http://127.0.0.1:8000)
4. Start test

Here is an example result for 10 users and write-heavy scenario:

<img src="images/load_test_result_1.png" width="800"/>

<img src="images/load_test_result_2.png" width="800"/>