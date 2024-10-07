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
    # llm = Llm(model='gpt-4o-mini', openai_api_key=config["OPENAI_API_KEY"])
    llm = Llm(model='llama3.1:8b')
    # Initialize the NewsFilter
    news_filter = NewsFilter(llm=llm, categories=categories)

    results_list = []
    summary_list = []
    processed_time = []
    # Iterate over the articles
    for item in top_items:
        start_time = time.time()
        article_content = item['Content']

        # Get the filter results
        analysis_results = news_filter.get_filter(article_text=article_content)

        # Keep track of the article metadata
        article_id = item.get('_id')  # Or any other unique identifier
        date = item.get('Date')
        article_title = item.get('Title')  # Get the article title
        url = item.get('Link')
        # Flatten the results
        flattened_results = {
            'Article_ID': article_id,
            'Date': date,
            'Title': article_title,
            'Url': url
        }

        # For summary counts per big category
        category_counts = {
            'Article_ID': article_id,
            'Date': date,
            'Title': article_title,
            'Url': url
        }

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
    summary_df_melted = pd.melt(summary_df, id_vars=['Article_ID', 'Date', 'Title', 'Url'],
                                var_name='Level0_Categories', value_name='Value')
    detailed_df_melted = pd.melt(detailed_df, id_vars=['Article_ID', 'Date', 'Title', 'Url'],
                                 var_name='Level1_Categories', value_name='Value')

    summary_df_melted_grouped = summary_df_melted.groupby(['Article_ID', 'Date', 'Title', 'Url']).agg({
        'Level0_Categories': lambda x: list(x),
        'Value': lambda x: list(x)
    }).reset_index()

    detailed_df_melted_grouped = detailed_df_melted.groupby(['Article_ID', 'Date', 'Title', 'Url']).agg({
        'Level1_Categories': lambda x: list(x),
        'Value': lambda x: list(x)
    }).reset_index()

    summary_df_melted_grouped['Level0_Categories'] = summary_df_melted_grouped.apply(lambda row: dict(zip(row['Level0_Categories'], row['Value'])), axis=1)
    detailed_df_melted_grouped['Level1_Categories'] = detailed_df_melted_grouped.apply(lambda row: [row['Level1_Categories'], row['Value']], axis=1)

    summary_df_melted_grouped.drop(columns=['Value'], inplace=True)
    detailed_df_melted_grouped.drop(columns=['Value'], inplace=True)

    df_merge = detailed_df_melted_grouped.merge(summary_df_melted_grouped, how='inner', on=['Article_ID', 'Date', 'Title', 'Url'])
    df_merge.rename(columns={'Article_ID': '_id'}, inplace=True)
    # Save the DataFrames to an Excel file with multiple sheets
    # output_file = 'analysis_results_test.xlsx'
    # with pd.ExcelWriter(output_file) as writer:
    #     detailed_df.to_excel(writer, sheet_name='Detailed Results', index=False)
    #     summary_df.to_excel(writer, sheet_name='Summary Counts', index=False)
    mongodb_handler.insert_db(df_merge[['_id', 'Date', 'Title', 'Url', 'Level0_Categories', 'Level1_Categories']],
                              dbs_name='CAESARS', col_name='test_filter')
    # print(f"Analysis results saved to {output_file}")

    # Optionally, print the last article's analysis results
    for large_category, factors_results in analysis_results.items():
        print(f"\nCategory: {large_category}")
        for factor, score in factors_results.items():
            print(f"{factor}: {score}")

if __name__ == "__main__":
    num_articles = 100
    main(num_articles)