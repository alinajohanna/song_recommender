# Case Study: The site for recommendations - "Gnod"

### Scenario

We have been hired as a Data Analyst for "Gnod".

"Gnod" is a site that provides recommendations for music, art, literature and products based on collaborative filtering algorithms. Their flagship product is the _music recommender_, which you can try at [www.gnoosic.com](www.gnoosic.com). The site asks users to input 3 bands they like, and computes similarity scores with the rest of the users. Then, they recommend to the user bands that users with similar tastes have picked.

"Gnod" is a small company, and its only revenue stream so far are adds in the site. In the future, they would like to explore partnership options with music apps (such as _Deezer_, _Soundcloud_ or even _Apple Music_ and _Spotify_). However, for that to be possible, they need to expand and improve their recommendations.

That's precisely where you come. They have hired you as a Data Analyst, and they expect you to bring a mix of technical expertise and business mindset to the table.

Jane, CTO of Gnod, has sent you an email assigning you with your first task.

### Results

We have generated a song recommendation system to explore the songs that are popular on the dutch market.

The user can enter a song and gets song recommendations that
- _are actually similar to the ones they picked from an acoustic point of view._
- _are popular around the world right now (songs from the Top 100 Billboard Charts) or
- _are within the top songs in the Netherlands in 2023._


### Approach

We applied the following techniques to generate the song recommender:

- Data Collection (Web Scraping & API)
- Data Cleaning
- Feature Selection
- Dimensionality Reduction Techniques (PCA, ISOMAP, **UMAP**)
- Clustering Methods (K-Means, **DBSCAN**, HDBSCAN)

### Usage

To use the recommender follow the requirements stated in the requirements.txt file and run the song_recommender.ipynb notebook