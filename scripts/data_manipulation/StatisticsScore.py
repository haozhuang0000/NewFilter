import os
import seaborn as sns
from tqdm import tqdm
from scripts.db import mongodb
from scripts.filters import categories
import json
import pandas as pd
import matplotlib.pyplot as plt
class StatisticalAnalysis:

    def __init__(self):

        self.mongodb_handler = mongodb.MongoDBHandler()
        db = self.mongodb_handler.get_database()

        self.col = db[os.environ['FILTERED_COLLECTION']]

    def _compute_categoryConverageRatio(self, level0_categories):
        category_coverage = 0
        total_category = 0
        for key, value in level0_categories.items():
            total_category += 1
            if value >= 1:
                category_coverage += 1
        return category_coverage / total_category

    def _compute_factorRatio(self, level1_categories):
        each_categories_sum = {}
        for key, value in categories.categories.items():
            each_categories_sum[key] = len(value)

        each_factor_counts = {}
        for key, value in level1_categories.items():
            if value == 1:
                category = key.split(' - ')[0]
                if category not in each_factor_counts.keys():
                    each_factor_counts[category] = 1
                elif category in each_factor_counts.keys():
                    each_factor_counts[category] += 1

        factor_ratio = {}
        for key, value in categories.categories.items():
            factor_ratio[key] = 0

        for key, value in each_factor_counts.items():
            factor_ratio[key] = each_factor_counts[key] / each_categories_sum[key]

        return factor_ratio
    def _compute_normal_factorRatio(self, factor_ratio):

        sum_value = sum(list(factor_ratio.values()))
        if sum_value > 0:
            normal_factor_ratio = {}
            for key, value in factor_ratio.items():
                normal_factor_ratio[key] = value / sum_value
            return normal_factor_ratio
        else:
            return factor_ratio

    def compute_ratio(self):

        find_cursor = self.col.find()
        list_cursor = list(find_cursor)
        for i in list_cursor:
            level0_categories = i['Level0_Categories']
            level1_categories = i['Level1_Categories']
            category_coverage_ratio = self._compute_categoryConverageRatio(level0_categories)
            i['Category_coverage_ratio'] = category_coverage_ratio
            factor_ratio = self._compute_factorRatio(level1_categories)
            i['Factor_ratio'] = factor_ratio
            normalized_factor_ratio = self._compute_normal_factorRatio(factor_ratio)
            i['Normalized_Factor_ratio'] = normalized_factor_ratio
            self.mongodb_handler.insert_db(
                [i],
                dbs_name='CAESARS',
                col_name='news_filter_updated_2'
            )
    def create_plot_categories(self):
        find_cursor = self.col.find()
        list_cursor = list(find_cursor)
        categories = []
        for i in list_cursor:
            # # Combine the Level0 and Level1 categories for each article
            for category, count in i.get('Level0_Categories', {}).items():
                if count > 0:
                    categories.append(category)
            # for category, count in i.get('Level1_Categories', {}).items():
            #     if count > 0:
            #         categories.append(category)

        # Convert the categories list to a DataFrame for easier processing
        df = pd.DataFrame(categories, columns=['Category'])

        # Count the occurrences of each category
        category_counts = df['Category'].value_counts()

        # Plot the distribution of categories using seaborn
        plt.figure(figsize=(8, 10))
        sns.barplot(x=category_counts.index, y=category_counts.values, palette='viridis')
        plt.title('Distribution of Articles by Categories', fontsize=16)
        plt.xlabel('Categories', fontsize=18)
        plt.ylabel('Number of Articles', fontsize=12)
        plt.xticks(rotation=45, ha='right')

        # Save the plot as a PNG file
        # plt.tight_layout()
        plt.savefig('categories_distribution.png', dpi=300)

        # Show the plot
        plt.show()
    def create_plot_companies(self):
        find_cursor = self.col.find()
        list_cursor = list(find_cursor)
        companies = []
        selected_companies = ['American Express Co', 'Chevron Corp', 'Exxon Mobil Corp',
                              "Macy's Inc", 'Ford Motor Co', 'ConocoPhillips', 'Tesla Inc',
                              'Discover Financial Services', 'AMC Entertainment Holdings Inc',
                              'Visa Inc', 'General Motors Co', 'Mastercard Inc']

        for i in list_cursor:
            for company, score in i.get('Company_scores', {}).items():
                if score > 0 and company in selected_companies:
                    companies.append(company)

        # Convert the companies list to a DataFrame for easier processing
        df_companies = pd.DataFrame(companies, columns=['Company'])

        # Count the occurrences of each company
        company_counts = df_companies['Company'].value_counts()

        # Display the top 10 companies
        print(company_counts.head(10))

        # Plot the distribution of companies using seaborn
        plt.figure(figsize=(10, 6))
        sns.barplot(x=company_counts.index, y=company_counts.values, palette='coolwarm')
        plt.title('12 Companies by Mentions in Articles', fontsize=16)
        plt.xlabel('Company', fontsize=12)
        plt.ylabel('Number of Mentions', fontsize=12)
        plt.xticks(rotation=45, ha='right')

        # Save the plot as a PNG file
        plt.tight_layout()
        plt.savefig('company_distribution.png', dpi=300)

        # Show the plot
        plt.show()
if __name__ == '__main__':
    statisticalAnalysis = StatisticalAnalysis()

    statisticalAnalysis.compute_ratio()
    # statisticalAnalysis.create_plot()
    # statisticalAnalysis.create_plot_companies()