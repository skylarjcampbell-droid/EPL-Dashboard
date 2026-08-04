import streamlit as st
import pandas as pd
import plotly.express as px

st.title('English Premeir League Dashboard')

# Load the dataset
df = pd.read_csv('EPL_25-26.csv', encoding = 'cp1252')
df['team_name'] = df['team_name'].str.replace(
    '&amp;',
    '&'
)

# -----------------------------------------------------------------
# Team Colors
# -----------------------------------------------------------------
team_colors = {
    'Arsenal': '#EF0107',
    'Aston Villa': '#670E36',
    'Bournemouth': '#DA291C',
    'Brentford': '#E30613',
    'Brighton & Hove Albion': '#0057B8',
    'Burnley': '#6C1D45',
    'Chelsea': '#034694',
    'Crystal Palace': '#1B458F',
    'Everton': '#003399',
    'Fulham': '#000000',
    'Leeds United': '#FFCD00',
    'Liverpool': '#C8102E',
    'Manchester City': '#6CABDD',
    'Manchester United': '#DA291C',
    'Newcastle United': '#241F20',
    'Nottingham Forest': '#DD0000',
    'Sunderland': '#EB172B',
    'Tottenham Hotspur': '#132257',
    'West Ham United': '#7A263A',
    'Wolverhampton': '#FDB913'
}

# -----------------------------------------------------------------
# Sidebar Filters
# -----------------------------------------------------------------

st.sidebar.header('Filters')

# Team Filter
team_options = ['All'] + sorted(df['team_name'].unique().tolist())

selected_teams = st.sidebar.selectbox(
    'Select Team',
    team_options
)

# Position Filter
position_options = ['All'] + sorted(df['position'].unique().tolist())

selected_position = st.sidebar.selectbox(
    'Select Position',
    position_options
)

# Rating Filter
rating_options = ['All', '5.5-6', '6-6.5', '6.5-7', '7-7.5', '7.5-8']

selected_rating = st.sidebar.selectbox(
    'Select Rating',
    rating_options
)

# -----------------------------------------------------------------
# Apply Filters
# -----------------------------------------------------------------

filtered_df = df.copy()

# Team Filter
if selected_teams != 'All':
    filtered_df = filtered_df[
        filtered_df['team_name'] ==  selected_teams
    ]

# Position Filter
if selected_position != 'All':
    filtered_df = filtered_df[
        filtered_df['position'] == selected_position
    ]

# Rating Filter
if selected_rating == 'All':
    pass
elif selected_rating == '5.5-6':
    filtered_df = filtered_df[
        (filtered_df['rating'] >= 5.5) & (filtered_df['rating'] < 6)
    ]
elif selected_rating == '6-6.5':
    filtered_df = filtered_df[
        (filtered_df['rating'] >= 6) & (filtered_df['rating'] < 6.5)
    ]
elif selected_rating == '6.5-7':
    filtered_df = filtered_df[
        (filtered_df['rating'] >= 6.5) & (filtered_df['rating'] < 7)
    ]
elif selected_rating == '7-7.5':
    filtered_df = filtered_df[
        (filtered_df['rating'] >= 7) & (filtered_df['rating'] < 7.5)
    ]
elif selected_rating == '7.5-8':
    filtered_df = filtered_df[
        (filtered_df['rating'] >= 7.5) & (filtered_df['rating'] < 8)
    ]
# -----------------------------------------------------------------
# Create KPI Columns
# -----------------------------------------------------------------
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        'Total Players',
        filtered_df['player_name'].nunique()
    )

with col2:
    st.metric(
        'Average Rating',
        round(filtered_df['rating'].mean(), 2)
    )

with col3:
    st.metric(
        'Total Goals',
        filtered_df['goals'].sum()
    )

with col4:
    st.metric(
        'Total Assists',
        int(filtered_df['assists'].sum())
    )

# -----------------------------------------------------------------
# Charts
# -----------------------------------------------------------------

top_scorers = (
    filtered_df
    .sort_values('goals', ascending=False)
    .head(10)
)

top_assists = (
    filtered_df
    .sort_values('assists', ascending=False)
    .head(10)
)


col1, col2 = st.columns(2)


with col1:

    fig_goals = px.bar(
        top_scorers,
        x='goals',
        y='player_name',
        orientation='h',
        title='Top Goal Scorers',
        color='goals',
        color_continuous_scale='greens',
        hover_data={
            'team_name': True,
            'goals': True,
            'rating': ':.2f',
        }
    )

    fig_goals.update_layout(
        xaxis={'tickangle': 0, 'tickmode': 'array'},
        yaxis={'categoryorder':'total ascending'}
    )

    st.plotly_chart(
        fig_goals,
        use_container_width=True
    )


with col2:

    fig_assists = px.bar(
        top_assists,
        x='assists',
        y='player_name',
        orientation='h',
        title='Top Assist Providers',
        color='assists',
        color_continuous_scale='Blues',
        hover_data={
            'team_name': True,
            'assists': True,
            'rating': ':.2f',
        }
    )

    fig_assists.update_layout(
        xaxis={'tickangle': 0, 'tickmode': 'array'},
        yaxis={'categoryorder':'total ascending'}
    )

    st.plotly_chart(
        fig_assists,
        use_container_width=True
    )


# -----------------------------------------------------------------
# Team Average Rating Bar Chart
# -----------------------------------------------------------------
fig_team_rating = px.bar(
    filtered_df.groupby('team_name', as_index=False)['rating'].mean(),
    x='team_name',
    y='rating',
    title='Average Team Rating',
    color='rating',
    color_continuous_scale='purples',
    hover_data={
        'team_name': True,
        'rating': ':.2f'
    },
    range_y=[6, 7]
)
fig_team_rating.update_xaxes(tickangle=45, tickmode='array')
st.plotly_chart(
    fig_team_rating,
    use_container_width=True
)


# -----------------------------------------------------------------
# Player Performance Scatter
# -----------------------------------------------------------------

fig_scatter = px.scatter(
    filtered_df,
    x='goals',
    y='rating',
    size='assists',
    color='position',
    hover_name='player_name',
    hover_data={
        'team_name': True,
        'goals': True,
        'assists': True,
        'rating': ':.2f',
        'position': True
    },
    title='Player Rating vs Goals',
    range_y=[6, 8],
    
)

st.plotly_chart(
    fig_scatter,
    use_container_width=True
)

# -----------------------------------------------------------------
# Team Performance Comparison
# -----------------------------------------------------------------

team_summary = (
    filtered_df
    .groupby('team_name')
    .agg(
        Goals=('goals','sum'),
        Assists=('assists','sum'),
        Avg_Rating=('rating','mean')
    )
    .reset_index()
)



fig_team = px.scatter(
    team_summary,
    x='Goals',
    y='Avg_Rating',
    size='Assists',
    color='team_name',
    color_discrete_map=team_colors,
    hover_name='team_name',
    title='Team Attack vs Average Rating'
)

st.plotly_chart(
    fig_team,
    use_container_width=True
)


# -----------------------------------------------------------------
# Show Data Table
# -----------------------------------------------------------------
st.subheader('Player Data')
st.dataframe(
    filtered_df,
    use_container_width=True
)

