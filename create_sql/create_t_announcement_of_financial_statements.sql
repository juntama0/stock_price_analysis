CREATE TABLE IF NOT EXISTS public.t_announcement_of_financial_statements
(
    pk_securities_code character varying(8) COLLATE pg_catalog."default" NOT NULL,
    pk_year character varying(4) COLLATE pg_catalog."default" NOT NULL,
    pk_quarterly_settlement character varying(1) COLLATE pg_catalog."default" NOT NULL,
    announcement_of_financial_statements_ymd character varying(8) COLLATE pg_catalog."default" NOT NULL,
    next_day_announcement_of_financial_statements_ymd character varying(8) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT t_announcement_of_financial_statements_pkey PRIMARY KEY (pk_securities_code, pk_year, pk_quarterly_settlement)
)