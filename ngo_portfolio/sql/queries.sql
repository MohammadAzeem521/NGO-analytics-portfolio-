-- ============================================================================
-- NGO ANALYTICS — ANALYTICAL SQL QUERIES
-- Author: Mohd Azeem | Teerthanker Mahaveer University
-- Database: sql/ngo_analytics.db (SQLite)
-- ============================================================================

-- --------------------------------------------------------------------------
-- Q1. Total donations & donor count per NGO (basic JOIN + GROUP BY)
-- --------------------------------------------------------------------------
SELECT
    g.ngo_name,
    COUNT(f.donation_id)              AS total_donations,
    ROUND(SUM(f.donation_amount_inr), 2) AS total_amount_inr,
    ROUND(AVG(f.donation_amount_inr), 2) AS avg_donation_inr
FROM fact_donations f
JOIN dim_ngo g ON f.ngo_id = g.ngo_id
GROUP BY g.ngo_name
ORDER BY total_amount_inr DESC;

-- --------------------------------------------------------------------------
-- Q2. Year-over-Year donation growth per NGO (window function: LAG)
-- --------------------------------------------------------------------------
WITH yearly AS (
    SELECT g.ngo_name, d.year, SUM(f.donation_amount_inr) AS yearly_total
    FROM fact_donations f
    JOIN dim_ngo g  ON f.ngo_id  = g.ngo_id
    JOIN dim_date d ON f.date_id = d.date_id
    GROUP BY g.ngo_name, d.year
)
SELECT
    ngo_name, year, yearly_total,
    LAG(yearly_total) OVER (PARTITION BY ngo_name ORDER BY year) AS prev_year_total,
    ROUND(
        100.0 * (yearly_total - LAG(yearly_total) OVER (PARTITION BY ngo_name ORDER BY year))
        / NULLIF(LAG(yearly_total) OVER (PARTITION BY ngo_name ORDER BY year), 0), 2
    ) AS yoy_growth_pct
FROM yearly
ORDER BY ngo_name, year;

