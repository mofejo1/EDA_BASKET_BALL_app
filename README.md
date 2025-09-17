# NBA Player Stats Explorer

A Streamlit web application that scrapes and analyzes NBA player statistics from Basketball-reference.com. This project includes both a basic version and an optimized version with advanced analytics features.

## 📁 Project Structure

```
BASKETBALLEDA/
├── EDA_BASKET_BALL_app.py      # Basic version
├── OPTIMIZED_EDA_APP.py        # Enhanced version with advanced features
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
└── .gitignore                  # Git ignore file
```

## 🎯 Features

### Basic Version (`EDA_BASKET_BALL_app.py`)

- 📊 **Historical Data Access**: Browse NBA player statistics from 2020 to present
- 🏀 **Team & Position Filtering**: Filter players by team and position
- 📈 **Correlation Heatmap**: Generate correlation matrix for statistical analysis
- 💾 **Data Export**: Download filtered data as CSV files
- 🔄 **Real-time Web Scraping**: Fetches latest data from Basketball-reference.com

### Optimized Version (`OPTIMIZED_EDA_APP.py`)

All basic features plus:

- 📊 **Tabbed Interface**: Organized content in 4 main tabs
- 🎯 **Player Comparison Tool**: Head-to-head player comparisons
- 📈 **Advanced Analytics**: Top performers, statistical summaries
- 📉 **Multiple Visualizations**: Scatter plots, distribution plots, box plots, team statistics
- 🔍 **Enhanced Filtering**: Minimum games played, minimum PPG filters
- 📱 **Responsive Design**: Wide layout with better UI/UX
- ⚡ **Performance**: Data caching for faster loading

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Setup

1. Clone the repository:

```bash
git clone https://github.com/mofejo1/EDA_BASKET_BALL_app.git
cd EDA_BASKET_BALL_app
```

2. Create a virtual environment:

```bash
python -m venv venv
```

3. Activate the virtual environment:

- Windows:

```bash
venv\Scripts\activate
```

- Mac/Linux:

```bash
source venv/bin/activate
```

4. Install dependencies:

```bash
pip install -r requirements.txt
```

## 💻 Usage

### Running the Basic Version

```bash
streamlit run EDA_BASKET_BALL_app.py
```

### Running the Optimized Version

```bash
streamlit run OPTIMIZED_EDA_APP.py
```

The app will open in your browser at `http://localhost:8501`

## 📊 Application Guide

### Basic Version Interface

1. **Year Selection**: Choose any NBA season from 2020 to current year
2. **Team Filter**: Select one or multiple teams
3. **Position Filter**: Choose player positions (C, PF, SF, PG, SG)
4. **Data Display**: View filtered statistics in an interactive table
5. **Download**: Export data as CSV
6. **Heatmap**: Click button to generate correlation matrix

### Optimized Version Interface

#### Tab 1: Data View 📊

- Summary metrics (total players, teams, averages)
- Sortable data table
- CSV download functionality

#### Tab 2: Analytics 📈

- Top 5 scorers, rebounders, and assisters
- Statistical summary of all numeric columns
- Enhanced correlation heatmap with annotations

#### Tab 3: Player Comparison 🎯

- Select two players for head-to-head comparison
- Visual bar chart comparison
- Key statistics side-by-side

#### Tab 4: Visualizations 📉

- **Scatter Plot**: Analyze relationship between any two statistics
- **Distribution Plot**: View statistical distributions with histograms
- **Box Plot**: Compare statistics across teams or positions
- **Team Statistics**: Aggregate team performance overview

## 📈 Data Source

This application scrapes data from [Basketball-reference.com](https://www.basketball-reference.com/), which provides comprehensive NBA statistics including:

- **Basic Stats**: Games, Minutes Played, Field Goals
- **Shooting**: FG%, 3P%, FT%
- **Counting Stats**: Points, Rebounds, Assists, Steals, Blocks
- **Advanced Metrics**: Available for recent seasons

## 🛠️ Technologies Used

- **Streamlit**: Web application framework
- **Pandas**: Data manipulation and analysis
- **Matplotlib/Seaborn**: Data visualization
- **BeautifulSoup4**: Web scraping
- **NumPy**: Numerical computations
- **lxml/html5lib**: HTML parsing

## ⚠️ Known Issues & Solutions

### Common Issues

1. **AttributeError with 'Tm' column**: Fixed - Basketball Reference changed column name from 'Tm' to 'Team'
2. **Deprecation warnings**: Fixed - Updated to use `@st.cache_data` instead of `@st.cache`
3. **Type errors in sorting**: Fixed - Convert Team column to string type before sorting

## 🚀 Deployment

### Deploy to Streamlit Cloud

1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. Deploy with one click

### Local Deployment Notes

- Ensure stable internet connection for web scraping
- Some older years may have different data formats
- Large year ranges may take time to load

## 📝 Version Comparison

| Feature                 | Basic Version | Optimized Version |
| ----------------------- | ------------- | ----------------- |
| Data Scraping           | ✅            | ✅                |
| Team/Position Filters   | ✅            | ✅                |
| CSV Export              | ✅            | ✅                |
| Correlation Heatmap     | ✅            | ✅ Enhanced       |
| Statistical Filters     | ❌            | ✅                |
| Player Comparison       | ❌            | ✅                |
| Multiple Visualizations | ❌            | ✅                |
| Tabbed Interface        | ❌            | ✅                |
| Data Caching            | ❌            | ✅                |
| Top Performers          | ❌            | ✅                |

## 🔮 Future Enhancements

- [ ] Add playoff statistics
- [ ] Include player shooting charts
- [ ] Add season-over-season comparisons
- [ ] Implement player career trajectories
- [ ] Add export to Excel functionality
- [ ] Include advanced analytics (PER, TS%, Usage Rate)
- [ ] Add team vs team comparisons
- [ ] Implement player search functionality

## 🤝 Contributing

Feel free to fork this project and submit pull requests with improvements.

## 📜 License

This project is for educational purposes. Please respect Basketball-reference.com's terms of service when using this application.

## 👤 Author

**Mofe**

- 📧 Email: Eyinimofe98@gmail.com
- 💻 GitHub: [https://github.com/mofejo1/EDA_BASKET_BALL_app](https://github.com/mofejo1/EDA_BASKET_BALL_app)

## 🙏 Acknowledgments

- Basketball-reference.com for providing the data
- Streamlit community for excellent documentation
- Data science learning community for inspiration
