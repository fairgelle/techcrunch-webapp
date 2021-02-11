import pandas as pd
import plotly.graph_objs as go
from datetime import datetime

# Use this file to read in your data and prepare the plotly visualizations. The path to the data files are in
# `data/file_name.csv`

def return_figures():
    """Creates four plotly visualizations

    Args:
        None

    Returns:
        list (dict): list containing the four plotly visualizations

    """

    # first chart plots top 5 post category
    # as a bar chart
    
    df = pd.read_csv("./data/techcrunch_posts.csv", parse_dates=['date'])
    count_per_category = df["category"].value_counts().sort_values(ascending=False)
    count_per_category = count_per_category.reset_index().head(5)
    
    count_per_category.columns = ['category', 'post_count']
    
    graph_one = []
    graph_one.append(
      go.Bar(
        x = count_per_category.category.tolist(),
        y = count_per_category.post_count.tolist()
      )
    )
    
    layout_one = dict(title = 'Top 5 post category',
                      xaxis = dict(title = 'Category'),
                      yaxis = dict(title = 'Post Count')
                )

   # second chart plots post count over the years
   # as a line chart

    # truncating the date into year YYYY-MM-DD
    df["year"] = df["date"].apply(lambda dt: dt.replace(day=1, month=1))
    
    count_by_year = df["year"].value_counts().reset_index()
    count_by_year.columns = ['year', 'post_count']
    count_by_year = count_by_year.sort_values(by=['year'])
    
    count_by_year.columns = ['year', 'post_count']
    
    graph_two = []

    graph_two.append(
      go.Scatter(
        x = count_by_year['year'].dt.strftime('%b %Y').tolist(),
        y = count_by_year['post_count'].tolist()
      )
    )

    layout_two = dict(title = 'Post count over the years',
                      xaxis = dict(title = 'Year'),
                      yaxis = dict(title = 'Post Count')
                 )
    
    # third chart plots the median post count per year
    # as a a line chart
        
    yearly_post_count_by_author = df.value_counts(subset=['year', 'authors']).reset_index()
    yearly_post_count_by_author.columns = ['year', 'author', 'post_count']
    median_post_count_by_year = yearly_post_count_by_author.groupby(yearly_post_count_by_author["year"])["post_count"].median()

    median_post_count_by_year = median_post_count_by_year.reset_index()
    
    graph_three = []

    graph_three.append(
    go.Scatter(
        x = median_post_count_by_year.year.tolist(),
        y = median_post_count_by_year.post_count.tolist()
      )
    )
    
    layout_three = dict(title = 'Median Post Count by Year',
                    xaxis = dict(title = 'Year'),
                    yaxis = dict(title = 'Post Count')
                  )
    
    # fourth chart plots post count for each author
    # as a bar chart
    
    count_by_authors = df["authors"].value_counts().reset_index()
    count_by_authors.columns = ['author', 'post_count']
    count_by_authors = count_by_authors.sort_values(by=['post_count'], ascending=False)

    count_by_authors = count_by_authors.head()
    
    graph_four = []
    graph_four.append(
        go.Bar(
            x = count_by_authors.post_count.tolist(),
            y = count_by_authors.author.tolist(),
            orientation='h'
        )
    )
    
    layout_four = dict(title = 'Top 5 most active authors',
                        xaxis = dict(title = 'Post Count'),
                        yaxis = dict(title = 'Authors', autorange="reversed", automargin=True),
                   )
    
    #fifth chart of number of authors
    #as a big ass number
    
    authors_countd = df['authors'].nunique()
    
    graph_five = []
    
    graph_five.append(
        go.Figure(
            go.Indicator(
                mode = "number",
                value = authors_countd,
                delta = {'position': "top", 'reference': 320},
                domain = {'x': [0, 1], 'y': [0, 1]}
            )
        )
    )
    
    layout_five = []
    
    # append all charts to the figures list
    figures = []
    figures.append(dict(data=graph_one, layout=layout_one))
    figures.append(dict(data=graph_two, layout=layout_two))
    figures.append(dict(data=graph_three, layout=layout_three))
    figures.append(dict(data=graph_four, layout=layout_four))
    figures.append(dict(data=graph_five, layout=layout_five))

    return figures
