import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime

# Page configuration
st.set_page_config(page_title='NBA Player Stats Explorer', layout='wide', initial_sidebar_state='expanded')

# Custom CSS for better styling
st.markdown("""
<style>
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
        font-size: 16px;
    }
    .stat-box {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

st.title('🏀 NBA Player Stats Explorer')

st.markdown("""
This app performs webscraping of NBA player stats data with advanced analytics!
* **Data source:** [Basketball-reference.com](https://www.basketball-reference.com/)
* **Features:** Player filtering, statistical analysis, visualizations, and data export
""")

# Sidebar configuration
st.sidebar.header('🎯 User Input Features')

# Update year range to include recent years
current_year = datetime.now().year
selected_year = st.sidebar.selectbox(
    'Select Year', 
    list(reversed(range(2000, current_year))),
    help="Choose the NBA season year"
)

# Web scraping of NBA player stats with caching
@st.cache_data(ttl=3600)  # Cache for 1 hour
def load_data(year):
    """Load NBA player statistics for a given year"""
    try:
        url = f"https://www.basketball-reference.com/leagues/NBA_{year}_per_game.html"
        html = pd.read_html(url, header=0)
        df = html[0]
        
        # Clean the data
        raw = df.drop(df[df.Age == 'Age'].index)  # Remove repeating headers
        raw = raw.fillna(0)
        playerstats = raw.drop(['Rk'], axis=1)
        
        # Convert data types
        playerstats['Team'] = playerstats['Team'].astype(str)
        playerstats['Age'] = pd.to_numeric(playerstats['Age'], errors='coerce')
        playerstats['Pos'] = playerstats['Pos'].astype(str)
        
        # Convert numeric columns
        numeric_columns = playerstats.columns.difference(['Player', 'Pos', 'Team', 'Awards'])
        for col in numeric_columns:
            playerstats[col] = pd.to_numeric(playerstats[col], errors='coerce')
        
        # Fill NaN values with 0 for numeric columns
        playerstats[numeric_columns] = playerstats[numeric_columns].fillna(0)
        
        return playerstats
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return pd.DataFrame()

# Load data with progress indicator
with st.spinner(f'Loading {selected_year} NBA season data...'):
    playerstats = load_data(selected_year)

if not playerstats.empty:
    # Sidebar filters
    st.sidebar.markdown("---")
    st.sidebar.subheader("🏀 Filters")
    
    # Team selection
    sorted_unique_team = sorted(playerstats['Team'].unique())
    default_teams = st.sidebar.checkbox('Select all teams', value=True)
    if default_teams:
        selected_team = sorted_unique_team
    else:
        selected_team = st.sidebar.multiselect(
            'Select Team(s)', 
            sorted_unique_team, 
            default=sorted_unique_team[:3],
            help="Choose one or more teams"
        )
    
    # Position selection
    unique_pos = ['C', 'PF', 'SF', 'PG', 'SG']
    default_pos = st.sidebar.checkbox('Select all positions', value=True)
    if default_pos:
        selected_pos = unique_pos
    else:
        selected_pos = st.sidebar.multiselect(
            'Select Position(s)', 
            unique_pos, 
            default=unique_pos,
            help="Choose one or more positions"
        )
    
    # Additional filters
    st.sidebar.markdown("---")
    st.sidebar.subheader("📊 Statistical Filters")
    
    # Games played filter
    min_games = st.sidebar.slider(
        'Minimum Games Played',
        min_value=0,
        max_value=82,
        value=0,
        help="Filter players by minimum games played"
    )
    
    # Points per game filter
    min_ppg = st.sidebar.slider(
        'Minimum Points Per Game',
        min_value=0.0,
        max_value=40.0,
        value=0.0,
        step=0.5,
        help="Filter players by minimum PPG"
    )
    
    # Apply filters
    df_selected = playerstats[
        (playerstats['Team'].isin(selected_team)) & 
        (playerstats['Pos'].isin(selected_pos)) &
        (playerstats['G'] >= min_games) &
        (playerstats['PTS'] >= min_ppg)
    ]
    
    # Main content area with tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Data View", "📈 Analytics", "🎯 Player Comparison", "📉 Visualizations"])
    
    with tab1:
        # Display filtered data
        st.header('Player Statistics')
        
        # Summary metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Players", len(df_selected))
        with col2:
            st.metric("Teams Selected", len(selected_team))
        with col3:
            avg_ppg = df_selected['PTS'].mean()
            st.metric("Avg PPG", f"{avg_ppg:.1f}")
        with col4:
            avg_age = df_selected['Age'].mean()
            st.metric("Avg Age", f"{avg_age:.1f}")
        
        st.markdown("---")
        
        # Display options
        col1, col2 = st.columns([1, 3])
        with col1:
            sort_by = st.selectbox(
                'Sort by:',
                ['PTS', 'TRB', 'AST', 'STL', 'BLK', 'FG%', '3P%', 'FT%'],
                help="Choose statistic to sort by"
            )
            ascending = st.checkbox('Ascending order', value=False)
        
        # Display sorted data
        df_display = df_selected.sort_values(by=sort_by, ascending=ascending)
        st.dataframe(
            df_display,
            use_container_width=True,
            height=500
        )
        
        # Download section
        st.markdown("---")
        st.subheader("💾 Download Data")
        
        col1, col2 = st.columns(2)
        with col1:
            # CSV download
            csv = df_selected.to_csv(index=False)
            b64 = base64.b64encode(csv.encode()).decode()
            href = f'<a href="data:file/csv;base64,{b64}" download="nba_stats_{selected_year}.csv">📥 Download as CSV</a>'
            st.markdown(href, unsafe_allow_html=True)
    
    with tab2:
        st.header('Statistical Analytics')
        
        # Top performers
        st.subheader('🏆 Top Performers')
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**Top Scorers**")
            top_scorers = df_selected.nlargest(5, 'PTS')[['Player', 'Team', 'PTS']]
            st.dataframe(top_scorers, hide_index=True)
        
        with col2:
            st.markdown("**Top Rebounders**")
            top_rebounders = df_selected.nlargest(5, 'TRB')[['Player', 'Team', 'TRB']]
            st.dataframe(top_rebounders, hide_index=True)
        
        with col3:
            st.markdown("**Top Assisters**")
            top_assisters = df_selected.nlargest(5, 'AST')[['Player', 'Team', 'AST']]
            st.dataframe(top_assisters, hide_index=True)
        
        st.markdown("---")
        
        # Statistical summary
        st.subheader('📊 Statistical Summary')
        
        # Select only numeric columns for statistics
        numeric_cols = df_selected.select_dtypes(include=[np.number]).columns
        stats_df = df_selected[numeric_cols].describe()
        
        st.dataframe(stats_df, use_container_width=True)
        
        # Correlation heatmap
        st.markdown("---")
        st.subheader('🔥 Correlation Heatmap')
        
        # Select key stats for correlation
        key_stats = ['PTS', 'TRB', 'AST', 'STL', 'BLK', 'FG%', '3P%', 'FT%', 'MP', 'TOV']
        available_stats = [col for col in key_stats if col in df_selected.columns]
        
        if len(available_stats) > 1:
            corr_data = df_selected[available_stats].corr()
            
            fig, ax = plt.subplots(figsize=(10, 8))
            mask = np.triu(np.ones_like(corr_data, dtype=bool))
            sns.heatmap(
                corr_data,
                mask=mask,
                annot=True,
                fmt='.2f',
                cmap='coolwarm',
                center=0,
                vmin=-1,
                vmax=1,
                square=True,
                linewidths=1,
                cbar_kws={"shrink": .8},
                ax=ax
            )
            plt.title('Player Statistics Correlation Matrix', fontsize=16, pad=20)
            plt.tight_layout()
            st.pyplot(fig)
    
    with tab3:
        st.header('Player Comparison Tool')
        
        # Player selection for comparison
        all_players = sorted(df_selected['Player'].unique())
        
        col1, col2 = st.columns(2)
        with col1:
            player1 = st.selectbox('Select First Player', all_players, index=0)
        with col2:
            player2 = st.selectbox('Select Second Player', all_players, 
                                  index=1 if len(all_players) > 1 else 0)
        
        if player1 and player2:
            # Get player data
            p1_data = df_selected[df_selected['Player'] == player1].iloc[0]
            p2_data = df_selected[df_selected['Player'] == player2].iloc[0]
            
            # Comparison metrics
            st.subheader('Head-to-Head Comparison')
            
            # Key stats to compare
            compare_stats = ['PTS', 'TRB', 'AST', 'STL', 'BLK', 'FG%', '3P%', 'FT%']
            
            col1, col2, col3 = st.columns([1, 2, 1])
            
            with col1:
                st.markdown(f"### {player1}")
                st.markdown(f"**Team:** {p1_data['Team']}")
                st.markdown(f"**Position:** {p1_data['Pos']}")
            
            with col3:
                st.markdown(f"### {player2}")
                st.markdown(f"**Team:** {p2_data['Team']}")
                st.markdown(f"**Position:** {p2_data['Pos']}")
            
            st.markdown("---")
            
            # Create comparison chart
            fig, ax = plt.subplots(figsize=(10, 6))
            
            x = np.arange(len(compare_stats))
            width = 0.35
            
            p1_values = [p1_data[stat] for stat in compare_stats]
            p2_values = [p2_data[stat] for stat in compare_stats]
            
            bars1 = ax.bar(x - width/2, p1_values, width, label=player1, color='#1f77b4')
            bars2 = ax.bar(x + width/2, p2_values, width, label=player2, color='#ff7f0e')
            
            ax.set_xlabel('Statistics')
            ax.set_ylabel('Values')
            ax.set_title('Player Statistical Comparison')
            ax.set_xticks(x)
            ax.set_xticklabels(compare_stats)
            ax.legend()
            ax.grid(True, alpha=0.3)
            
            # Add value labels on bars
            for bars in [bars1, bars2]:
                for bar in bars:
                    height = bar.get_height()
                    ax.annotate(f'{height:.1f}',
                              xy=(bar.get_x() + bar.get_width() / 2, height),
                              xytext=(0, 3),
                              textcoords="offset points",
                              ha='center', va='bottom',
                              fontsize=8)
            
            plt.tight_layout()
            st.pyplot(fig)
    
    with tab4:
        st.header('Data Visualizations')
        
        # Visualization options
        viz_type = st.selectbox(
            'Select Visualization Type',
            ['Scatter Plot', 'Distribution Plot', 'Box Plot', 'Team Statistics']
        )
        
        if viz_type == 'Scatter Plot':
            st.subheader('Scatter Plot Analysis')
            
            col1, col2 = st.columns(2)
            numeric_cols = df_selected.select_dtypes(include=[np.number]).columns.tolist()
            
            with col1:
                x_axis = st.selectbox('X-axis', numeric_cols, index=numeric_cols.index('MP') if 'MP' in numeric_cols else 0)
            with col2:
                y_axis = st.selectbox('Y-axis', numeric_cols, index=numeric_cols.index('PTS') if 'PTS' in numeric_cols else 1)
            
            fig, ax = plt.subplots(figsize=(10, 6))
            scatter = ax.scatter(df_selected[x_axis], df_selected[y_axis], 
                               c=df_selected['PTS'], cmap='viridis', 
                               s=100, alpha=0.6, edgecolors='black', linewidth=0.5)
            ax.set_xlabel(x_axis, fontsize=12)
            ax.set_ylabel(y_axis, fontsize=12)
            ax.set_title(f'{y_axis} vs {x_axis}', fontsize=14)
            ax.grid(True, alpha=0.3)
            plt.colorbar(scatter, ax=ax, label='Points Per Game')
            plt.tight_layout()
            st.pyplot(fig)
            
        elif viz_type == 'Distribution Plot':
            st.subheader('Statistical Distribution')
            
            stat_to_plot = st.selectbox(
                'Select Statistic',
                ['PTS', 'TRB', 'AST', 'STL', 'BLK', 'FG%', '3P%', 'FT%']
            )
            
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
            
            # Histogram
            ax1.hist(df_selected[stat_to_plot].dropna(), bins=30, edgecolor='black', alpha=0.7)
            ax1.set_xlabel(stat_to_plot)
            ax1.set_ylabel('Frequency')
            ax1.set_title(f'Distribution of {stat_to_plot}')
            ax1.grid(True, alpha=0.3)
            
            # Box plot by position
            positions = df_selected['Pos'].unique()
            data_by_pos = [df_selected[df_selected['Pos'] == pos][stat_to_plot].dropna() for pos in positions]
            ax2.boxplot(data_by_pos, labels=positions)
            ax2.set_xlabel('Position')
            ax2.set_ylabel(stat_to_plot)
            ax2.set_title(f'{stat_to_plot} by Position')
            ax2.grid(True, alpha=0.3)
            
            plt.tight_layout()
            st.pyplot(fig)
            
        elif viz_type == 'Box Plot':
            st.subheader('Box Plot Analysis')
            
            stat_to_plot = st.selectbox(
                'Select Statistic',
                ['PTS', 'TRB', 'AST', 'STL', 'BLK', 'MP']
            )
            
            fig, ax = plt.subplots(figsize=(12, 6))
            
            # Create box plot for each team
            teams = selected_team[:10]  # Limit to 10 teams for readability
            data_by_team = [df_selected[df_selected['Team'] == team][stat_to_plot].dropna() for team in teams]
            
            bp = ax.boxplot(data_by_team, labels=teams, patch_artist=True)
            
            # Color the boxes
            colors = plt.cm.Set3(np.linspace(0, 1, len(teams)))
            for patch, color in zip(bp['boxes'], colors):
                patch.set_facecolor(color)
            
            ax.set_xlabel('Team')
            ax.set_ylabel(stat_to_plot)
            ax.set_title(f'{stat_to_plot} Distribution by Team')
            ax.grid(True, alpha=0.3)
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            st.pyplot(fig)
            
        else:  # Team Statistics
            st.subheader('Team Performance Overview')
            
            # Aggregate team statistics
            team_stats = df_selected.groupby('Team').agg({
                'PTS': 'mean',
                'TRB': 'mean',
                'AST': 'mean',
                'STL': 'mean',
                'BLK': 'mean',
                'Player': 'count'
            }).round(1)
            team_stats.columns = ['Avg PTS', 'Avg TRB', 'Avg AST', 'Avg STL', 'Avg BLK', 'Player Count']
            team_stats = team_stats.sort_values('Avg PTS', ascending=False)
            
            # Display top teams
            st.dataframe(team_stats.head(10), use_container_width=True)
            
            # Bar chart of top scoring teams
            fig, ax = plt.subplots(figsize=(12, 6))
            top_teams = team_stats.head(10)
            x_pos = np.arange(len(top_teams))
            
            bars = ax.bar(x_pos, top_teams['Avg PTS'], color='skyblue', edgecolor='navy', linewidth=1.5)
            
            # Add value labels on bars
            for bar in bars:
                height = bar.get_height()
                ax.annotate(f'{height:.1f}',
                          xy=(bar.get_x() + bar.get_width() / 2, height),
                          xytext=(0, 3),
                          textcoords="offset points",
                          ha='center', va='bottom')
            
            ax.set_xlabel('Team')
            ax.set_ylabel('Average Points Per Game')
            ax.set_title('Top 10 Teams by Average PPG')
            ax.set_xticks(x_pos)
            ax.set_xticklabels(top_teams.index, rotation=45, ha='right')
            ax.grid(True, alpha=0.3, axis='y')
            
            plt.tight_layout()
            st.pyplot(fig)

else:
    st.error("Unable to load data. Please check your internet connection and try again.")