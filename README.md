# Project 4 – DS 1300: Recent College Grads, Unemployment, and Salary Analysis

## Overview
This project analyzes the relationship between college major, unemployment risk, and salary outcomes for recent graduates in the United States. It extends the analysis to include geographic variation in salaries by state, providing actionable insights for students, advisors, and policymakers.

## Objectives
- Quantify how unemployment risk and gender composition affect median salaries by major
- Test key hypotheses using robust statistical methods (t-test, ANOVA, correlation)
- Visualize salary and unemployment gaps with clear, reproducible figures
- Map state-level salary differences for key majors using BLS data

## Data Sources
- `/data/recent-grads.csv`: 173 × 21, original major-level data
- `/data/LNS14027662.csv`: FRED BA unemployment series (1992–2025)
- `/data/cpsaat25.xlsx`: CPS A-25, unemployment by occupation & sex
- `/data/state_M2024_dl.xlsx`: BLS OEWS May 2024, state-level occupational wages
- `/meta/major_to_occ.csv`: Hand-built major-to-occupation lookup (if used)

## Workflow
All analysis is performed in a single Jupyter notebook: `project4.ipynb`.

### Key Steps
1. **Setup & Imports**: Ensures reproducibility and organized outputs
2. **Data Ingestion & Cleaning**: Aligns and merges all sources, engineers gap variables
3. **Statistical Analysis**:
   - H₁: Welch t-test for salary differences by occupation risk
   - H₂: ANOVA for unemployment gap across gender buckets
   - H₃: Pearson correlation for gender-pay link
4. **Visualization**:
   - Boxplots, barplots, scatterplots, heatmaps
   - US state-level salary choropleth (Plotly)
5. **Geographic Extension**: Maps average salaries by major and state, highlighting regional disparities
6. **Summary & Export**: Key takeaways and optional PowerPoint export

## Reproducibility & Quality
- All code is annotated with "# Why:" comments for narrative clarity
- Logging at INFO level for pipeline steps
- Figures saved as SVG and PNG in `/outputs/figs/`
- Categorical columns set to `category` dtype before analysis
- Requirements auto-updated as new libraries are used

## Setup & Usage
1. Clone/download this repository
2. Place all data files in the `/data/` directory as specified above
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Launch Jupyter and run `project4.ipynb` end-to-end

## Visualization Example
- US map of average Engineering salaries by state (BLS OEWS May 2024)
- Sequential color scale for intuitive comparison

## Extending the Analysis
- Add more majors or regions to the geographic analysis
- Test for regional effects using ANOVA or chi-squared tests
- Adjust for cost of living using external COLI data (optional)

## Authors & Acknowledgments
- Analysis by Dr Data Savvy (DS 1300, Spring 2024)
- Data from BLS, FRED, and US Census

## License
For educational use only. Data sources retain their original licenses. 