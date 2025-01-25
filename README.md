# SamvidhanBot
Wisdom of the Constitution of India and its makers.

# RAG ChatBot

The RAG Chatbot helps users talk to the makers of the Indian Constitution. This is deployed using Streamlit here: [https://constitutionbot.streamlit.app/](https://constitutionbot.streamlit.app/)

The code for this is app is here: `ragchatbot.py`

I detailed the process I followed in this blog: [Medium](https://medium.com/@saikrishna_17904/e9b75282c54f)

Please feel free to give feedback on improving this. Very happy to work with others as well. Make a PR.

Few more things that have to be done:
- [ ] Conversation instead of a single query.
- [ ] Add more LLM Models.
- [ ] Train Committee reports datasets as well.


# Twitter bot

[SamvidhanBot](https://twitter.com/SamvidhanBot)

Curated by [Maximusden](https://twitter.com/Maximusden) and [Sai Krishna](https://github.com/d-saikrishna)

The debates of the Constituent Assembly, the articles in the constitution & the scholarly commentary on it are very contextualized and cannot be captured by 280 characters.

Requesting citizens to add context wherever necessary and be part of this discussion.

## How to build this twitter bot?

1. Register a Project app on the [developers portal](https://developer.twitter.com/en/portal/dashboard). Free version is enough for my app.
2. Get API_KEY, API_SECRET, ACCESS_TOKEN ACCESS_TOKEN_SECRET from the developers portal for the app. You'd use them for authentication. Save them in the environment variables. 
3. I used these two endpoints for my bot
```
tweet_url = 'https://api.twitter.com/2/tweets'
media_upload_url = 'https://upload.twitter.com/1.1/media/upload.json'
```
[tweet_url](https://developer.twitter.com/en/docs/twitter-api/tweets/manage-tweets/api-reference/post-tweets) is used to post the tweet. This is a v2 API

[media_upload_url](https://developer.twitter.com/en/docs/twitter-api/v1/media/upload-media/api-reference/post-media-upload) is used to upload media (images). This is a v1.1 API.

4. All my tweets information is stored in a google sheets. I used pygsheets to get one tweet and formatted it.

5. Uploaded the media using media_upload_url; retreived media_ids and then used the tweet_url to tweet!

6. To run the bot on every reboot of my Pi (cuz power cuts :/)

        sudo nano /etc/rc.local
        # Add the following before exit 0
        /bin/bash /path/to/your/script.sh

    I had created a run_bot.sh shell script which hsa the workflow coded.

# Blogs
1. [Scientific Temper in India](https://samvidhanbot.substack.com/p/scientific-temper-in-india): Article on Scientific temper in India, mourning the loss of Science martyrs.  
2. [Appointing the umpire](https://samvidhanbot.substack.com/p/appointing-the-umpire): Article on the Supreme Court's judgement on the appointment of the Cheif Election Commissioner. Data and Visualisations can be found at: [Link](https://github.com/d-saikrishna/SamvidhanBot/tree/main/Blogs/ElectionCommission)
