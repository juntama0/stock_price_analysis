CREATE TABLE IF NOT EXISTS public.t_announcement_of_financial_statements_stock_price
(
    pk_securities_code character varying(8) COLLATE pg_catalog."default" NOT NULL,
    pk_year character varying(4) COLLATE pg_catalog."default" NOT NULL,
    pk_quarterly_settlement character varying(1) COLLATE pg_catalog."default" NOT NULL,
    stock_price numeric,
    next_day_stock_price numeric,
    growth_rate numeric,
    deviation_rate_average_stock_price_25 numeric,
    CONSTRAINT t_announcement_of_financial_statements_stock_price_pkey PRIMARY KEY (pk_securities_code, pk_year, pk_quarterly_settlement)
)