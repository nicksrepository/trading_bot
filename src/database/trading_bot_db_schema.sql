--
-- PostgreSQL database dump
--

-- Dumped from database version 16.4
-- Dumped by pg_dump version 16.4

-- Started on 2024-08-27 14:11:36

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
-- TOC entry 226 (class 1259 OID 16757)
-- Name: analytics_results; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.analytics_results (
    id integer NOT NULL,
    ticker_id_1 integer,
    ticker_id_2 integer,
    correlation numeric,
    "timestamp" timestamp without time zone
);


ALTER TABLE public.analytics_results OWNER TO postgres;

--
-- TOC entry 225 (class 1259 OID 16756)
-- Name: analytics_results_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.analytics_results_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.analytics_results_id_seq OWNER TO postgres;

--
-- TOC entry 4923 (class 0 OID 0)
-- Dependencies: 225
-- Name: analytics_results_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.analytics_results_id_seq OWNED BY public.analytics_results.id;


--
-- TOC entry 228 (class 1259 OID 16776)
-- Name: data_cleaning_logs; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.data_cleaning_logs (
    id integer NOT NULL,
    table_name character varying(255),
    cleaned_on timestamp without time zone,
    issues_found text,
    issues_resolved text
);


ALTER TABLE public.data_cleaning_logs OWNER TO postgres;

--
-- TOC entry 227 (class 1259 OID 16775)
-- Name: data_cleaning_logs_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.data_cleaning_logs_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.data_cleaning_logs_id_seq OWNER TO postgres;

--
-- TOC entry 4924 (class 0 OID 0)
-- Dependencies: 227
-- Name: data_cleaning_logs_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.data_cleaning_logs_id_seq OWNED BY public.data_cleaning_logs.id;


--
-- TOC entry 222 (class 1259 OID 16725)
-- Name: financials; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.financials (
    id integer NOT NULL,
    ticker_id integer,
    period character varying(10),
    report_date date,
    revenue numeric,
    net_income numeric,
    earnings_per_share numeric
);


ALTER TABLE public.financials OWNER TO postgres;

--
-- TOC entry 221 (class 1259 OID 16724)
-- Name: financials_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.financials_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.financials_id_seq OWNER TO postgres;

--
-- TOC entry 4925 (class 0 OID 0)
-- Dependencies: 221
-- Name: financials_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.financials_id_seq OWNED BY public.financials.id;


--
-- TOC entry 218 (class 1259 OID 16695)
-- Name: historical_data; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.historical_data (
    id integer NOT NULL,
    ticker_id integer,
    date date NOT NULL,
    open numeric,
    high numeric,
    low numeric,
    close numeric,
    adjusted_close numeric,
    volume bigint
);


ALTER TABLE public.historical_data OWNER TO postgres;

--
-- TOC entry 217 (class 1259 OID 16694)
-- Name: historical_data_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.historical_data_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.historical_data_id_seq OWNER TO postgres;

--
-- TOC entry 4926 (class 0 OID 0)
-- Dependencies: 217
-- Name: historical_data_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.historical_data_id_seq OWNED BY public.historical_data.id;


--
-- TOC entry 224 (class 1259 OID 16741)
-- Name: intraday_data; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.intraday_data (
    id integer NOT NULL,
    ticker_id integer,
    "timestamp" timestamp without time zone NOT NULL,
    open numeric,
    high numeric,
    low numeric,
    close numeric,
    volume bigint
);


ALTER TABLE public.intraday_data OWNER TO postgres;

--
-- TOC entry 223 (class 1259 OID 16740)
-- Name: intraday_data_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.intraday_data_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.intraday_data_id_seq OWNER TO postgres;

--
-- TOC entry 4927 (class 0 OID 0)
-- Dependencies: 223
-- Name: intraday_data_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.intraday_data_id_seq OWNED BY public.intraday_data.id;


