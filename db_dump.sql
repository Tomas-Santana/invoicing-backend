--
-- PostgreSQL database dump
--

-- Dumped from database version 15.3
-- Dumped by pg_dump version 15.3

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
-- Name: bank; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.bank (
    id_bank integer NOT NULL,
    name character varying(100) NOT NULL
);


ALTER TABLE public.bank OWNER TO postgres;

--
-- Name: banco_id_banco_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.banco_id_banco_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.banco_id_banco_seq OWNER TO postgres;

--
-- Name: banco_id_banco_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.banco_id_banco_seq OWNED BY public.bank.id_bank;


--
-- Name: bank_payment_method; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.bank_payment_method (
    id_bank integer NOT NULL,
    id_method integer NOT NULL
);


ALTER TABLE public.bank_payment_method OWNER TO postgres;

--
-- Name: client; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.client (
    id_cliente integer NOT NULL,
    pid character varying(30),
    dir character varying(100),
    name character varying(50),
    surname character varying(50),
    pid_prefix character varying(2)
);


ALTER TABLE public.client OWNER TO postgres;

--
-- Name: cliente_id_cliente_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.cliente_id_cliente_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.cliente_id_cliente_seq OWNER TO postgres;

--
-- Name: cliente_id_cliente_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.cliente_id_cliente_seq OWNED BY public.client.id_cliente;


--
-- Name: invoice; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.invoice (
    id_invoice integer NOT NULL,
    id_client integer NOT NULL,
    date date NOT NULL,
    void boolean DEFAULT false
);


ALTER TABLE public.invoice OWNER TO postgres;

--
-- Name: factura_id_factura_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.factura_id_factura_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.factura_id_factura_seq OWNER TO postgres;

--
-- Name: factura_id_factura_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.factura_id_factura_seq OWNED BY public.invoice.id_invoice;


--
-- Name: invoice_product; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.invoice_product (
    id_invoice integer NOT NULL,
    code_product character varying(10) NOT NULL,
    quantity integer NOT NULL
);


ALTER TABLE public.invoice_product OWNER TO postgres;

--
-- Name: payment_method; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.payment_method (
    id_method integer NOT NULL,
    name character varying(100) NOT NULL
);


ALTER TABLE public.payment_method OWNER TO postgres;

--
-- Name: metodo_de_pago_id_metodo_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.metodo_de_pago_id_metodo_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.metodo_de_pago_id_metodo_seq OWNER TO postgres;

--
-- Name: metodo_de_pago_id_metodo_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.metodo_de_pago_id_metodo_seq OWNED BY public.payment_method.id_method;


--
-- Name: payment; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.payment (
    id_invoice integer NOT NULL,
    id_bank integer,
    amount real NOT NULL,
    id_method integer NOT NULL
);


ALTER TABLE public.payment OWNER TO postgres;

--
-- Name: product; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.product (
    code character varying(10) NOT NULL,
    name character varying(100) NOT NULL,
    price real NOT NULL,
    photourl character varying(200)
);


ALTER TABLE public.product OWNER TO postgres;

--
-- Name: producto_id_producto_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.producto_id_producto_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.producto_id_producto_seq OWNER TO postgres;

--
-- Name: producto_id_producto_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.producto_id_producto_seq OWNED BY public.product.code;


--
-- Name: bank id_bank; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.bank ALTER COLUMN id_bank SET DEFAULT nextval('public.banco_id_banco_seq'::regclass);


--
-- Name: client id_cliente; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.client ALTER COLUMN id_cliente SET DEFAULT nextval('public.cliente_id_cliente_seq'::regclass);


--
-- Name: invoice id_invoice; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.invoice ALTER COLUMN id_invoice SET DEFAULT nextval('public.factura_id_factura_seq'::regclass);


--
-- Name: payment_method id_method; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.payment_method ALTER COLUMN id_method SET DEFAULT nextval('public.metodo_de_pago_id_metodo_seq'::regclass);


--
-- Name: product code; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.product ALTER COLUMN code SET DEFAULT nextval('public.producto_id_producto_seq'::regclass);


--
-- Data for Name: bank; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.bank (id_bank, name) FROM stdin;
1	BANESCO
2	BNC
3	VENEZUELA
4	BOFA
5	CHASE
\.


--
-- Data for Name: bank_payment_method; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.bank_payment_method (id_bank, id_method) FROM stdin;
\.


--
-- Data for Name: client; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.client (id_cliente, pid, dir, name, surname, pid_prefix) FROM stdin;
4	1	Panteon Nacional	Simon	Bolivar	V
3	30604530	La Lago	Tomas	Santana	V
1	7902245	La Lago	Miguel	Santana	V
2	27491472	La Lago	Erika	Santana	V
\.


--
-- Data for Name: invoice; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.invoice (id_invoice, id_client, date, void) FROM stdin;
2	1	2024-04-10	f
3	1	2024-04-11	f
4	2	2024-04-10	f
5	2	2024-04-11	f
6	3	2024-04-09	f
7	3	2024-04-11	f
8	4	2024-04-09	f
9	4	2024-04-11	f
\.


