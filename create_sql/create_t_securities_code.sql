CREATE TABLE IF NOT EXISTS public.t_securities_code
(
    pk_securities_code character varying(8) COLLATE pg_catalog."default" NOT NULL,
    company_name character varying(90) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT t_securities_code_pkey PRIMARY KEY (pk_securities_code)
)