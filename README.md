# Literature Review

## Todo

- When generating schema, we want to query around 1000-5000 trials. This might differ from the num_trials specified by the user.
- Add interface to query by piece name.
- Don't insert study if it already exists?

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

## Usage

## Resources

- [Clinical Trials API](https://clinicaltrials.gov/data-api/api)
- [Clinical Trials Field Definitions](https://clinicaltrials.gov/data-api/about-api/study-data-structure)
