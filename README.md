# TalentMap

TalentMap is a **Streamlit-based career recommendation web app** that helps users discover occupations aligned with their skills, knowledge areas, and interests. It builds on the U.S. Department of Labor's **O*NET occupational database**, transforming raw skills/knowledge/interest data into similarity matrices that power personalized job/career suggestions, alongside a built-in chatbot assistant and user authentication.

## Features

- **Personalized career recommendations** – users input their skills, knowledge, and interests; the app matches them against occupation profiles derived from O*NET data.
- **Interactive multi-page UI** built with Streamlit, including Home, About, Recommend, Chatbot, Contact, and Feedback pages.
- **AI chatbot assistant** to help users explore careers conversationally.
- **User authentication** for a personalized session experience.
- **Feedback collection** to continuously improve recommendation quality.
- **Custom UI theming** via Streamlit config and CSS styling.

## How It Works

1. Raw O*NET reference files (`Skills.txt`, `Knowledge.txt`, `Interests.txt`, `Occupation Data.txt`) are processed by scripts in `src/` to build structured matrices:
   - `build_knowledge_matrix.py`, `build_interest_Matrix.py`, `build_career_matrix.py`, and `build_matrix.py` generate CSV matrices (`job_knowledge_matrix.csv`, `interest_matrix.csv`, `career_matrix.csv`).
   - `merge_titles.py` merges occupation titles into the matrices (`career_matrix_with_titles.csv`).
2. `train_model.py` and `recommender.py` build and serve the recommendation logic on top of these matrices.
3. The Streamlit app (`app.py`) loads the trained recommender and presents an interactive UI where users provide their profile (skills, knowledge, interests) via `modules/input_module.py`.
4. `modules/recommendation.py` scores and ranks matching occupations, returning the closest career matches to the user.
5. User data (accounts, feedback) is persisted in a local SQLite database (`talent_map.db`) via `database/db.py` and `database/models.py`.

## Project Structure

```
talent-map/
├── app.py                        # Streamlit application entry point
├── requirements.txt              # Python dependencies
├── talent_map.db                 # SQLite database (users, feedback, etc.)
├── test_model.py                 # Script for testing the recommendation model
├── .streamlit/
│   └── config.toml               # Streamlit UI/theme configuration
├── data/                         # O*NET source data and generated matrices
│   ├── Skills.txt
│   ├── Knowledge.txt
│   ├── Interests.txt
│   ├── Occupation Data.txt
│   ├── career_matrix.csv
│   ├── career_matrix_with_titles.csv
│   ├── interest_matrix.csv
│   ├── job_knowledge_matrix.csv
│   └── job_skill_matrix.csv
├── database/
│   ├── db.py                     # Database connection/session handling
│   └── models.py                 # ORM / schema models
├── modules/
│   ├── input_module.py           # Collects and validates user input
│   └── recommendation.py         # Core recommendation scoring logic
├── src/
│   ├── build_career_matrix.py    # Builds the combined career matrix
│   ├── build_interest_Matrix.py  # Builds the interest matrix
│   ├── build_knowledge_matrix.py # Builds the knowledge matrix
│   ├── build_matrix.py           # Shared matrix-building utilities
│   ├── merge_titles.py           # Merges occupation titles into matrices
│   ├── recommender.py            # Recommendation model/engine
│   └── train_model.py            # Trains the recommendation model
├── styles/                       # Custom CSS for the Streamlit UI
└── views/
    ├── home.py                   # Landing page
    ├── about.py                  # About page
    ├── auth.py                   # Login/signup handling
    ├── chatbot.py                # AI chatbot assistant page
    ├── recommend.py              # Career recommendation page
    ├── feedback.py                # User feedback page
    └── contact.py                # Contact page
```

## Getting Started

### Prerequisites

- Python 3.8+
- pip

### Installation

```bash
git clone https://github.com/theasthashukla212/talent-map.git
cd talent-map
pip install -r requirements.txt
```

### Running the App

```bash
streamlit run app.py
```

The app will start locally and open in your browser (by default at `http://localhost:8501`).

### Rebuilding the Recommendation Matrices (optional)

If you update the raw O*NET data in `data/`, regenerate the matrices before running the app:

```bash
python src/build_knowledge_matrix.py
python src/build_interest_Matrix.py
python src/build_career_matrix.py
python src/merge_titles.py
python src/train_model.py
```

### Testing the Model

```bash
python test_model.py
```

## Tech Stack

- **Frontend/UI:** Streamlit
- **Backend/Logic:** Python
- **Database:** SQLite
- **Data Source:** O*NET occupational database (Skills, Knowledge, Interests, Occupation Data)

## Contributing

Contributions are welcome. Please open an issue to discuss significant changes before submitting a pull request.

## License

No license file is currently included in this repository. Please contact the repository owner for usage terms.
