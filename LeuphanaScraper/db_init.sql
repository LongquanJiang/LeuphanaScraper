CREATE USER leuphana WITH PASSWORD 'leuphana';

CREATE DATABASE leuphana WITH OWNER leuphana;

\c leuphana

CREATE SEQUENCE news_id_seq AS integer;

ALTER SEQUENCE news_id_seq OWNER TO leuphana;

CREATE TABLE news (
    id integer PRIMARY KEY NOT NULL DEFAULT nextval('news_id_seq'::regclass),
    title character varying(200) NOT NULL,
    subtitle character varying(200) NOT NULL DEFAULT ''::character varying,
    topic character varying(200) NOT NULL DEFAULT ''::character varying,
    pub_year integer,
    pub_month integer,
    pub_day integer,
    url character varying(500) NOT NULL DEFAULT ''::character varying,
    content character varying(5000) NOT NULL DEFAULT ''::character varying,
    is_deleted boolean NOT NULL DEFAULT false
);

ALTER TABLE news
    ADD CONSTRAINT news_pub_month_lowerbound CHECK (pub_month >= 1),
    ADD CONSTRAINT news_pub_month_upperbound CHECK (pub_month <= 12),
    ADD CONSTRAINT news_pub_day_lowerbound CHECK (pub_month >= 1),
    ADD CONSTRAINT news_pub_day_upperbound CHECK (pub_month <= 31),
    ADD CONSTRAINT news_pub_year_lowerbound CHECK (pub_year >= 0),
    OWNER TO leuphana;

GRANT CONNECT ON DATABASE leuphana TO leuphana;
GRANT SELECT, INSERT, UPDATE, DELETE, TRUNCATE ON ALL TABLES IN SCHEMA public TO leuphana;
GRANT USAGE ON ALL SEQUENCES IN SCHEMA public TO leuphana;