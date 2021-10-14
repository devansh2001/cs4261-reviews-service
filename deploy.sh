#heroku login;
#heroku container:login;
docker build -t reviews-service .
docker tag reviews-service registry.heroku.com/cs4261-reviews-service/web
docker push registry.heroku.com/cs4261-reviews-service/web
heroku container:release web -a cs4261-reviews-service
#heroku logs --tail --app cs4261-reviews-service;