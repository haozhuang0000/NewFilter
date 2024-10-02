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
    # Your news article text
    mongodb_handler = mongodb.MongoDBHandler()
    db = mongodb_handler.get_database()
    col = db[config['NEWS_COLLECTION']]

    # Retrieve articles from MongoDB
    top_items = col.find().sort("Storage_date", -1).limit(num_articles)

    # Initialize the LLM
    llm = Llm(model='gpt-4o-mini', openai_api_key=config["OPENAI_API_KEY"])

    # Initialize the NewsFilter
    news_filter = NewsFilter(llm=llm, categories=categories)
    
    results_list = []

    # Iterate over the articles
    for item in top_items:
        article_content = item['Content']  # Adjust the field name if necessary

        # Get the filter results
        analysis_results = news_filter.get_filter(article_text=article_content)

        # Keep track of the article ID or other metadata
        article_id = item.get('_id')  # Or any other unique identifier
        storage_date = item.get('Storage_date')

        # Flatten the results
        flattened_results = {'Article_ID': article_id, 'Storage_date': storage_date}
        for large_category, factors_results in analysis_results.items():
            for factor, score in factors_results.items():
                # Create a unique key for each factor
                key = f"{large_category} - {factor}"
                flattened_results[key] = score

        # Append the flattened results to the list
        results_list.append(flattened_results)

    # Create a DataFrame from the results
    df = pd.DataFrame(results_list)

    # Save the DataFrame to a CSV file
    df.to_csv('analysis_results.csv', index=False)

    # Print the results
    for large_category, factors_results in analysis_results.items():
        print(f"\nCategory: {large_category}")
        for factor, score in factors_results.items():
            print(f"{factor}: {score}")

if __name__ == "__main__":
    num_articles = 3  # Or any number you want

    main(num_articles)