--
-- TOC entry 229 (class 1259 OID 16791)
-- Name: minute_data; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.minute_data (
    ticker_id integer NOT NULL,
    "timestamp" timestamp with time zone NOT NULL,
    open numeric,
    high numeric,
    low numeric,
    close numeric,
    volume bigint
);


ALTER TABLE public.minute_data OWNER TO postgres;

--
-- TOC entry 220 (class 1259 OID 16711)
-- Name: news_events; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.news_events (
    id integer NOT NULL,
    ticker_id integer,
    event_date timestamp without time zone,
    event_type character varying(255),
    description text,
    source character varying(255)
);


ALTER TABLE public.news_events OWNER TO postgres;

--
-- TOC entry 219 (class 1259 OID 16710)
-- Name: news_events_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.news_events_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.news_events_id_seq OWNER TO postgres;

--
-- TOC entry 4928 (class 0 OID 0)
-- Dependencies: 219
-- Name: news_events_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.news_events_id_seq OWNED BY public.news_events.id;


--
-- TOC entry 216 (class 1259 OID 16684)
-- Name: tickers; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tickers (
    ticker_id integer NOT NULL,
    symbol character varying(10) NOT NULL,
    name character varying(255),
    sector character varying(255),
    industry character varying(255)
);


ALTER TABLE public.tickers OWNER TO postgres;

--
-- TOC entry 215 (class 1259 OID 16683)
-- Name: tickers_ticker_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.tickers_ticker_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.tickers_ticker_id_seq OWNER TO postgres;

--
-- TOC entry 4929 (class 0 OID 0)
-- Dependencies: 215
-- Name: tickers_ticker_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.tickers_ticker_id_seq OWNED BY public.tickers.ticker_id;


--
-- TOC entry 4727 (class 2604 OID 16760)
-- Name: analytics_results id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.analytics_results ALTER COLUMN id SET DEFAULT nextval('public.analytics_results_id_seq'::regclass);


--
-- TOC entry 4728 (class 2604 OID 16779)
-- Name: data_cleaning_logs id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.data_cleaning_logs ALTER COLUMN id SET DEFAULT nextval('public.data_cleaning_logs_id_seq'::regclass);


--
-- TOC entry 4725 (class 2604 OID 16728)
-- Name: financials id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.financials ALTER COLUMN id SET DEFAULT nextval('public.financials_id_seq'::regclass);


--
-- TOC entry 4723 (class 2604 OID 16698)
-- Name: historical_data id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.historical_data ALTER COLUMN id SET DEFAULT nextval('public.historical_data_id_seq'::regclass);


--
-- TOC entry 4726 (class 2604 OID 16744)
-- Name: intraday_data id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.intraday_data ALTER COLUMN id SET DEFAULT nextval('public.intraday_data_id_seq'::regclass);


--
-- TOC entry 4724 (class 2604 OID 16714)
-- Name: news_events id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.news_events ALTER COLUMN id SET DEFAULT nextval('public.news_events_id_seq'::regclass);


--
-- TOC entry 4722 (class 2604 OID 16687)
-- Name: tickers ticker_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tickers ALTER COLUMN ticker_id SET DEFAULT nextval('public.tickers_ticker_id_seq'::regclass);


--
-- TOC entry 4748 (class 2606 OID 16764)
-- Name: analytics_results analytics_results_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.analytics_results
    ADD CONSTRAINT analytics_results_pkey PRIMARY KEY (id);


--
-- TOC entry 4750 (class 2606 OID 16783)
-- Name: data_cleaning_logs data_cleaning_logs_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.data_cleaning_logs
    ADD CONSTRAINT data_cleaning_logs_pkey PRIMARY KEY (id);


--
-- TOC entry 4740 (class 2606 OID 16732)
-- Name: financials financials_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.financials
    ADD CONSTRAINT financials_pkey PRIMARY KEY (id);


--
-- TOC entry 4742 (class 2606 OID 16734)
-- Name: financials financials_ticker_id_report_date_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.financials
    ADD CONSTRAINT financials_ticker_id_report_date_key UNIQUE (ticker_id, report_date);


