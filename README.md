# saVex
Django Project for Saving, Expense and Retirement Solutions

### Build Commands

```
# # Run Migration command
python manage.py makemigrations

# # Migrate
python manage.py migrate

docker build -t richie31/saves:latest .

docker run --network=my_rasp_network -p 8000:8000 --env-file .env --restart unless-stopped richie31/savex:latest


```

### Api's

[Swagger API Documentation](http://192.168.1.2:8000/swagger/)