-- --------------------------------------------------------------------------
-- Q3. Running (cumulative) donation total per NGO over time (window function)
-- --------------------------------------------------------------------------
SELECT
    g.ngo_name, d.date, f.donation_amount_inr,
    SUM(f.donation_amount_inr) OVER (
        PARTITION BY g.ngo_name ORDER BY d.date
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS running_total_inr
FROM fact_donations f
JOIN dim_ngo g  ON f.ngo_id  = g.ngo_id
JOIN dim_date d ON f.date_id = d.date_id
WHERE g.ngo_name = 'Pratham Education Foundation'
ORDER BY d.date
LIMIT 20;

-- --------------------------------------------------------------------------
-- Q4. Rank NGOs by total donations within each organization type (RANK)
-- --------------------------------------------------------------------------
SELECT * FROM (
    SELECT
        g.organization_type, g.ngo_name,
        SUM(f.donation_amount_inr) AS total_amount_inr,
        RANK() OVER (PARTITION BY g.organization_type ORDER BY SUM(f.donation_amount_inr) DESC) AS rank_in_type
    FROM fact_donations f
    JOIN dim_ngo g ON f.ngo_id = g.ngo_id
    GROUP BY g.organization_type, g.ngo_name
)
ORDER BY organization_type, rank_in_type;

-- --------------------------------------------------------------------------
-- Q5. Donor-type contribution mix (% of total) per NGO
-- --------------------------------------------------------------------------
SELECT
    g.ngo_name, f.donor_type,
    SUM(f.donation_amount_inr) AS amount_inr,
    ROUND(100.0 * SUM(f.donation_amount_inr) /
          SUM(SUM(f.donation_amount_inr)) OVER (PARTITION BY g.ngo_name), 2) AS pct_of_ngo_total
FROM fact_donations f
JOIN dim_ngo g ON f.ngo_id = g.ngo_id
GROUP BY g.ngo_name, f.donor_type
ORDER BY g.ngo_name, pct_of_ngo_total DESC;

-- --------------------------------------------------------------------------
-- Q6. Campaign performance: achievement % vs target (JOIN + subquery)
-- --------------------------------------------------------------------------
SELECT
    c.campaign_name, g.ngo_name, c.target_amount_inr,
    COALESCE(raised.total_raised, 0) AS raised_amount_inr,
    ROUND(100.0 * COALESCE(raised.total_raised, 0) / c.target_amount_inr, 1) AS pct_achieved,
    c.status
FROM dim_campaign c
JOIN dim_ngo g ON c.ngo_id = g.ngo_id
LEFT JOIN (
    SELECT campaign_id, SUM(donation_amount_inr) AS total_raised
    FROM fact_donations
    GROUP BY campaign_id
) raised ON c.campaign_id = raised.campaign_id
ORDER BY pct_achieved DESC
LIMIT 15;

-- --------------------------------------------------------------------------
-- Q7. Monthly donation trend (all NGOs combined) — time series for Power BI
-- --------------------------------------------------------------------------
SELECT
    d.year, d.month, d.month_name,
    COUNT(f.donation_id) AS num_donations,
    ROUND(SUM(f.donation_amount_inr), 2) AS total_amount_inr
FROM fact_donations f
JOIN dim_date d ON f.date_id = d.date_id
GROUP BY d.year, d.month
ORDER BY d.year, d.month;

-- --------------------------------------------------------------------------
-- Q8. Top 5 donor states by total contribution (geographic analysis)
-- --------------------------------------------------------------------------
SELECT
    donor_state,
    COUNT(*) AS num_donations,
    ROUND(SUM(donation_amount_inr), 2) AS total_amount_inr
FROM fact_donations
GROUP BY donor_state
ORDER BY total_amount_inr DESC
LIMIT 5;

-- --------------------------------------------------------------------------
-- Q9. Recurring vs One-Time donor value comparison
-- --------------------------------------------------------------------------
SELECT
    CASE WHEN is_recurring = 1 THEN 'Recurring Donor' ELSE 'One-Time Donor' END AS donor_category,
    COUNT(*) AS num_donations,
    ROUND(AVG(donation_amount_inr), 2) AS avg_donation_inr,
    ROUND(SUM(donation_amount_inr), 2) AS total_amount_inr
FROM fact_donations
GROUP BY is_recurring;

-- --------------------------------------------------------------------------
-- Q10. NGOs whose average donation exceeds the overall average (subquery/HAVING)
-- --------------------------------------------------------------------------
SELECT g.ngo_name, ROUND(AVG(f.donation_amount_inr), 2) AS avg_donation_inr
FROM fact_donations f
JOIN dim_ngo g ON f.ngo_id = g.ngo_id
GROUP BY g.ngo_name
HAVING AVG(f.donation_amount_inr) > (SELECT AVG(donation_amount_inr) FROM fact_donations)
ORDER BY avg_donation_inr DESC;

-- --------------------------------------------------------------------------
-- Q11. Volunteer engagement summary per NGO (secondary fact table)
-- --------------------------------------------------------------------------
SELECT
    g.ngo_name,
    SUM(v.volunteer_count) AS total_volunteer_instances,
    SUM(v.hours_logged)    AS total_hours_logged,
    ROUND(1.0 * SUM(v.hours_logged) / NULLIF(SUM(v.volunteer_count), 0), 1) AS avg_hours_per_volunteer
FROM fact_volunteer_hours v
JOIN dim_ngo g ON v.ngo_id = g.ngo_id
GROUP BY g.ngo_name
ORDER BY total_hours_logged DESC;

-- --------------------------------------------------------------------------
-- Q12. Fiscal-year donation summary (Indian FY: Apr-Mar)
-- --------------------------------------------------------------------------
SELECT
    d.fiscal_year,
    COUNT(f.donation_id) AS num_donations,
    ROUND(SUM(f.donation_amount_inr), 2) AS total_amount_inr
FROM fact_donations f
JOIN dim_date d ON f.date_id = d.date_id
GROUP BY d.fiscal_year
ORDER BY d.fiscal_year;

-- --------------------------------------------------------------------------
-- Q13. Payment mode preference by donor type (pivot-style CASE aggregation)
-- --------------------------------------------------------------------------
SELECT
    donor_type,
    SUM(CASE WHEN payment_mode = 'UPI' THEN 1 ELSE 0 END)          AS upi_count,
    SUM(CASE WHEN payment_mode = 'Credit Card' THEN 1 ELSE 0 END)  AS credit_card_count,
    SUM(CASE WHEN payment_mode = 'Net Banking' THEN 1 ELSE 0 END)  AS net_banking_count,
    SUM(CASE WHEN payment_mode = 'Cheque' THEN 1 ELSE 0 END)       AS cheque_count,
    SUM(CASE WHEN payment_mode = 'NEFT/RTGS' THEN 1 ELSE 0 END)    AS neft_rtgs_count
FROM fact_donations
GROUP BY donor_type;

-- --------------------------------------------------------------------------
-- Q14. NGOs founded before 1980 vs after — average donation comparison (CTE)
-- --------------------------------------------------------------------------
WITH ngo_era AS (
    SELECT ngo_id, ngo_name,
           CASE WHEN year_founded < 1980 THEN 'Founded Pre-1980' ELSE 'Founded 1980 Onwards' END AS era
    FROM dim_ngo
)
SELECT
    e.era,
    COUNT(DISTINCT e.ngo_id) AS num_ngos,
    ROUND(AVG(f.donation_amount_inr), 2) AS avg_donation_inr,
    ROUND(SUM(f.donation_amount_inr), 2) AS total_amount_inr
FROM fact_donations f
JOIN ngo_era e ON f.ngo_id = e.ngo_id
GROUP BY e.era;

-- --------------------------------------------------------------------------
-- Q15. Top 3 campaigns by total funds raised, per NGO (window function: ROW_NUMBER)
-- --------------------------------------------------------------------------
WITH campaign_totals AS (
    SELECT
        g.ngo_name, c.campaign_name,
        SUM(f.donation_amount_inr) AS total_raised,
        ROW_NUMBER() OVER (PARTITION BY g.ngo_name ORDER BY SUM(f.donation_amount_inr) DESC) AS rn
    FROM fact_donations f
    JOIN dim_campaign c ON f.campaign_id = c.campaign_id
    JOIN dim_ngo g ON f.ngo_id = g.ngo_id
    GROUP BY g.ngo_name, c.campaign_name
)
SELECT ngo_name, campaign_name, ROUND(total_raised, 2) AS total_raised_inr
FROM campaign_totals
WHERE rn <= 3
ORDER BY ngo_name, rn;

-- --------------------------------------------------------------------------
-- Q16. Corporate CSR channel effectiveness vs other channels
-- --------------------------------------------------------------------------
SELECT
    c.channel,
    COUNT(f.donation_id) AS num_donations,
    ROUND(SUM(f.donation_amount_inr), 2) AS total_amount_inr,
    ROUND(AVG(f.donation_amount_inr), 2) AS avg_donation_inr
FROM fact_donations f
JOIN dim_campaign c ON f.campaign_id = c.campaign_id
GROUP BY c.channel
ORDER BY total_amount_inr DESC;

-- --------------------------------------------------------------------------
-- Q17. Focus-area level donation performance (join back to real NGO research)
-- --------------------------------------------------------------------------
SELECT
    g.primary_focus_area,
    COUNT(DISTINCT g.ngo_id) AS num_ngos,
    ROUND(SUM(f.donation_amount_inr), 2) AS total_amount_inr,
    ROUND(AVG(f.donation_amount_inr), 2) AS avg_donation_inr
FROM fact_donations f
JOIN dim_ngo g ON f.ngo_id = g.ngo_id
GROUP BY g.primary_focus_area
ORDER BY total_amount_inr DESC;
