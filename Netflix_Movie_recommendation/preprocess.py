import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.impute import SimpleImputer


def preprocess_data(file_path):
    df = pd.read_csv(file_path)

    drop_cols = ['homepage', 'original_title', 'tagline', 'title', 'overview']
    df.drop(columns=drop_cols, inplace=True)

    numeric_cols = ['budget', 'revenue', 'runtime', 'vote_count', 'vote_average', 'popularity']
    num_imputer = SimpleImputer(strategy='median')
    df[numeric_cols] = num_imputer.fit_transform(df[numeric_cols])

    cat_cols = ['genres', 'keywords', 'original_language', 'production_companies',
                'production_countries', 'spoken_languages', 'status']
    for col in cat_cols:
        df[col] = df[col].fillna('Unknown')

    df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')
    df['release_year'] = df['release_date'].dt.year.fillna(0).astype(int)
    df.drop(columns=['release_date'], inplace=True)

    label_enc_cols = ['original_language', 'status']
    for col in label_enc_cols:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])

    multi_label_cols = ['genres', 'keywords', 'production_companies',
                        'production_countries', 'spoken_languages']
    for col in multi_label_cols:
        df[col + '_count'] = df[col].apply(lambda x: len(str(x).split('|')))
        df.drop(columns=[col], inplace=True)

    scaler = StandardScaler()
    df[numeric_cols] = scaler.fit_transform(df[numeric_cols])

    # print(df.head())
    return df
