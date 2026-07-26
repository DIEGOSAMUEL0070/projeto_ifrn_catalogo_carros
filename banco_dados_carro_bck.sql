--
-- PostgreSQL database dump
--

\restrict 0DX1vMRgLAAsLDyma7sUkirVT6SbKaSB68Z7fdB89aKoP6KFViLwWQSSsuaUr4T

-- Dumped from database version 18.4
-- Dumped by pg_dump version 18.4

-- Started on 2026-07-26 18:54:58

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
-- TOC entry 219 (class 1259 OID 16510)
-- Name: anos; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.anos (
    id integer NOT NULL,
    ano integer NOT NULL
);


ALTER TABLE public.anos OWNER TO postgres;

--
-- TOC entry 220 (class 1259 OID 16515)
-- Name: anos_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.anos_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.anos_id_seq OWNER TO postgres;

--
-- TOC entry 5088 (class 0 OID 0)
-- Dependencies: 220
-- Name: anos_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.anos_id_seq OWNED BY public.anos.id;


--
-- TOC entry 221 (class 1259 OID 16516)
-- Name: cambios; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.cambios (
    id integer NOT NULL,
    nome character varying(50) NOT NULL
);


ALTER TABLE public.cambios OWNER TO postgres;

--
-- TOC entry 222 (class 1259 OID 16521)
-- Name: cambios_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.cambios_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.cambios_id_seq OWNER TO postgres;

--
-- TOC entry 5089 (class 0 OID 0)
-- Dependencies: 222
-- Name: cambios_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.cambios_id_seq OWNED BY public.cambios.id;


--
-- TOC entry 223 (class 1259 OID 16522)
-- Name: carros; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.carros (
    id character varying(36) NOT NULL,
    modelo character varying(100) NOT NULL,
    ano_id integer,
    preco numeric(10,2) NOT NULL,
    marca_id integer,
    cor_id integer,
    tipo_cambio_id integer,
    tipo_combustivel_id integer,
    usuario_id integer
);


ALTER TABLE public.carros OWNER TO postgres;

--
-- TOC entry 224 (class 1259 OID 16528)
-- Name: combustiveis; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.combustiveis (
    id integer NOT NULL,
    nome character varying(50) NOT NULL
);


ALTER TABLE public.combustiveis OWNER TO postgres;

--
-- TOC entry 225 (class 1259 OID 16533)
-- Name: combustiveis_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.combustiveis_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.combustiveis_id_seq OWNER TO postgres;

--
-- TOC entry 5090 (class 0 OID 0)
-- Dependencies: 225
-- Name: combustiveis_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.combustiveis_id_seq OWNED BY public.combustiveis.id;


--
-- TOC entry 226 (class 1259 OID 16534)
-- Name: cores; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.cores (
    id integer NOT NULL,
    nome character varying(50) NOT NULL
);


ALTER TABLE public.cores OWNER TO postgres;

--
-- TOC entry 227 (class 1259 OID 16539)
-- Name: cores_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.cores_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.cores_id_seq OWNER TO postgres;

--
-- TOC entry 5091 (class 0 OID 0)
-- Dependencies: 227
-- Name: cores_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.cores_id_seq OWNED BY public.cores.id;


--
-- TOC entry 228 (class 1259 OID 16540)
-- Name: marcas; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.marcas (
    id integer NOT NULL,
    nome character varying(100) NOT NULL
);


ALTER TABLE public.marcas OWNER TO postgres;

--
-- TOC entry 229 (class 1259 OID 16545)
-- Name: marcas_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.marcas_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.marcas_id_seq OWNER TO postgres;

--
-- TOC entry 5092 (class 0 OID 0)
-- Dependencies: 229
-- Name: marcas_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.marcas_id_seq OWNED BY public.marcas.id;


--
-- TOC entry 230 (class 1259 OID 16546)
-- Name: usuarios; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.usuarios (
    id integer NOT NULL,
    email character varying(150) NOT NULL,
    senha character varying(255) NOT NULL,
    nome character varying(100) NOT NULL
);


ALTER TABLE public.usuarios OWNER TO postgres;

--
-- TOC entry 231 (class 1259 OID 16555)
-- Name: usuarios_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.usuarios_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.usuarios_id_seq OWNER TO postgres;

