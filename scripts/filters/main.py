# main.py
import sys
sys.path.append(r'../../')
sys.path.append(r'../')
from llm import Llm
from news_filter import NewsFilter
from categories import categories
from dotenv import dotenv_values
import pandas as pd
from db import mongodb
config = dotenv_values(".env")
print(config)
def main(num_articles):
    mongodb_handler = mongodb.MongoDBHandler()
    db = mongodb_handler.get_database()
    col = db[config['NEWS_COLLECTION']]
    
    top_items = col.find().sort("Storage_date", -1).limit(num_articles)

    # Initialize the LLM
    llm = Llm(model='gpt-4o-mini', openai_api_key=config["OPENAI_API_KEY"])

    # Initialize the NewsFilter
    news_filter = NewsFilter(llm=llm, categories=categories)
    
    results_list = []
    summary_list = []

    # Iterate over the articles
    for item in top_items:
        article_content = item['Content'] 

        # Get the filter results
        analysis_results = news_filter.get_filter(article_text=article_content)

        # Keep track of the article metadata
        article_id = item.get('_id')  # Or any other unique identifier
        storage_date = item.get('Storage_date')
        article_title = item.get('Title')  # Get the article title

        # Flatten the results
        flattened_results = {
            'Article_ID': article_id,
            'Storage_date': storage_date,
            'Title': article_title
        }

        # For summary counts per big category
        category_counts = {
            'Article_ID': article_id,
            'Storage_date': storage_date,
            'Title': article_title
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

    # Create DataFrames from the results
    detailed_df = pd.DataFrame(results_list)
    summary_df = pd.DataFrame(summary_list)

    # Save the DataFrames to an Excel file with multiple sheets
    output_file = 'analysis_results.xlsx'
    with pd.ExcelWriter(output_file) as writer:
        detailed_df.to_excel(writer, sheet_name='Detailed Results', index=False)
        summary_df.to_excel(writer, sheet_name='Summary Counts', index=False)

    print(f"Analysis results saved to {output_file}")

    # Optionally, print the last article's analysis results
    for large_category, factors_results in analysis_results.items():
        print(f"\nCategory: {large_category}")
        for factor, score in factors_results.items():
            print(f"{factor}: {score}")

if __name__ == "__main__":
    num_articles = 3
    main(num_articles)