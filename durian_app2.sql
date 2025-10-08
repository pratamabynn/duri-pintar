--
-- avnadminQL database dump
--

-- Dumped from database version 17.5
-- Dumped by pg_dump version 17.5

-- Started on 2025-10-08 18:10:18

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
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
-- TOC entry 222 (class 1259 OID 16580)
-- Name: scan_buah; Type: TABLE; Schema: public; Owner: avnadmin
--

CREATE TABLE public.scan_buah (
    id_scan integer NOT NULL,
    id_user integer,
    jenis_durian character varying(100),
    tanggal_scan timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.scan_buah OWNER TO avnadmin;

--
-- TOC entry 221 (class 1259 OID 16579)
-- Name: scan_buah_id_scan_seq; Type: SEQUENCE; Schema: public; Owner: avnadmin
--

CREATE SEQUENCE public.scan_buah_id_scan_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.scan_buah_id_scan_seq OWNER TO avnadmin;

--
-- TOC entry 4927 (class 0 OID 0)
-- Dependencies: 221
-- Name: scan_buah_id_scan_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: avnadmin
--

ALTER SEQUENCE public.scan_buah_id_scan_seq OWNED BY public.scan_buah.id_scan;


--
-- TOC entry 220 (class 1259 OID 16567)
-- Name: scan_daun; Type: TABLE; Schema: public; Owner: avnadmin
--

CREATE TABLE public.scan_daun (
    id_scan integer NOT NULL,
    id_user integer,
    hasil_prediksi character varying(100),
    tanggal_scan timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.scan_daun OWNER TO avnadmin;

--
-- TOC entry 219 (class 1259 OID 16566)
-- Name: scan_daun_id_scan_seq; Type: SEQUENCE; Schema: public; Owner: avnadmin
--

CREATE SEQUENCE public.scan_daun_id_scan_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.scan_daun_id_scan_seq OWNER TO avnadmin;

--
-- TOC entry 4929 (class 0 OID 0)
-- Dependencies: 219
-- Name: scan_daun_id_scan_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: avnadmin
--

ALTER SEQUENCE public.scan_daun_id_scan_seq OWNED BY public.scan_daun.id_scan;


--
-- TOC entry 224 (class 1259 OID 16778)
-- Name: scan_history; Type: TABLE; Schema: public; Owner: avnadmin
--

CREATE TABLE public.scan_history (
    id integer NOT NULL,
    scan_type character varying(50) NOT NULL,
    result character varying(100) NOT NULL,
    confidence double precision NOT NULL,
    filename character varying(200) NOT NULL,
    "timestamp" timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL
);


ALTER TABLE public.scan_history OWNER TO avnadmin;

--
-- TOC entry 223 (class 1259 OID 16777)
-- Name: scan_history_id_seq; Type: SEQUENCE; Schema: public; Owner: avnadmin
--

CREATE SEQUENCE public.scan_history_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.scan_history_id_seq OWNER TO avnadmin;

--
-- TOC entry 4931 (class 0 OID 0)
-- Dependencies: 223
-- Name: scan_history_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: avnadmin
--

ALTER SEQUENCE public.scan_history_id_seq OWNED BY public.scan_history.id;


--
-- TOC entry 218 (class 1259 OID 16558)
-- Name: users; Type: TABLE; Schema: public; Owner: avnadmin
--

CREATE TABLE public.users (
    id_user integer NOT NULL,
    nama character varying(100) NOT NULL,
    email character varying(100) NOT NULL,
    password character varying(255)
);


ALTER TABLE public.users OWNER TO avnadmin;

--
-- TOC entry 217 (class 1259 OID 16557)
-- Name: users_id_user_seq; Type: SEQUENCE; Schema: public; Owner: avnadmin
--

CREATE SEQUENCE public.users_id_user_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_id_user_seq OWNER TO avnadmin;

--
-- TOC entry 4934 (class 0 OID 0)
-- Dependencies: 217
-- Name: users_id_user_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: avnadmin
--

ALTER SEQUENCE public.users_id_user_seq OWNED BY public.users.id_user;


--
-- TOC entry 4760 (class 2604 OID 16583)
-- Name: scan_buah id_scan; Type: DEFAULT; Schema: public; Owner: avnadmin
--

ALTER TABLE ONLY public.scan_buah ALTER COLUMN id_scan SET DEFAULT nextval('public.scan_buah_id_scan_seq'::regclass);


--
-- TOC entry 4758 (class 2604 OID 16570)
-- Name: scan_daun id_scan; Type: DEFAULT; Schema: public; Owner: avnadmin
--

ALTER TABLE ONLY public.scan_daun ALTER COLUMN id_scan SET DEFAULT nextval('public.scan_daun_id_scan_seq'::regclass);


--
-- TOC entry 4762 (class 2604 OID 16781)
-- Name: scan_history id; Type: DEFAULT; Schema: public; Owner: avnadmin
--

ALTER TABLE ONLY public.scan_history ALTER COLUMN id SET DEFAULT nextval('public.scan_history_id_seq'::regclass);


--
-- TOC entry 4757 (class 2604 OID 16561)
-- Name: users id_user; Type: DEFAULT; Schema: public; Owner: avnadmin
--

ALTER TABLE ONLY public.users ALTER COLUMN id_user SET DEFAULT nextval('public.users_id_user_seq'::regclass);


--
-- TOC entry 4771 (class 2606 OID 16586)
-- Name: scan_buah scan_buah_pkey; Type: CONSTRAINT; Schema: public; Owner: avnadmin
--

ALTER TABLE ONLY public.scan_buah
    ADD CONSTRAINT scan_buah_pkey PRIMARY KEY (id_scan);


--
-- TOC entry 4769 (class 2606 OID 16573)
-- Name: scan_daun scan_daun_pkey; Type: CONSTRAINT; Schema: public; Owner: avnadmin
--

ALTER TABLE ONLY public.scan_daun
    ADD CONSTRAINT scan_daun_pkey PRIMARY KEY (id_scan);


--
-- TOC entry 4773 (class 2606 OID 16784)
-- Name: scan_history scan_history_pkey; Type: CONSTRAINT; Schema: public; Owner: avnadmin
--

ALTER TABLE ONLY public.scan_history
    ADD CONSTRAINT scan_history_pkey PRIMARY KEY (id);


--
-- TOC entry 4765 (class 2606 OID 16565)
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: avnadmin
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- TOC entry 4767 (class 2606 OID 16563)
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: avnadmin
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id_user);


--
-- TOC entry 4775 (class 2606 OID 16587)
-- Name: scan_buah scan_buah_id_user_fkey; Type: FK CONSTRAINT; Schema: public; Owner: avnadmin
--

ALTER TABLE ONLY public.scan_buah
    ADD CONSTRAINT scan_buah_id_user_fkey FOREIGN KEY (id_user) REFERENCES public.users(id_user);


--
-- TOC entry 4774 (class 2606 OID 16574)
-- Name: scan_daun scan_daun_id_user_fkey; Type: FK CONSTRAINT; Schema: public; Owner: avnadmin
--

ALTER TABLE ONLY public.scan_daun
    ADD CONSTRAINT scan_daun_id_user_fkey FOREIGN KEY (id_user) REFERENCES public.users(id_user);


--
-- TOC entry 4926 (class 0 OID 0)
-- Dependencies: 222
-- Name: TABLE scan_buah; Type: ACL; Schema: public; Owner: avnadmin
--

GRANT ALL ON TABLE public.scan_buah TO durian_user;


--
-- TOC entry 4928 (class 0 OID 0)
-- Dependencies: 220
-- Name: TABLE scan_daun; Type: ACL; Schema: public; Owner: avnadmin
--

GRANT ALL ON TABLE public.scan_daun TO durian_user;


--
-- TOC entry 4930 (class 0 OID 0)
-- Dependencies: 224
-- Name: TABLE scan_history; Type: ACL; Schema: public; Owner: avnadmin
--

GRANT ALL ON TABLE public.scan_history TO durian_user;


--
-- TOC entry 4932 (class 0 OID 0)
-- Dependencies: 223
-- Name: SEQUENCE scan_history_id_seq; Type: ACL; Schema: public; Owner: avnadmin
--

GRANT SELECT,USAGE ON SEQUENCE public.scan_history_id_seq TO durian_user;


--
-- TOC entry 4933 (class 0 OID 0)
-- Dependencies: 218
-- Name: TABLE users; Type: ACL; Schema: public; Owner: avnadmin
--

GRANT ALL ON TABLE public.users TO durian_user;


--
-- TOC entry 4935 (class 0 OID 0)
-- Dependencies: 217
-- Name: SEQUENCE users_id_user_seq; Type: ACL; Schema: public; Owner: avnadmin
--

GRANT ALL ON SEQUENCE public.users_id_user_seq TO durian_user;


-- Completed on 2025-10-08 18:10:18

--
-- avnadminQL database dump complete
--

