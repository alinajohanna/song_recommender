import pandas as pd
import numpy as np
import pickle

import time
from config import client_id, client_secret
import spotipy as sp
from spotipy.oauth2 import SpotifyClientCredentials
from scipy.spatial import distance_matrix
import plotly.graph_objects as go

sp = sp.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))

X_umap_transformed_df = pd.read_csv('umap_df.csv').drop(columns="Unnamed: 0")

def recommender2(df) -> None:
    while True:
        # Enter a song title
        song = input('Please enter the name of a song or an artist: ')

        # Searching the song on Spotify
        try:
            results = sp.search(q=song, limit=1)
            song_id = [results['tracks']['items'][0]['id']]
            print('Processing track...')
        except:
            print("Song not found! Please try again.")
            continue

        try:
            features = sp.audio_features(tracks=song_id)
            feature_df = pd.DataFrame(features)
            print('Retrieving audio features...')
        except:
            print("Error processing tracks")
            continue

        columns_to_drop = ['type', 'id', 'uri', 'track_href', 'analysis_url', 'duration_ms', 'time_signature']
        feature_df = feature_df.drop(columns=columns_to_drop)

        # Load scaler and transform data
        with open('audio_features.pickle', 'rb') as f:
            loaded_scaler = pickle.load(f)
            X = pd.DataFrame(loaded_scaler.transform(feature_df))

        # Load the UMAP model
        with open('umap_model.pickle', 'rb') as file:
            loaded_reducer = pickle.load(file)

        # Use the loaded UMAP model to transform new data
        song_umap_transformed = loaded_reducer.transform(X)
        song_umap_transformed_df = pd.DataFrame(song_umap_transformed, columns=["UMAP_1", "UMAP_2"])

        d = distance_matrix(song_umap_transformed_df, X_umap_transformed_df)
        closest_song_to_user_song = np.argmin(d)

        song_cluster = df.iloc[closest_song_to_user_song, -1]

        suggestions = df[df['cluster'] == song_cluster].sample(5)
        url = "https://open.spotify.com/intl-de/track/"+suggestions['id'].values[0]
        print(f"Here is a recommended song: {suggestions['title'].values[0]} by {suggestions['artist'].values[0]}")
        print(f"Listen to it here: {url}")
        
        # Show the graph for the audio features of the suggested song
        suggestions = suggestions[['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo']]
        suggested_song_features = suggestions.iloc[0]

        
        #plot it
        suggested_song_df = pd.DataFrame(dict(
            r=suggested_song_features,
            theta=['danceability', 'energy', 'key', 'loudness', 'mode',
                   'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo']
        ))
        
        your_song_df = pd.DataFrame(dict(
            r=feature_df.iloc[0],
            theta=['danceability', 'energy', 'key', 'loudness', 'mode',
                   'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo']
        ))

        fig = go.Figure()
        #fig = make_subplots(rows=1, cols=2, specs=[[{'type': 'polar'}]*2])

        fig.add_trace(go.Scatterpolar(
            name = "you song",
            r=your_song_df['r'],
            theta=your_song_df['theta'],
            fill='toself',
            line_color='lightsteelblue'
        ))
        
        fig.add_trace(go.Scatterpolar(
            name = "suggested song",
            r=suggested_song_df['r'],
            theta=suggested_song_df['theta'],
            fill='toself',
            line_color='orange'
        ))
        

        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                ),
            ),
            showlegend=True,
            title="See how your songs audio features compare to the suggested song features:",
        )

        fig.show()

        user_feedback = input('Type "next" if you want to explore more amazing music. If not then type "end": ')
        if user_feedback == 'end':
            print("Great! Enjoy listening to the song!")
            break
        elif user_feedback == 'next':
            continue
        else:
            print('Invalid input. Please type "next" or "end".')
            continue
