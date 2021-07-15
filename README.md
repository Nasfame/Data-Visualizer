# Data-Visualizer
Backend REST API that provides data to dashboard for data visualizing

## Deployed  
 https://data-charter.herokuapp.com/

## Documentation
**`Postman`**

## Tech Stacks Involved

**Python**
**Flask** (Backend-MicroFramework)
**SQL-Alchemy** ( ORM)
**Sqlite3** (DB) (light,fast)

 ## Notable Mentions

1.I have created an api for posting new data to the DB.
2. For authentication - I have used flask-login api. It is native to flask hence faster .  Had in mind was JWT
3. Security - To ensure  user credentials aren't leaked during a breach - instead of storing passwords in raw form,sha256 hash value of password is stored. 
4. Slimming SQLInjection- ORM-SQLALCHEMY is used.
5.Documented using POSTMAN.

API - SignUP/In,Assignment APIS including topN,CRUD API

## Bugs

1. order_by method seems to be not working properly in the orm.

## What Next?

1. Fix Bugs
2. Unit Testing.