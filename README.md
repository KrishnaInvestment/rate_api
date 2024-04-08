### Clone Repo
```
git clone https://github.com/KrishnaInvestment/rate_api.git
```
### Install docker & Docker Compose

```
sudo apt install docker-compose
```

### OR

##### [Please use this link to install docker](https://www.cherryservers.com/blog/install-docker-ubuntu-22-04)
##### [Please use this link to install docker-compose](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-compose-on-ubuntu-22-04)

### Start a Docker-compose Server
```sh
cd rate_api
sudo docker-compose up --build -d

When running docker-compose commands make sure you are in the directory that have docker-compose.yaml file
```

### Get the API Endpoints
##### [http://127.0.0.1/rates/?date_from=2016-01-01&date_to=2016-01-10&origin=CNSGH&destination=north_europe_main](http://127.0.0.1/rates/?date_from=2016-01-01&date_to=2016-01-10&origin=CNSGH&destination=north_europe_main)
Please Adjust the port and host accordingly

### OR
```sh
curl "http://127.0.0.1/rates/?date_from=2016-01-01&date_to=2016-01-10&origin=CNSGH&destination=north_europe_main"
```

### Stop a Docker-compose Server
```sh
sudo docker-compose down
```
### Restart a Docker-compose Server
```sh
sudo docker-compose restart
```

### Check Docker Compose Logs
```sh
sudo docker-compose logs flask
sudo docker-compose logs postfres
```

### Use Postgres DB Shell
```sh
psql -h localhost -p 5432 -U root_user -d test_db 

OR

sudo docker exec -e PGPASSWORD=test_password -it rate_api_postgres_1 psql -U root_user -d test_db

Please adjust accordingly
```

### Run API Test cases
```sh
sudo docker exec rate_api_flask_1 pytest /flask_app/tests
```

### Created Two New tables
```sql
route (
    id BIGSERIAL PRIMARY KEY,
    orig_code text,
    dest_code text,
    orig_region text,
    dest_region text
);
 AND
 
 price_detail (
    id bigint,
    route_id bigint,  <-- FOREIGN KEY (route_id) REFERENCES route(id)-->
    day date,
    price integer
);
```


### To run pre-commit hooks for static code review
```sh
sudo apt install pre-commit
cd flask_app
pre-commit run --all-files

Run
git add
Before running the pre-commit
```

- .env file already exists. Please update .env file (if required) and restart the docker-compose.