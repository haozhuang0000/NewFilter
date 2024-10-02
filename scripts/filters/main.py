# main.py

from llm import Llm
from news_filter import NewsFilter
from categories import categories
from dotenv import dotenv_values
config = dotenv_values(".env")

if __name__ == "__main__":
    # Your news article text
    article_text = """
        U.S. oil prices ended slightly higher Tuesday after an early-session drop to their lowest level in nearly a month on expectations global producers would bring additional crude oil to market to make up for recent deficits. Light, sweet crude for August delivery ended a tiny 0.03% higher at $68.08 a barrel on the New York Mercantile Exchange. Brent crude, the global benchmark, rose 0.5% to $72.16 a barrel. U.S. prices fell to as low as $67.03 a barrel during morning trading, the lowest intraday since mid- June. “Reports that the U.S. is mulling an [strategic petroleum reserve] release and a softer stance on Iranian exports, along with comments from other large producers reassuring markets that they would continue to balance the market, helped fuel the perception that more oil is re-entering the market,” said JBC Energy, which added this notion “is finding solid justification in terms of crude movements.” Traders began to reduce selling, giving oil prices a modest lift late in the U.S. session, on the view weekly U.S. oil inventory data may show another bullish decline. Last week’s official report showed a 13 million-barrel drop to 405 million barrels, the lowest since February 2015. The government’s weekly report on oil inventories is due to be released by the Energy Information Administration on Wednesday morning. Analysts surveyed by The Wall Street Journal are expecting, on average, a 3.3 million-barrel decline last week in crude-oil inventories. The American Petroleum Institute, an industry group, said late Tuesday that its own data for the week showed a 629,000-barrel increase in crude supplies, a 425,000-barrel rise in gasoline stocks and a 1.7-million-barrel increase in distillate inventories, according to a market participant. “The market is trading nervous after taking a pummeling in yesterday’s action,” said Dan Flynn at Price Futures in Chicago. “The market is in chop mode for the moment and we are expecting another large draw in crude oil and product stocks.” Tuesday’s moves came after oil prices fell more than 4% for the second time in the last four sessions on Monday. Oil-market observers are increasingly focused on the possibility the U.S. could open up its strategic reserves following comments by President Donald Trump late last week. “The main reason for yesterday’s significant price drop was the talk about SPR release that is getting louder,” according to Tamas Varga, analyst at brokerage PVM Oil Associates Ltd. “The U.S. SPR is currently some 270 million barrels above the required level of 90 days of the previous year’s net imports—there is room to act if deemed necessary,” he added. Also exerting pressure are signs Saudi Arabia, the world’s largest crude exporter, is ramping up output more than agreed in conjunction with the Organization of the Petroleum Exporting Countries last month. OPEC, of which Saudi Arabia is the de facto head, and 10 producers outside the cartel, including Russia, agreed in late June to begin increasing crude production by up to 1 million barrels a day starting this month after more than year of holding back output. The decision came amid supply outages in Venezuela and risk to supply in Iran due to impending U.S. economic sanctions. At the same time, the U.S. Energy Information Administration said Monday that it expects U.S. shale oil output to increase by 143,000 barrels a day month on month to reach 7.47 million barrels a day in August. Among refined products, gasoline futures rose 1.2% to $2.0261 a gallon. Diesel futures gained 0.8% to $2.0701 a gallon. Corrections & Amplifications The U.S. Energy Information Administration said Monday it expects U.S. shale oil output to increase by 143,000 barrels a day. An earlier version of this article misstated the number of barrels a day. (July 17, 2018)
    """

    # Initialize the LLM
    llm = Llm(model='gpt-4o-mini', openai_api_key=config["OPENAI_API_KEY"])

    # Initialize the NewsFilter
    news_filter = NewsFilter(llm=llm, categories=categories)

    # Get the filter results
    analysis_results = news_filter.get_filter(article_text=article_text)

    # Print the results
    for large_category, factors_results in analysis_results.items():
        print(f"\nCategory: {large_category}")
        for factor, score in factors_results.items():
            print(f"{factor}: {score}")