--
-- TOC entry 5093 (class 0 OID 0)
-- Dependencies: 231
-- Name: usuarios_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.usuarios_id_seq OWNED BY public.usuarios.id;


--
-- TOC entry 4885 (class 2604 OID 16556)
-- Name: anos id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.anos ALTER COLUMN id SET DEFAULT nextval('public.anos_id_seq'::regclass);


--
-- TOC entry 4886 (class 2604 OID 16557)
-- Name: cambios id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cambios ALTER COLUMN id SET DEFAULT nextval('public.cambios_id_seq'::regclass);


--
-- TOC entry 4887 (class 2604 OID 16558)
-- Name: combustiveis id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.combustiveis ALTER COLUMN id SET DEFAULT nextval('public.combustiveis_id_seq'::regclass);


--
-- TOC entry 4888 (class 2604 OID 16559)
-- Name: cores id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cores ALTER COLUMN id SET DEFAULT nextval('public.cores_id_seq'::regclass);


--
-- TOC entry 4889 (class 2604 OID 16560)
-- Name: marcas id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.marcas ALTER COLUMN id SET DEFAULT nextval('public.marcas_id_seq'::regclass);


--
-- TOC entry 4890 (class 2604 OID 16561)
-- Name: usuarios id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuarios ALTER COLUMN id SET DEFAULT nextval('public.usuarios_id_seq'::regclass);


--
-- TOC entry 5070 (class 0 OID 16510)
-- Dependencies: 219
-- Data for Name: anos; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.anos (id, ano) FROM stdin;
1	2001
2	2002
3	2003
4	2004
5	2005
6	2006
7	2007
8	2008
9	2009
10	2010
11	2011
12	2012
13	2013
14	2014
15	2015
16	2016
17	2017
18	2018
19	2019
20	2020
21	2021
22	2022
23	2023
24	2024
25	2025
26	2026
\.


--
-- TOC entry 5072 (class 0 OID 16516)
-- Dependencies: 221
-- Data for Name: cambios; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.cambios (id, nome) FROM stdin;
1	Manual
2	Automático
\.


--
-- TOC entry 5074 (class 0 OID 16522)
-- Dependencies: 223
-- Data for Name: carros; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.carros (id, modelo, ano_id, preco, marca_id, cor_id, tipo_cambio_id, tipo_combustivel_id, usuario_id) FROM stdin;
\.


--
-- TOC entry 5075 (class 0 OID 16528)
-- Dependencies: 224
-- Data for Name: combustiveis; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.combustiveis (id, nome) FROM stdin;
1	Gasolina
2	Etanol
3	Diesel
4	Híbrido
5	Elétrico
\.


--
-- TOC entry 5077 (class 0 OID 16534)
-- Dependencies: 226
-- Data for Name: cores; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.cores (id, nome) FROM stdin;
1	Branco
2	Preto
3	Prata
4	Cinza
5	Vermelho
\.


--
-- TOC entry 5079 (class 0 OID 16540)
-- Dependencies: 228
-- Data for Name: marcas; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.marcas (id, nome) FROM stdin;
1	Chevrolet
2	Fiat
3	Ford
4	Hyundai
5	Toyota
6	Volkswagen
7	Ferrari
\.


--
-- TOC entry 5081 (class 0 OID 16546)
-- Dependencies: 230
-- Data for Name: usuarios; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.usuarios (id, email, senha, nome) FROM stdin;
\.


--
-- TOC entry 5094 (class 0 OID 0)
-- Dependencies: 220
-- Name: anos_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.anos_id_seq', 1040, true);


--
-- TOC entry 5095 (class 0 OID 0)
-- Dependencies: 222
-- Name: cambios_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.cambios_id_seq', 2, true);


--
-- TOC entry 5096 (class 0 OID 0)
-- Dependencies: 225
-- Name: combustiveis_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.combustiveis_id_seq', 5, true);


--
-- TOC entry 5097 (class 0 OID 0)
-- Dependencies: 227
-- Name: cores_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.cores_id_seq', 5, true);


--
-- TOC entry 5098 (class 0 OID 0)
-- Dependencies: 229
-- Name: marcas_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.marcas_id_seq', 7, true);


--
-- TOC entry 5099 (class 0 OID 0)
-- Dependencies: 231
-- Name: usuarios_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.usuarios_id_seq', 1, true);


