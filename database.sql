DROP TABLE IF EXISTS urls;
DROP TABLE IF EXISTS url_checks;

CREATE TABLE urls (
  id SERIAL PRIMARY KEY,
  name TEXT UNIQUE NOT NULL,
  created_at DATE NOT NULL
);

CREATE TABLE url_checks (
  id SERIAL PRIMARY KEY,
  url_id INTEGER NOT NULL REFERENCES urls (id),
  status_code INTEGER NOT NULL,
  h1 TEXT,
  title TEXT,
  description TEXT,
  created_at DATE NOT NULL
);