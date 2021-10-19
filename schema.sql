DROP DATABASE IF EXISTS promofeeds;

CREATE DATABASE promofeeds;

\c promofeeds;

CREATE TABLE IF NOT EXISTS PartnerMRSS (
  feedid SERIAL,
  createdDate DATE,
  feedURL VARCHAR,
  isActive INT,
  trackingGroup INT PRIMARY KEY,
  updatedDate DATE 
);

