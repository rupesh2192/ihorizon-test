# ihorizon-test

### Steps to test
1. Migrate: `python manage.py migrate`
2. Load Auth Fixtures: `python manage.py loaddata authentication/fixtures/initial.json`
3. Load Auth Fixtures: `python manage.py loaddata supportdesk/fixtures/initial.json`
4. Run Server: `python manage.py runserver`
5. Visit Login Page: `http://127.0.0.1:8000/auth/login/`
6. Visit Admin Login Page: `http://127.0.0.1:8000/admin/login/`

### Credentials
There would be 1 admin, 2 customers and 2 agents created with below usernames and password for all the customers and agents is `Admin@11`, and for admin the password is `admin`
* admin
* customer
* customer_1
* agent
* agent_1


### Admin
* The status of the requests can be changed from the admin console
* The User type can be either `customer` or `agent` and can be changed from the admin console 