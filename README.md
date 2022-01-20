# Zattoo multi-tenant API
> This is an API implementation for Zattoo's multi-tenant platform.

[![CodeChecks](https://github.com/saveshodhan/zattoo-multi-tenant-api/actions/workflows/github-actions-pytest.yml/badge.svg)](https://github.com/saveshodhan/zattoo-multi-tenant-api/actions?query=workflow%3ACodeChecks)
[![codecov](https://codecov.io/gh/saveshodhan/zattoo-multi-tenant-api/branch/main/graph/badge.svg?token=IZ0ZRWK68Z)](https://codecov.io/gh/saveshodhan/zattoo-multi-tenant-api)

### System requirements
This app needs the below to be present on the system:
- `Python 3`
- `PostgreSQL`
- `make` (for convenience)

### Getting started
1. Create a `virtual environment`.
   - You can do this either by the traditional way - `python3 -m venv venv` and then `source venv/bin/activate`.
   - Or you could use some third-party packages like [`virtualenvwrapper`](https://virtualenvwrapper.readthedocs.io/en/latest/).
2. After cloning the repo, run `make env` to install packages.
   - If you are going to work on the app, run `make devenv` instead. This will install a few additional packages (required for `pytest` and `flake8` below).
3. If you wish to have a dummy data setup, run `make dummydata`. This will create a database, tables, and populate them with dummy data.
   - The details of the database to be created will be fetched from the [config](config).
   - The tables will be populated as per the [models](app/models/models.py).
   - The dummy data will be populated from [dummy_data.json](dummy_data/dummy_data.json).
4. Once the database is setup, make sure to set a convenient value for `idle_in_transaction_session_timeout`.
   - For development purposes, you can set it to `0` which will make sure that the transactions don't timeout - `alter database zattoo set idle_in_transaction_session_timeout = 0`.
5. Run the app using `make run`.
6. Go to http://localhost:8081/docs to check the Swagger UI.
7. **[Only for dev purpose]** If you will be making any changes, you can use the below utilities
   - Run `make test` to run pytest based test cases.
   - Run `make flake8` to run flake8 check (runs on a diff with `main` branch)
   - These are also configured in CI

### Tech stack
- Python
- FastAPI
- PostgreSQL
- pytest
- flake8

### Design decisions
- `FastAPI` - I decided to use this framework as it is very intuitive, the documentation is really nice, the community support is growing very fast, and is an ASGI compliant framework.
- `PostgreSQL` - The task mentioned about `tenant_number` being an incremental integer, along with other data that is related to the tenant. Hence, I decided to go for SQL. Postgres because of the native JSON support, it handles scale very well (not that MySQL doesn't), and it comes with some handy utilities like `pg_bouncer`, `pg_stats`, etc.
- `pytest` - This is a very mature lib, with lots of customizations, plugins available to cater a variety of different requirements, even if the app grows complex in future.

### Future tasks
For the sake of the task and for brevity, I did not implement the below, but it can be done easily:
- Pagination support for the `/tenants` endpoint
- Custom logging that could export the logs to anywhere else if required
- Sentry for error tracking
- Prometheus to export various metrics
- Grafana to display these metrics nicely
- New Relic to monitor how does the app scale
- Implement caching of results (for scaling)

### Scaling things
In future if the app starts getting a lot of traffic, we can employ certain strategies to handle the load:
- Dockerizing the app and adding a Kubernetes layer to handle the auto up/down-scaling
- Put the setup behind an LB
- If there would be a POST / PUT / DELETE endpoint to add / update / delete a tenant, the actual work (especially database related) should be offloaded to a message queue like Kafka. This will reduce the latency on these endpoints. Of course you will have to live with [eventual consistency](https://martinfowler.com/articles/microservice-trade-offs.html#consistency)
- Segregation of database connections as `READ_ONLY` and `READ_WRITE` with both of these on separate instances
- Perform load testing of the endpoints
  - Can use `locust` for this
  - I did something similar in [loadtest_setup](https://github.com/saveshodhan/loadtest_setup)
