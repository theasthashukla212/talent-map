# Talent Map

Talent Map is a career recommendation system that helps students and individuals discover suitable career paths based on their interests, skills, and academic background. The system uses machine learning techniques, specifically cosine similarity, to match user profiles with job requirements from the O\*NET database.

## Features

- **Career Recommendation**: Provides personalized job recommendations based on user input.
- **Domain Scoring**: Offers domain recommendations (e.g., Engineering, Medical, Business) using a scoring system.
- **Interactive Web App**: Built with Streamlit for easy user interaction.
- **Data-Driven**: Utilizes O\*NET occupational data for accurate job matching.
- **Modular Design**: Organized into modules for input handling, recommendations, and data processing.

## Project Structure

```
talent-map/
├── app.py                          # Main application entry point
├── test_model.py                   # Test script for the recommendation model
├── requirements.txt                # Python dependencies
├── README.md                       # Project documentation
├── data/                           # Data files
│   ├── career_matrix.csv           # Merged career matrix
│   ├── career_matrix_with_titles.csv # Career matrix with job titles
│   ├── interest_matrix.csv         # Interest data
│   ├── job_knowledge_matrix.csv    # Knowledge requirements
│   ├── job_skill_matrix.csv        # Skill requirements
│   └── *.txt                       # Raw data files
├── modules/                        # Application modules
│   ├── input_module.py             # User input handling (Streamlit)
│   └── recommendation.py           # Domain recommendation logic
└── src/                            # Source code for data processing
    ├── build_career_matrix.py      # Builds the career matrix
    ├── build_interest_Matrix.py    # Builds interest matrix
    ├── build_knowledge_matrix.py   # Builds knowledge matrix
    ├── build_matrix.py             # General matrix building
    ├── merge_titles.py             # Merges job titles
    ├── recommender.py              # Core recommendation engine
    └── train_model.py              # Model training and normalization
```

## Installation

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd talent-map
   ```

2. Create a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Running the Web App

To start the interactive Streamlit application:

```bash
streamlit run app.py
```

This will launch a web interface where users can:

- Select their academic stream (PCM, PCB, Commerce, Arts)
- Choose their interests (Technology, Biology, Business, etc.)
- Specify their strengths (Logical Thinking, Communication, etc.)

The app will then provide career and domain recommendations.

### Using the Recommendation Engine

You can also use the recommendation functions directly in Python:

```python
from app import recommend

# Example user input (list of selected features)
user_input = ['Mathematics', 'Physics', 'Technology']

recommendations = recommend(user_input)
print(recommendations)
```

### Building Data Matrices

To rebuild the data matrices from raw O\*NET data:

```bash
python src/build_career_matrix.py
python src/train_model.py  # For normalization
```

## Data Sources

The project uses data from the O\*NET (Occupational Information Network) database, which provides comprehensive information about occupations, skills, knowledge, and interests required for various jobs.

- **Skills Matrix**: Contains skill requirements for different occupations
- **Knowledge Matrix**: Includes knowledge areas relevant to jobs
- **Interest Matrix**: Maps Holland codes (RIASEC) to occupations
- **Career Matrix**: Merged matrix combining all features

## Algorithms

- **Cosine Similarity**: Used for matching user profiles with job requirements
- **Normalization**: Min-Max scaling applied to features for better similarity computation
- **Scoring System**: Rule-based scoring for domain recommendations

## Dependencies

- pandas: Data manipulation and analysis
- numpy: Numerical computing
- scikit-learn: Machine learning algorithms
- streamlit: Web application framework

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- O\*NET database for occupational data
- Scikit-learn for machine learning tools
- Streamlit for the web framework
