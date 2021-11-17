# mysql-bulk-create-users
Small tool for tired DBAs.

Create users (with random strong password), grant all privileges on their databases (create database if need).
Also support very old syntax of MySQL <=5.5, Mariadb <=10.1

Input:
+ MySQL Credential files: .my.cnf (as sample)
+ User List: userList. Each rows is a username (as sample)
+ Privileges List: privList.csv .CSV file, each rows is a username,database pair. (as sample)

Output:
+ Print username & password (as json)
+ List of granted databases for users.
