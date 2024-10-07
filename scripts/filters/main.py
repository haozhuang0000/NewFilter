# main.py
import os
import sys
import time
import numpy as np
sys.path.append(r'../../')
sys.path.append(r'../')
from llm import Llm
from news_filter import NewsFilter
from categories import categories
from dotenv import load_dotenv, find_dotenv
import pandas as pd
from db import mongodb
load_dotenv(find_dotenv())

def main(num_articles):
    mongodb_handler = mongodb.MongoDBHandler()
    db = mongodb_handler.get_database()
    col = db[os.environ['NEWS_COLLECTION']]

    top_items = col.find().sort("Storage_date", -1).limit(num_articles)

    # Initialize the LLM
    llm = Llm(model='llama3.1:8b')

    # Initialize the NewsFilter
    news_filter = NewsFilter(llm=llm, categories=categories)

    results_list = []
    summary_list = []
    processed_time = []
    # Iterate over the articles
    for item in top_items:
        start_time = time.time()
        article_content = item['content']

        # Get the company names from the article
        company_names = item.get('company_names', [])  # Get the list or an empty list if not present

        # Get the filter results
        analysis_results = news_filter.get_filter(article_text=article_content)

        # Get company relevance scores if company names are present
        if company_names:
            relevance_scores = news_filter.get_company_relevance(article_text=article_content, company_names=company_names)
        else:
            relevance_scores = {}

        # Keep track of the article metadata
        article_id = item.get('_id')  # Or any other unique identifier
        date = item.get('date')
        article_title = item.get('title')  # Get the article title
        url = item.get('link')

        # Flatten the results
        flattened_results = {
            'Article_ID': article_id,
            'Date': date,
            'Title': article_title,
            'Url': url,
            'Company_scores': relevance_scores  # Add company scores as a separate field
        }

        # For summary counts per big category
        category_counts = {
            'Article_ID': article_id,
            'Date': date,
            'Title': article_title,
            'Url': url
        }

        # Process analysis_results to fill flattened_results and category_counts
        for large_category, factors_results in analysis_results.items():
            # Count the number of matches (scores of 1) for the big category
            matches = sum(score == 1 for score in factors_results.values())
            category_counts[large_category] = matches

            for factor, score in factors_results.items():
                # Create a unique key for each factor
                key = f"{large_category} - {factor}"
                flattened_results[key] = score

        # Append the flattened results to the list
        results_list.append(flattened_results)
        summary_list.append(category_counts)
        end_time = time.time()
        time_spend = end_time - start_time
        processed_time.append(time_spend)

    print(f'Average processed time: {np.sum(processed_time) / num_articles}')
    # Create DataFrames from the results
    detailed_df = pd.DataFrame(results_list)
    summary_df = pd.DataFrame(summary_list)

    # Ensure summary_df contains only expected columns
    expected_columns = ['Article_ID', 'Date', 'Title', 'Url'] + list(categories.keys())
    summary_df = summary_df[expected_columns]

    # Exclude 'Company_scores' from melting
    value_vars = [col for col in detailed_df.columns if col not in ['Article_ID', 'Date', 'Title', 'Url', 'Company_scores']]

    # Melt the dataframes
    detailed_df_melted = pd.melt(
        detailed_df,
        id_vars=['Article_ID', 'Date', 'Title', 'Url'],
        value_vars=value_vars,
        var_name='Level1_Categories',
        value_name='Value'
    )
    summary_df_melted = pd.melt(
        summary_df,
        id_vars=['Article_ID', 'Date', 'Title', 'Url'],
        var_name='Level0_Categories',
        value_name='Value'
    )

    # Group and aggregate
    summary_df_melted_grouped = summary_df_melted.groupby(['Article_ID', 'Date', 'Title', 'Url']).agg({
        'Level0_Categories': lambda x: list(x),
        'Value': lambda x: list(x)
    }).reset_index()
    detailed_df_melted_grouped = detailed_df_melted.groupby(['Article_ID', 'Date', 'Title', 'Url']).agg({
        'Level1_Categories': lambda x: list(x),
        'Value': lambda x: list(x)
    }).reset_index()

    # Convert lists to dictionaries
    summary_df_melted_grouped['Level0_Categories'] = summary_df_melted_grouped.apply(
        lambda row: dict(zip(row['Level0_Categories'], row['Value'])), axis=1)
    detailed_df_melted_grouped['Level1_Categories'] = detailed_df_melted_grouped.apply(
        lambda row: dict(zip(row['Level1_Categories'], row['Value'])), axis=1)

    summary_df_melted_grouped.drop(columns=['Value'], inplace=True)
    detailed_df_melted_grouped.drop(columns=['Value'], inplace=True)

    # Merge the grouped dataframes
    df_merge = detailed_df_melted_grouped.merge(
        summary_df_melted_grouped,
        how='inner',
        on=['Article_ID', 'Date', 'Title', 'Url']
    )

    # Merge 'Company_scores' back into df_merge
    df_merge = df_merge.merge(
        detailed_df[['Article_ID', 'Company_scores']],
        on='Article_ID',
        how='left'
    )

    df_merge.rename(columns={'Article_ID': '_id'}, inplace=True)

    # Insert into MongoDB
    mongodb_handler.insert_db(
        df_merge[['_id', 'Date', 'Title', 'Url', 'Level0_Categories', 'Level1_Categories', 'Company_scores']],
        dbs_name='CAESARS',
        col_name='test_filter'
    )

    # Optionally, print the last article's analysis results
    for large_category, factors_results in analysis_results.items():
        print(f"\nCategory: {large_category}")
        for factor, score in factors_results.items():
            print(f"{factor}: {score}")

    # Print the company relevance scores for the last article
    print("\nCompany Relevance Scores:")
    for company_name, score in relevance_scores.items():
        print(f"{company_name}: {score}")

if __name__ == "__main__":
    num_articles = 1
    main(num_articles)
