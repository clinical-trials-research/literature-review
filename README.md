# Literature Review

## Todo

- When generating schema, we want to query around 1000-5000 trials. This might differ from the num_trials specified by the user.
- Don't insert study if it already exists.

## Notebooks

1. [Summary Statistics](./notebooks/01-summary-stats.ipynb)

## Installation

### Install Poetry

If poetry is not installed,

```bash
pip install pipx
pipx install poetry
```

### Install Repo with Poetry

```bash
git clone https://github.com/clinical-trials-research/literature-review.git
cd literature-review
poetry install
```

## API

- **`ClinicalTrials(*, num_studies=1000, connection=None, schema_directory="schema.json")`** - Creates `ClinicalTrials` object which provides an interface for database management.
  - `num_studies` - Number of studies to retrieve in each call to `update_database` or `get_studies`.
  - `connection` - Database connection. If not specified, creates new one.
  - `schema_directory` - Schema to use. If not specified, creates a schema.

    ```python
    from litreview import ClinicalTrials

    trials = ClinicalTrials()
    ```

- **`ClinicalTrials.query(*fields)`** - Query the database for the specified fields

    ```python
    trials.query("NCTId", "BriefDescription")
    ```

- **`ClinicalTrials.update_database()`** - Update the database with `num_studies` number of studies.

    ```python
    trials.update_database()
    ```

- **`ClinicalTrials.get_studies()`** - Retrieve `num_studies` number of studies in a list.

    ```python
    studies = trials.get_studies()
    ```

## Resources

- [Clinical Trials API](https://clinicaltrials.gov/data-api/api)
- [Clinical Trials Field Definitions](https://clinicaltrials.gov/data-api/about-api/study-data-structure)
