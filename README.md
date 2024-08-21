# Literature Review

## Todo

- When generating schema, we want to query around 1000-5000 trials. This might differ from the num_trials specified by the user.
- Don't insert study if it already exists.
- Modify `_create_table` algorithm. Right now, it doesn't work with PostgreSQL because we cannot define foreign relations before tables are created.

## Notebooks

1. [NLP Notes](./notebooks/00-nlp-notes.ipynb)
2. [Summary Statistics](./notebooks/01-summary-stats.ipynb)
3. [Embeddings](./notebooks/02-embeddings.ipynb)
4. [Vector Database](./notebooks/03-vector-database.ipynb)

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

### Clinical Trials

- [Clinical Trials API](https://clinicaltrials.gov/data-api/api)
- [Clinical Trials Field Definitions](https://clinicaltrials.gov/data-api/about-api/study-data-structure)

### NLP

- [What is an embedding?](https://stackoverflow.blog/2023/11/09/an-intuitive-introduction-to-text-embeddings/)
- [HuggingFace NLP Tutorial](https://huggingface.co/learn/nlp-course/chapter1/1)
- [BERT Embeddings Tutorial](https://mccormickml.com/2019/05/14/BERT-word-embeddings-tutorial/#3-extracting-embeddings)
