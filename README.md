# NBA Player Stats Explorer

A Streamlit web application that scrapes and analyzes NBA player statistics from Basketball-reference.com.

## Features

- 📊 **Historical Data Access**: Browse NBA player statistics from 1950 to present
- 🏀 **Team & Position Filtering**: Filter players by team and position
- 📈 **Interactive Visualizations**: Generate correlation heatmaps for statistical analysis
- 💾 **Data Export**: Download filtered data as CSV files
- 🔄 **Real-time Web Scraping**: Fetches latest data from Basketball-reference.com

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Setup

1. Clone the repository:

```bash
git clone <your-repo-url>
cd nba-stats-explorer
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

## Usage

1. Run the Streamlit app:

```bash
streamlit run app.py
```

2. Open your browser and navigate to `http://localhost:8501`

3. Use the sidebar to:

   - Select a year to analyze
   - Filter by teams (multiple selection allowed)
   - Filter by positions (C, PF, SF, PG, SG)

4. View the filtered player statistics in the main panel

5. Click "Intercorrelation Heatmap" to visualize statistical correlations

6. Use the download link to export data as CSV

## Data Source

This application scrapes data from [Basketball-reference.com](https://www.basketball-reference.com/), which provides comprehensive NBA statistics.

## Key Statistics Included

- **Basic Stats**: Games, Minutes Played, Field Goals, etc.
- **Shooting**: FG%, 3P%, FT%
- **Advanced**: PER, TS%, Usage Rate (depending on year)
- **Per Game Averages**: Points, Rebounds, Assists, Steals, Blocks

## Technologies Used

- **Streamlit**: Web application framework
- **Pandas**: Data manipulation and analysis
- **Matplotlib/Seaborn**: Data visualization
- **BeautifulSoup4**: Web scraping
- **NumPy**: Numerical computations

## Deployment

### Deploy to Streamlit Cloud

1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. Deploy with one click

### Local Deployment Notes

- Ensure stable internet connection for web scraping
- Some years may have different data formats
- Large year ranges may take time to load

## Troubleshooting

### Common Issues

1. **Data not loading**: Check internet connection and verify Basketball-reference.com is accessible
2. **Correlation heatmap error**: Ensure selected data has numeric columns
3. **Deprecated warnings**: Update to latest package versions in requirements.txt

## Future Enhancements

- [ ] Add player comparison features
- [ ] Include playoff statistics
- [ ] Add more visualization options (shot charts, trend lines)
- [ ] Implement caching for faster data retrieval
- [ ] Add export to Excel functionality
- [ ] Include team statistics analysis

## Contributing

Feel free to fork this project and submit pull requests with improvements.

## License

This project is for educational purposes. Please respect Basketball-reference.com's terms of service when using this application.

## Author

[Your Name]

## Acknowledgments

- Basketball-reference.com for providing the data
- Streamlit community for excellent documentation and support
