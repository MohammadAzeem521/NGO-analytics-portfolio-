-- ============================================================================
-- NGO ANALYTICS DATABASE — SCHEMA DEFINITION
-- Star Schema: 1 Fact table (donations) + 1 secondary fact (volunteer hours)
--              + 3 Dimension tables (ngo, date, campaign)
-- Author: Mohd Azeem | Teerthanker Mahaveer University
-- ============================================================================
-- NOTE: dim_ngo fields are REAL, research-verified data (official NGO
-- websites). fact_donations, fact_volunteer_hours and dim_campaign contain
-- SYNTHETIC data generated for analytics/portfolio demonstration purposes.
-- ============================================================================

CREATE TABLE dim_ngo (
    ngo_id              TEXT PRIMARY KEY,       -- e.g. NGO01
    ngo_name            TEXT NOT NULL,
    year_founded        INTEGER,
    headquarters_city   TEXT,
    headquarters_state  TEXT,
    organization_type   TEXT,                    -- Trust / Society / Sec.8 Company etc.
    primary_focus_area  TEXT,                     -- Education / Health / Environment etc.
    website             TEXT
);

CREATE TABLE dim_date (
    date_id       INTEGER PRIMARY KEY,            -- YYYYMMDD surrogate key
    date          TEXT,
    year          INTEGER,
    quarter       INTEGER,
    month         INTEGER,
    month_name    TEXT,
    day           INTEGER,
    weekday_name  TEXT,
    is_weekend    INTEGER,                        -- 0/1
    fiscal_year   TEXT                             -- Indian FY format e.g. 2023-24
);

CREATE TABLE dim_campaign (
    campaign_id         TEXT PRIMARY KEY,
    ngo_id              TEXT REFERENCES dim_ngo(ngo_id),
    campaign_name       TEXT,
    channel             TEXT,                      -- Online Portal / Corporate CSR / etc.
    start_date          TEXT,
    end_date            TEXT,
    target_amount_inr   REAL,
    status              TEXT                        -- Completed / Ongoing
);

CREATE TABLE fact_donations (
    donation_id          TEXT PRIMARY KEY,
    ngo_id               TEXT REFERENCES dim_ngo(ngo_id),
    campaign_id          TEXT REFERENCES dim_campaign(campaign_id),
    date_id              INTEGER REFERENCES dim_date(date_id),
    donor_type           TEXT,                     -- Individual / Corporate / Foundation / Government Grant
    payment_mode         TEXT,
    donor_state           TEXT,
    is_recurring          INTEGER,                  -- 0/1
    donation_amount_inr   REAL
);

CREATE TABLE fact_volunteer_hours (
    log_id            TEXT PRIMARY KEY,
    ngo_id            TEXT REFERENCES dim_ngo(ngo_id),
    date_id           INTEGER REFERENCES dim_date(date_id),
    volunteer_count   INTEGER,
    hours_logged      INTEGER,
    activity_type     TEXT
);

-- Indexes for join/filter performance
CREATE INDEX idx_fact_donations_ngo      ON fact_donations(ngo_id);
CREATE INDEX idx_fact_donations_date     ON fact_donations(date_id);
CREATE INDEX idx_fact_donations_campaign ON fact_donations(campaign_id);
CREATE INDEX idx_fact_volunteer_ngo      ON fact_volunteer_hours(ngo_id);
CREATE INDEX idx_campaign_ngo            ON dim_campaign(ngo_id);

