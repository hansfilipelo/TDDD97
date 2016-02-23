-- Creator:       MySQL Workbench 6.3.5/ExportSQLite Plugin 0.1.0
-- Author:        Hans-Filip Elo
-- Caption:       New Model
-- Project:       Name of the project
-- Changed:       2016-02-23 14:36
-- Created:       2016-02-20 09:12
PRAGMA foreign_keys = OFF;

-- Schema: database
ATTACH "database.sdb" AS "database";
BEGIN;
CREATE TABLE "database"."countries"(
  "idcountries" INTEGER PRIMARY KEY NOT NULL,
  "name" VARCHAR(45) NOT NULL
);
CREATE TABLE "database"."cities"(
  "idcities" INTEGER PRIMARY KEY NOT NULL,
  "name" VARCHAR(45),
  "country" INTEGER,
  CONSTRAINT "fk_cities_countres"
    FOREIGN KEY("country")
    REFERENCES "countries"("idcountries")
);
CREATE INDEX "database"."cities.fk_cities_countres_idx" ON "cities" ("country");
CREATE TABLE "database"."users"(
  "idusers" INTEGER PRIMARY KEY NOT NULL,
  "email" VARCHAR(45) NOT NULL,
  "passwordHash" VARCHAR(45) NOT NULL,
  "firstname" VARCHAR(45) NOT NULL,
  "familyName" VARCHAR(45) NOT NULL,
  "gender" INTEGER NOT NULL,
  "city" INTEGER NOT NULL,
  "salt" VARCHAR(45) NOT NULL,
  CONSTRAINT "fk_users_cities"
    FOREIGN KEY("city")
    REFERENCES "cities"("idcities")
);
CREATE INDEX "database"."users.fk_users_cities_idx" ON "users" ("city");
CREATE TABLE "database"."messages"(
  "idmessages" INTEGER PRIMARY KEY NOT NULL,
  "fromUser" INTEGER,
  "toUser" INTEGER,
  "content" VARCHAR(255),
  CONSTRAINT "fk_messages_from_user"
    FOREIGN KEY("fromUser")
    REFERENCES "users"("idusers"),
  CONSTRAINT "fk_messages_to_user"
    FOREIGN KEY("toUser")
    REFERENCES "users"("idusers")
);
CREATE INDEX "database"."messages.fk_messages_to_user_idx" ON "messages" ("toUser");
CREATE INDEX "database"."messages.fk_messages_from_user_idx" ON "messages" ("fromUser");
COMMIT;