--
-- TOC entry 4892 (class 2606 OID 16563)
-- Name: anos anos_ano_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.anos
    ADD CONSTRAINT anos_ano_key UNIQUE (ano);


--
-- TOC entry 4894 (class 2606 OID 16565)
-- Name: anos anos_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.anos
    ADD CONSTRAINT anos_pkey PRIMARY KEY (id);


--
-- TOC entry 4896 (class 2606 OID 16567)
-- Name: cambios cambios_nome_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cambios
    ADD CONSTRAINT cambios_nome_key UNIQUE (nome);


--
-- TOC entry 4898 (class 2606 OID 16569)
-- Name: cambios cambios_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cambios
    ADD CONSTRAINT cambios_pkey PRIMARY KEY (id);


--
-- TOC entry 4900 (class 2606 OID 16571)
-- Name: carros carros_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.carros
    ADD CONSTRAINT carros_pkey PRIMARY KEY (id);


--
-- TOC entry 4902 (class 2606 OID 16573)
-- Name: combustiveis combustiveis_nome_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.combustiveis
    ADD CONSTRAINT combustiveis_nome_key UNIQUE (nome);


--
-- TOC entry 4904 (class 2606 OID 16575)
-- Name: combustiveis combustiveis_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.combustiveis
    ADD CONSTRAINT combustiveis_pkey PRIMARY KEY (id);


--
-- TOC entry 4906 (class 2606 OID 16577)
-- Name: cores cores_nome_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cores
    ADD CONSTRAINT cores_nome_key UNIQUE (nome);


--
-- TOC entry 4908 (class 2606 OID 16579)
-- Name: cores cores_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cores
    ADD CONSTRAINT cores_pkey PRIMARY KEY (id);


--
-- TOC entry 4910 (class 2606 OID 16581)
-- Name: marcas marcas_nome_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.marcas
    ADD CONSTRAINT marcas_nome_key UNIQUE (nome);


--
-- TOC entry 4912 (class 2606 OID 16583)
-- Name: marcas marcas_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.marcas
    ADD CONSTRAINT marcas_pkey PRIMARY KEY (id);


--
-- TOC entry 4914 (class 2606 OID 16585)
-- Name: usuarios usuarios_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT usuarios_email_key UNIQUE (email);


--
-- TOC entry 4916 (class 2606 OID 16587)
-- Name: usuarios usuarios_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT usuarios_pkey PRIMARY KEY (id);


--
-- TOC entry 4917 (class 2606 OID 16588)
-- Name: carros carros_ano_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.carros
    ADD CONSTRAINT carros_ano_id_fkey FOREIGN KEY (ano_id) REFERENCES public.anos(id) ON DELETE SET NULL;


--
-- TOC entry 4918 (class 2606 OID 16593)
-- Name: carros carros_cor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.carros
    ADD CONSTRAINT carros_cor_id_fkey FOREIGN KEY (cor_id) REFERENCES public.cores(id) ON DELETE SET NULL;


--
-- TOC entry 4919 (class 2606 OID 16598)
-- Name: carros carros_marca_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.carros
    ADD CONSTRAINT carros_marca_id_fkey FOREIGN KEY (marca_id) REFERENCES public.marcas(id) ON DELETE SET NULL;


--
-- TOC entry 4920 (class 2606 OID 16603)
-- Name: carros carros_tipo_cambio_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.carros
    ADD CONSTRAINT carros_tipo_cambio_id_fkey FOREIGN KEY (tipo_cambio_id) REFERENCES public.cambios(id) ON DELETE SET NULL;


--
-- TOC entry 4921 (class 2606 OID 16608)
-- Name: carros carros_tipo_combustivel_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.carros
    ADD CONSTRAINT carros_tipo_combustivel_id_fkey FOREIGN KEY (tipo_combustivel_id) REFERENCES public.combustiveis(id) ON DELETE SET NULL;


--
-- TOC entry 4922 (class 2606 OID 16613)
-- Name: carros carros_usuario_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.carros
    ADD CONSTRAINT carros_usuario_id_fkey FOREIGN KEY (usuario_id) REFERENCES public.usuarios(id) ON DELETE SET NULL;


-- Completed on 2026-07-26 18:54:58

--
-- PostgreSQL database dump complete
--

\unrestrict 0DX1vMRgLAAsLDyma7sUkirVT6SbKaSB68Z7fdB89aKoP6KFViLwWQSSsuaUr4T

