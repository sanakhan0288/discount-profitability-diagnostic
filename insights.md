
# Superstore Sales & Profitability — Business Findings

## Project Objective

Investigate how recorded sales, profit margins, and discount levels vary across product categories and regions. Identify areas that management should investigate further.

## Dataset Overview

- Transaction rows analysed: 10,194
- Columns: 21
- Distinct orders: 5,111
- Units sold: 38,654
- Missing values in the audit: 0
- Exact duplicate rows in the audit: 0
- Recorded order dates: 2023-01-03 to 2026-12-30

The workbook is a Superstore-style sample dataset. Its recorded date range extends beyond the analysis date of 2026-10-12, so the source and dates should be verified before treating them as historical business records.

## Key Finding 1: Overall Profitability

**Evidence**
- Total sales: 2,326,534.35
- Total profit: 292,296.81
- Overall profit margin: 12.56%
- Average row-level discount: 15.54%

**Interpretation**

The dataset records positive overall profit, with a total profit margin of approximately 12.56%.

**Recommended investigation**

Review profitability by product, region, discount level, and time period to determine where performance is strongest and weakest.

## Key Finding 2: High-Discount Transactions Have Negative Profit

**Evidence**

| Discount band | Sales | Profit | Profit margin |
|---|---:|---:|---:|
| No Discount | 1,105,323.79 | 326,718.59 | 29.56% |
| Low (0–10%) | 54,952.50 | 9,099.77 | 16.56% |
| Medium (>10–30%) | 905,971.98 | 81,985.50 | 9.05% |
| High (>30%) | 260,286.08 | -125,507.24 | -48.22% |

**Interpretation**

The high-discount group has negative recorded profit, while the no-discount group has the highest profit margin among these groups.

This pattern is an investigation lead, not proof that discounts caused the losses. Product mix, costs, order characteristics, and other factors may influence the relationship.

**Recommended investigation**

Review high-discount products and orders individually. Compare their recorded sales, profit, quantity, product category, and region before making pricing decisions.

## Key Finding 3: Tables, Bookcases, and Supplies Need Review

**Evidence**

The lowest-profit sub-category results include:

- Tables: profit of approximately -17,753.21
- Bookcases: profit of approximately -6,353.07
- Supplies: profit of approximately -1,171.39

**Interpretation**

These product groups have negative total profit in the supplied dataset and warrant further investigation.

**Recommended investigation**

Compare discount levels, order quantities, sales, and profit margins within these sub-categories. Determine whether the pattern is concentrated in specific products or regions.

## Data Quality and Methodology

- The Python audit found no missing values in the supplied workbook and no exact duplicate rows.
- Profit margin is calculated as total profit divided by total sales.
- Distinct orders count unique Order ID values.
- Average discount is a simple average across transaction rows; it is not weighted by sales.
- Discount bands are exploratory groupings defined for this project.
- The supplied date range should be verified against the original source.

## Limitations

- Superstore is fictional sample data, not verified company performance.
- The data is observational and does not establish causal relationships.
- Aggregated summaries can hide differences among individual products and orders.
- Discount-band thresholds affect the comparisons.
- Findings should be validated at a more detailed level before recommending business changes.

## Conclusion

The main investigation priorities are the negative profit recorded in the high-discount group and the losses recorded for selected product sub-categories. An interactive Tableau dashboard will allow users to explore these patterns by product category, region, and time.
