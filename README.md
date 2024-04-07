### Clone Repo
```
git clone https://github.com/KrishnaInvestment/rate_api.git
```
### Install docker

##### [Please use this link to install docker](https://www.cherryservers.com/blog/install-docker-ubuntu-22-04)
##### [Please use this link to install docker-compose](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-compose-on-ubuntu-22-04)

### Start a Docker-compose Server
```sh
sudo docker-compose up --build -d
```
### Get the API Endpoints
##### [http://127.0.0.1:5000/rates/?date_from=2016-01-03&date_to=2016-01-06&origin=china_south_main&destination=scandinavia](http://127.0.0.1:5000/rates/?date_from=2016-01-03&date_to=2016-01-06&origin=china_south_main&destination=scandinavia)
Please Adjust the port and host accordingly

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
Please adjust accordingly
```

### Run API Test cases
```sh
sudo docker exec rate_api_flask_1 pytest /flask_app/tests
```

### To run pre-commit hooks for static code review
```sh
sudo apt install pre-commit

pre-commit run --all-files

Run
git add
Before running the pre-commit
```