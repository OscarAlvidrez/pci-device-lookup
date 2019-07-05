-- Pull the information from the environment variables
\set username `echo $USER_NAME`
\set password `echo \'$USER_PASSWORD\'`
\set db `echo $USER_DB`

-- Creates the  DB and ROLE
CREATE USER :username WITH PASSWORD :password;
CREATE database :db OWNER :username;