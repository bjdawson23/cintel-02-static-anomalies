# Continuous Intelligence

This site provides documentation for this project.
Use the navigation to explore module-specific materials.

## How-To Guide

Many instructions are common to all our projects.

See
[⭐ **Workflow: Apply Example**](https://denisecase.github.io/pro-analytics-02/workflow-b-apply-example-project/)
to get these projects running on your machine.

## Project Documentation Pages (docs/)

- **Home** - this documentation landing page
- **Project Instructions** - instructions specific to this module
- **Your Files** - how to copy the example and create your version
- **Glossary** - project terms and concepts

## Custom Project

### Dataset

The dataset used was: clinic_data_dawson.csv

### Signals

I added logic to check if the height is TOO LOW or TOO HIGH.

### Experiments

Testing for height under 15 inches was classified as too low. A reason column was added explaining which value(s) triggered the anomaly.

### Results

The code found 8 rows with anomalies. Two of the rows had multiple anomalies for age and height.

### Interpretation

The 8 flagged records reveal likely data entry errors in the clinic's patient records system.
Ages of 94, 120, and 220 years are impossible for a pediatric clinic serving children up to age 16, suggesting likely transcription or keying mistakes were made.

A height of 5 inches and a height of 14 inches are unlikely for any full-term child, pointing to unit errors or keystroke mistakes.
Heights of 84 and 95 inches (7–8 feet) are similarly impossible for pediatric patients.

For the clinic, this means the data pipeline successfully identified records that should be reviewed and corrected before being used in any analysis, reporting, or billing.

For Business Intelligence purposes, implementing this anomaly check as a routine step would help protect against data quality issues.

### Web-Service Metrics Anomaly Rules And Findings

I added a second detector for web-service metrics using these rules:

- High traffic when `requests > 250`
- High error rate when `errors / requests > 0.04`
- High latency when `total_latency_ms > 9000`

The run flagged 22 anomaly intervals (timestamps between 9 and 49).
Most were multi-signal events (high traffic, error rate, and latency together), which points to likely service strain during peak load windows.
This gives BI value by identifying where reliability risk concentrates so teams can target capacity planning and performance tuning.

## Additional Resources

- [Suggested Datasets](https://denisecase.github.io/pro-analytics-02/reference/datasets/cintel/)