--
-- Data for Name: invoice_product; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.invoice_product (id_invoice, code_product, quantity) FROM stdin;
2	12345	2
2	09876	1
3	13579	1
3	24680	2
4	54321	2
4	67890	3
5	09876	5
6	12345	10
7	54321	2
7	67890	1
8	24680	5
9	09876	5
9	24680	1
9	12345	12
\.


--
-- Data for Name: payment; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.payment (id_invoice, id_bank, amount, id_method) FROM stdin;
2	4	11	4
3	1	50	1
3	\N	20	3
2	2	1.1	2
3	3	7	2
4	5	80	4
4	1	12.4	1
5	\N	38.5	3
6	5	22	4
7	2	48.4	1
8	3	137.5	2
9	2	60.4	1
9	2	32	2
\.


--
-- Data for Name: payment_method; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.payment_method (id_method, name) FROM stdin;
1	TARJETA DE CREDITO
2	TARJETA DE DEBITO
3	EFECTIVO
4	ZELLE
\.


--
-- Data for Name: product; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.product (code, name, price, photourl) FROM stdin;
12345	TENEDOR	2	https://m.media-amazon.com/images/I/61U4tatR8HL._AC_UF894,1000_QL80_.jpg
67890	SILLA	20	https://m.media-amazon.com/images/I/81pVe8Dl7KS.jpg
13579	VELA AROMATICA	20	https://m.media-amazon.com/images/I/612sOIz0HEL._UF1000,1000_QL80_.jpg
24680	LAMPARA	25	https://m.media-amazon.com/images/I/61uLmGqbcVL._AC_UF894,1000_QL80_.jpg
54321	BOLIGRAFOS	12	https://m.media-amazon.com/images/I/81y314kpUsL.jpg
09876	TAZA	7	https://m.media-amazon.com/images/I/71YF9K8XvFL._AC_UF894,1000_QL80_.jpg
\.


--
-- Name: banco_id_banco_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.banco_id_banco_seq', 5, true);


--
-- Name: cliente_id_cliente_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.cliente_id_cliente_seq', 4, true);


--
-- Name: factura_id_factura_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.factura_id_factura_seq', 9, true);


--
-- Name: metodo_de_pago_id_metodo_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.metodo_de_pago_id_metodo_seq', 4, true);


--
-- Name: producto_id_producto_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.producto_id_producto_seq', 6, true);


--
-- Name: bank pk_banco; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.bank
    ADD CONSTRAINT pk_banco PRIMARY KEY (id_bank);


--
-- Name: client pk_cliente; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.client
    ADD CONSTRAINT pk_cliente PRIMARY KEY (id_cliente);


--
-- Name: invoice pk_factura; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.invoice
    ADD CONSTRAINT pk_factura PRIMARY KEY (id_invoice);


--
-- Name: payment_method pk_metodo_de_pago; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.payment_method
    ADD CONSTRAINT pk_metodo_de_pago PRIMARY KEY (id_method);


--
-- Name: product pk_producto; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.product
    ADD CONSTRAINT pk_producto PRIMARY KEY (code);


--
-- Name: bank_payment_method fk_banco_metodo_banco; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.bank_payment_method
    ADD CONSTRAINT fk_banco_metodo_banco FOREIGN KEY (id_bank) REFERENCES public.bank(id_bank);


--
-- Name: bank_payment_method fk_banco_metodo_metodo_de_pago; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.bank_payment_method
    ADD CONSTRAINT fk_banco_metodo_metodo_de_pago FOREIGN KEY (id_method) REFERENCES public.payment_method(id_method);


--
-- Name: invoice fk_factura_cliente; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.invoice
    ADD CONSTRAINT fk_factura_cliente FOREIGN KEY (id_client) REFERENCES public.client(id_cliente);


--
-- Name: payment fk_factura_pago_banco; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.payment
    ADD CONSTRAINT fk_factura_pago_banco FOREIGN KEY (id_bank) REFERENCES public.bank(id_bank);


--
-- Name: payment fk_factura_pago_factura; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.payment
    ADD CONSTRAINT fk_factura_pago_factura FOREIGN KEY (id_invoice) REFERENCES public.invoice(id_invoice) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: payment fk_factura_pago_metodo_de_pago; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.payment
    ADD CONSTRAINT fk_factura_pago_metodo_de_pago FOREIGN KEY (id_method) REFERENCES public.payment_method(id_method);


--
-- Name: invoice_product fk_factura_producto_factura; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.invoice_product
    ADD CONSTRAINT fk_factura_producto_factura FOREIGN KEY (id_invoice) REFERENCES public.invoice(id_invoice) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: invoice_product fk_factura_producto_producto; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.invoice_product
    ADD CONSTRAINT fk_factura_producto_producto FOREIGN KEY (code_product) REFERENCES public.product(code);


--
-- PostgreSQL database dump complete
--

