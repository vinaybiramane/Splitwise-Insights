import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk
from nltk.probability import FreqDist

# Download necessary NLTK data
nltk.download('punkt')
nltk.download('stopwords')

def load_data(file):
    df = pd.read_csv(file)
    df = df.iloc[:-1,:]
    df['Date'] = pd.to_datetime(df['Date'])
    df['Cost'] = df.Cost.astype('float')
    return df

def filter_data(df, start_date, end_date):
    df['justdate'] = df['Date'].apply(lambda x: x.date())
    return df[(df['justdate'] >= start_date) & (df['justdate'] <= end_date)]

def plot_cost_charts(df):
    # Monthly spending trend
    total_spending = df['Cost'].sum()

    # Get category-wise spending
    category_spending = df.groupby('Category')['Cost'].sum().sort_values()

    # Calculate monthly spending
    monthly_spending = df.groupby(df['Date'].dt.to_period('M'))['Cost'].sum()

    # Get top 5 expensive purchases
    top_5_expensive = df.nlargest(5, 'Cost')
    
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(data=top_5_expensive, x="Date", y="Cost", hue="Category", ax=ax)
    ax.set_title('Top 5 Expensive Spends')
    st.pyplot(fig)

    fig, ax = plt.subplots(figsize=(12, 6))
    sns.scatterplot(data=df, x="Date", y="Cost", hue="Category", ax=ax)
    ax.set_title('Monthly Spending Trend')
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    st.pyplot(fig)

    # Top 10 categories by total cost
    category_costs = df.groupby('Category')['Cost'].sum().sort_values(ascending=False).head(10)
    
    fig, ax = plt.subplots(figsize=(12, 6))
    category_spending.plot(kind='bar',ax=ax)
    ax.set_title('Monthly Spending Trend')

    st.pyplot(fig)
    
    # Visualize monthly spending trend
    fig, ax = plt.subplots(figsize=(12, 6))
    monthly_spending.plot(kind='line', marker='o', ax=ax)
    ax.set_title('Monthly Spending Trend')

    st.pyplot(fig)
    
def preprocess_text(text):
    tokens = word_tokenize(text.lower())
    stop_words = set(stopwords.words('english'))
    return [word for word in tokens if word.isalnum() and word not in stop_words]

def plot_description_insights(df):
    # Word frequency analysis
    stop_words = set(stopwords.words('english'))
    words = [word.lower() for desc in df['Description'] for word in word_tokenize(str(desc)) if word.isalnum()]
    words = [word for word in words if word not in stop_words]
    
   # Get most common words
    word_freq = FreqDist(words)
    common_words = word_freq.most_common(10)

    print("\nMost common words in descriptions:")
    for word, count in common_words:
        print(f"{word}: {count}")

    # Visualize most common words
    fig, ax = plt.subplots(figsize=(12, 6))
    word_freq.plot(30, cumulative=False)
    st.pyplot(fig)
    
    # Analyze descriptions by category
    category_words = {}
    for category in df['Category'].unique():
        category_desc = ' '.join(df[df['Category'] == category]['Description'].astype(str))
        category_words[category] = FreqDist(preprocess_text(category_desc)).most_common(5)

    print("\nMost common words by category:")
    for category, words in category_words.items():
        print(f"\n{category}:")
        for word, count in words:
            print(f"  {word}: {count}")


    # Visualize words by category
    fig, ax = plt.subplots(figsize=(40, 10))
    for i, (category, words) in enumerate(category_words.items()):
        ax.bar([x[0] for x in words], [x[1] for x in words], label=category)
    ax.set_title('Top 5 Words by Category')
    ax.set_xlabel('Words')
    ax.set_ylabel('Frequency')
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    # ax.set_xticks(ticks = range(len(words)), ha = 'right' ,rotation=45, labels = [x[0] for x in words])
    st.pyplot(fig)


def main():
    st.title('Splitwise Insights')

    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    if uploaded_file is not None:
        df = load_data(uploaded_file)

        min_date = df['Date'].min().date()
        max_date = df['Date'].max().date()

        start_date = st.date_input('Start date', min_date)
        end_date = st.date_input('End date', max_date)

        filtered_df = filter_data(df, start_date, end_date)

        tab1, tab2 = st.tabs(["Cost Charts", "Description Insights"])

        with tab1:
            st.header("Cost Related Charts")
            plot_cost_charts(filtered_df)

        with tab2:
            st.header("Description Insights")
            plot_description_insights(filtered_df)

if __name__ == "__main__":
    main()