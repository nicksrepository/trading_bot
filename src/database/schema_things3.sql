-- First, let's add the new columns to the existing financials table
ALTER TABLE public.financials
ADD COLUMN IF NOT EXISTS total_assets numeric,
ADD COLUMN IF NOT EXISTS total_liabilities numeric,
ADD COLUMN IF NOT EXISTS total_equity numeric,
ADD COLUMN IF NOT EXISTS cash_and_cash_equivalents numeric,
ADD COLUMN IF NOT EXISTS total_debt numeric,
ADD COLUMN IF NOT EXISTS operating_income numeric,
ADD COLUMN IF NOT EXISTS gross_profit numeric,
ADD COLUMN IF NOT EXISTS ebitda numeric,
ADD COLUMN IF NOT EXISTS free_cash_flow numeric,
ADD COLUMN IF NOT EXISTS research_and_development numeric,
ADD COLUMN IF NOT EXISTS current_ratio numeric,
ADD COLUMN IF NOT EXISTS debt_to_equity_ratio numeric,
ADD COLUMN IF NOT EXISTS return_on_assets numeric,
ADD COLUMN IF NOT EXISTS return_on_equity numeric,
ADD COLUMN IF NOT EXISTS book_value_per_share numeric;

-- Now, let's update the constraints if they don't already exist
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'financials_pkey') THEN
        ALTER TABLE ONLY public.financials
        ADD CONSTRAINT financials_pkey PRIMARY KEY (id);
    END IF;

    IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'financials_ticker_id_report_date_key') THEN
        ALTER TABLE ONLY public.financials
        ADD CONSTRAINT financials_ticker_id_report_date_key UNIQUE (ticker_id, report_date);
    END IF;

    IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'financials_ticker_id_fkey') THEN
        ALTER TABLE ONLY public.financials
        ADD CONSTRAINT financials_ticker_id_fkey FOREIGN KEY (ticker_id) REFERENCES public.tickers(ticker_id);
    END IF;
END;