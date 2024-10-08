# Splitwise Insights

This project provides tools for analyzing Splitwise expense data using AI-powered insights and data visualization.

## Part 1: AI-Powered CSV Insights (insights_llm.py)

### Overview
The `insights_llm.py` script uses Langchain agents to answer questions about CSV data. It leverages OpenAI's language model to provide intelligent insights based on user queries.

### Requirements
- Python 3.7+
- OpenAI API key
- Required libraries: langchain, openai, pandas, python-dotenv

### Setup
1. Install required libraries:
   ```
   pip install langchain openai pandas python-dotenv
   ```

2. Create a `.env` file in the project root and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

### Usage
1. Run the script:
   ```
   python insights_llm.py
   ```

2. Enter the path to your CSV file when prompted.

3. Ask questions about the data. The AI agent will analyze the CSV and provide answers.

4. Type 'exit' to quit the program.

### Example Questions
- "What is the total amount spent?"
- "Which category has the highest expenses?"
- "Show me the top 5 most expensive items."

## Part 2: Data Visualization (insight.py)

### Overview
The `insight.py` script creates insightful charts from Splitwise expense data using Python libraries like Matplotlib and Seaborn.

### Requirements
- Python 3.7+
- Required libraries: pandas, matplotlib, seaborn, nltk

### Setup
1. Install required libraries:
   ```
   pip install pandas matplotlib seaborn nltk
   ```

2. Download NLTK data:
   ```python
   import nltk
   nltk.download('punkt')
   nltk.download('stopwords')
   ```

### Usage
1. Ensure your Splitwise CSV export is in the same directory as the script.

2. Modify the script to use your CSV filename:
   ```python
   df = pd.read_csv('your_splitwise_export.csv')
   ```

3. Run the script:
   ```
   python insight.py
   ```

4. The script will generate and display various charts:
   - Monthly spending trend
   - Top categories by total cost
   - Word frequency in expense descriptions

### Customization
You can modify the script to change chart types, colors, or add new visualizations based on your specific needs.

## Contributing
Contributions to improve either part of the project are welcome. Please submit a pull request or open an issue to discuss proposed changes.

## License
[MIT License](LICENSE)