--
-- TOC entry 4734 (class 2606 OID 16702)
-- Name: historical_data historical_data_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.historical_data
    ADD CONSTRAINT historical_data_pkey PRIMARY KEY (id);


--
-- TOC entry 4736 (class 2606 OID 16704)
-- Name: historical_data historical_data_ticker_id_date_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.historical_data
    ADD CONSTRAINT historical_data_ticker_id_date_key UNIQUE (ticker_id, date);


--
-- TOC entry 4744 (class 2606 OID 16748)
-- Name: intraday_data intraday_data_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.intraday_data
    ADD CONSTRAINT intraday_data_pkey PRIMARY KEY (id);


--
-- TOC entry 4746 (class 2606 OID 16750)
-- Name: intraday_data intraday_data_ticker_id_timestamp_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.intraday_data
    ADD CONSTRAINT intraday_data_ticker_id_timestamp_key UNIQUE (ticker_id, "timestamp");


--
-- TOC entry 4752 (class 2606 OID 16797)
-- Name: minute_data minute_data_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.minute_data
    ADD CONSTRAINT minute_data_pkey PRIMARY KEY (ticker_id, "timestamp");


--
-- TOC entry 4738 (class 2606 OID 16718)
-- Name: news_events news_events_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.news_events
    ADD CONSTRAINT news_events_pkey PRIMARY KEY (id);


--
-- TOC entry 4730 (class 2606 OID 16691)
-- Name: tickers tickers_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tickers
    ADD CONSTRAINT tickers_pkey PRIMARY KEY (ticker_id);


--
-- TOC entry 4732 (class 2606 OID 16693)
-- Name: tickers tickers_symbol_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tickers
    ADD CONSTRAINT tickers_symbol_key UNIQUE (symbol);


--
-- TOC entry 4757 (class 2606 OID 16765)
-- Name: analytics_results analytics_results_ticker_id_1_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.analytics_results
    ADD CONSTRAINT analytics_results_ticker_id_1_fkey FOREIGN KEY (ticker_id_1) REFERENCES public.tickers(ticker_id);


--
-- TOC entry 4758 (class 2606 OID 16770)
-- Name: analytics_results analytics_results_ticker_id_2_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.analytics_results
    ADD CONSTRAINT analytics_results_ticker_id_2_fkey FOREIGN KEY (ticker_id_2) REFERENCES public.tickers(ticker_id);


--
-- TOC entry 4755 (class 2606 OID 16735)
-- Name: financials financials_ticker_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.financials
    ADD CONSTRAINT financials_ticker_id_fkey FOREIGN KEY (ticker_id) REFERENCES public.tickers(ticker_id);


--
-- TOC entry 4753 (class 2606 OID 16705)
-- Name: historical_data historical_data_ticker_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.historical_data
    ADD CONSTRAINT historical_data_ticker_id_fkey FOREIGN KEY (ticker_id) REFERENCES public.tickers(ticker_id);


--
-- TOC entry 4756 (class 2606 OID 16751)
-- Name: intraday_data intraday_data_ticker_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.intraday_data
    ADD CONSTRAINT intraday_data_ticker_id_fkey FOREIGN KEY (ticker_id) REFERENCES public.tickers(ticker_id);


--
-- TOC entry 4759 (class 2606 OID 16798)
-- Name: minute_data minute_data_ticker_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.minute_data
    ADD CONSTRAINT minute_data_ticker_id_fkey FOREIGN KEY (ticker_id) REFERENCES public.tickers(ticker_id);


--
-- TOC entry 4754 (class 2606 OID 16719)
-- Name: news_events news_events_ticker_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.news_events
    ADD CONSTRAINT news_events_ticker_id_fkey FOREIGN KEY (ticker_id) REFERENCES public.tickers(ticker_id);


-- Completed on 2024-08-27 14:11:36

--
-- PostgreSQL database dump complete
--

