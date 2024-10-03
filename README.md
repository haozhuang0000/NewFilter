# NewFilter

This repository utilizes Large Language Models (LLMs) to categorize news articles into predefined categories.

## Setup

- Install all required libraries listed in `requirements.txt`.
- Run `main.py` within the `scripts\filters` directory.

## Description of Modules

### `db` Folder

Contains `mongodb.py`, which establishes a client to retrieve data from the MongoDB database.

### `documents` Folder

Includes operations involving Retrieval-Augmented Generation (RAG). Currently, RAG is not used because the news articles are not long enough to necessitate its use.

### `filters` Folder

Contains modules related to the filtering process:

- **`categories.py`**: Defines all the main categories and subcategories used for classification.
- **`llm.py`**: Provides an LLM wrapper around a model using LangChain. Currently, `ChatOpenAI` is used due to familiarity.
- **`news_filter.py`**: Contains the `get_filter()` function, which makes an LLM call to obtain the evaluation results for a single article.
- **`prompts.py`**: Holds the prompt template used by the LLM.

### `main.py`

Implements the logic behind the filtering process:

- Retrieves the top 3 most recent articles from the database.
- Feeds the 'content' section of each article into the `get_filter()` function.
  - Makes one call of `get_filter()` for each large category to obtain scores for each subcategory.
- Aggregates all the scores and compiles them into an `.xlsx` file:
  - **Sheet 1**: Contains the scores of every subcategory.
  - **Sheet 2**: Contains the summary counts of each larger category.