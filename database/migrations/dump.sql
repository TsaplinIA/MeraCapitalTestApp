--
-- PostgreSQL database dump
--

-- Dumped from database version 15.3 (Debian 15.3-1.pgdg110+1)
-- Dumped by pg_dump version 15.3 (Debian 15.3-1.pgdg110+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


-- ALTER TABLE public.alembic_version OWNER TO postgres;

--
-- Name: currencies; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.currencies (
    currency_idx uuid DEFAULT gen_random_uuid() NOT NULL,
    ticker character varying(8) NOT NULL,
    index_price_name character varying(32) NOT NULL
);


-- ALTER TABLE public.currencies OWNER TO $(postgres);

--
-- Name: pricestamps; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.pricestamps (
    pricestamp_idx uuid DEFAULT gen_random_uuid() NOT NULL,
    price integer NOT NULL,
    "timestamp" integer NOT NULL,
    currency_idx uuid NOT NULL
);


-- ALTER TABLE public.pricestamps OWNER TO postgres;

--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.alembic_version (version_num) FROM stdin;
fb1811c71ea2
\.


--
-- Data for Name: currencies; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.currencies (currency_idx, ticker, index_price_name) FROM stdin;
530c4e48-d559-4e71-98b8-c207bcba8622	BTC	btc_usd
ea5d1de1-c400-4339-a94e-b69b8d8781c0	ETH	eth_usd
\.


--
-- Data for Name: pricestamps; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.pricestamps (pricestamp_idx, price, "timestamp", currency_idx) FROM stdin;
\.


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: currencies currencies_index_price_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.currencies
    ADD CONSTRAINT currencies_index_price_name_key UNIQUE (index_price_name);


--
-- Name: currencies currencies_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.currencies
    ADD CONSTRAINT currencies_pkey PRIMARY KEY (currency_idx);


--
-- Name: currencies currencies_ticker_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.currencies
    ADD CONSTRAINT currencies_ticker_key UNIQUE (ticker);


--
-- Name: pricestamps pricestamps_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pricestamps
    ADD CONSTRAINT pricestamps_pkey PRIMARY KEY (pricestamp_idx);


--
-- Name: pricestamps pricestamps_currency_idx_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pricestamps
    ADD CONSTRAINT pricestamps_currency_idx_fkey FOREIGN KEY (currency_idx) REFERENCES public.currencies(currency_idx) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

