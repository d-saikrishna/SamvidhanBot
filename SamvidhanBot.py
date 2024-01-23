import pygsheets
import random
from decouple import config
import os
import time
import requests
from requests_oauthlib import OAuth1


dir = "/home/chaoticneuron/SamvidhanBot"
def tweet_constititution_wisdom():

    consumer_key = config('consumer_key')
    consumer_secret = config('consumer_secret')
    access_token = config('access_token')
    access_token_secret = config('access_token_secret')

    oauth = OAuth1(
        consumer_key,
        client_secret=consumer_secret,
        resource_owner_key=access_token,
        resource_owner_secret=access_token_secret
        )

    # Twitter API endpoints
    tweet_url = 'https://api.twitter.com/2/tweets'
    media_upload_url = 'https://upload.twitter.com/1.1/media/upload.json'

    # MAKE TWEET
    gc = pygsheets.authorize(service_file=dir+r'/constitutionbot-3e833b17dba1.json')
    sh = gc.open('ConstitutionBot')
    wks = sh.worksheet('title', 'Sheet1')
    df = wks.get_as_df()
    df = df[(df['Length'] <= 275) & (df['Length'] > 0)].reset_index(drop=True)
    n = random.randint(0, df.shape[0] - 1)

    files = os.listdir(dir+r'/Media/')
    if (df['Author'][n] == 'NA'):
        tweet = str(df['Tweet'][n])
        author_images = [k for k in files if 'fact' in k]
    elif (df['Author'][n] == 'Shri Prem Behari Narain Raizada') or (df['Author'][n] == 'Raghu Vira') \
            or (df['Author'][n] == 'women') or (df['Author'][n] == 'words') \
            or ('Article' in df['Author'][n]) or (df['Author'][n] == 'Gandhi') or (
            df['Author'][n] == 'Narayan Agarwal'):
        tweet = str(df['Tweet'][n])
        author_images = [k for k in files if df['Author'][n] in k]
    else:
        tweet = '"' + str(df['Tweet'][n]) + '" - ' + str(df['Author'][n])
        try:
            author_images = [k for k in files if df['Author'][n] in k]
        except:
            pass

    tweet = tweet
    #print(type(df['Author'][n]))
    #print(author_images)
    #print(tweet)
    # Upload the image
    
    


    try:
        filename = author_images[random.randint(0, len(author_images) - 1)]
        image_path = dir+r'/Media/'+filename
        files = {'media': (filename+'.jpg', open(image_path, 'rb'))}
        media_response = requests.post(media_upload_url, auth=oauth, files=files)
        media_id = media_response.json()['media_id_string']
        tweet_data = {
                        'text': tweet,
                        'media': {'media_ids':[media_id]}
                        }

    except:
        tweet_data = {
                        'text': tweet
                        }
    
    # Making the request
    tweet_response = requests.post(tweet_url, auth=oauth, json=tweet_data)


def run():
    while True:
        tweet_constititution_wisdom()
        time.sleep(7200)

if __name__ == "__main__":
    run()
