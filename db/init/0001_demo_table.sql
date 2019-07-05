-- Pull the information from the environment variables
\set username `echo $USER_NAME`
\set db `echo $USER_DB`

\c :db :username

BEGIN;
CREATE TABLE "vendor" (
    "id" serial NOT NULL PRIMARY KEY,
    "created_at" timestamp with time zone NOT NULL,
    "code" varchar(64) NOT NULL,
    "name" varchar(128)
);

CREATE TABLE "device" (
    "id" serial NOT NULL PRIMARY KEY,
    "created_at" timestamp with time zone NOT NULL,
    "code" varchar(64) NOT NULL,
    "name" varchar(128),
    "vendor_id" integer NOT NULL REFERENCES "vendor" ("id") DEFERRABLE INITIALLY DEFERRED

);
COMMIT;

