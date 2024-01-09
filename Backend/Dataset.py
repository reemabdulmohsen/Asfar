import pandas as pd
import re
import random

df = pd.read_excel('story.xlsx')
df = df.drop(['Article source'], axis=1)
df = df.drop(index=[12])


def clean_newlines(text):
    cleaned_text = re.sub(r'\n+', ' ', text)
    return cleaned_text


df['prompt'] = df['prompt'].apply(clean_newlines)
df['story'] = df['story'].apply(clean_newlines)
# remove the space in the beginning
df['prompt'] = df['prompt'].apply(lambda x: x.strip())
df['story'] = df['story'].apply(lambda x: x.strip())


def generate_random_story_prompt(country):
    # Filter the DataFrame based on the given country
    country_df = df[df['Country'] == country]

    # Choose a random index from the filtered DataFrame
    random_index = random.randint(0, len(country_df) - 1)

    # Get the random story and prompt based on the random index
    random_story = country_df.iloc[random_index]['story']
    random_prompt = country_df.iloc[random_index]['prompt']

    return random_story, random_prompt
