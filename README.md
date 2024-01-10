# SamvidhanBot
Tweeting the wisdom of the Constitution of India and its makers.

[Link](https://twitter.com/SamvidhanBot)

Curated by [Maximusden](https://twitter.com/Maximusden) and [Sai Krishna](https://github.com/d-saikrishna)

The debates of the Constituent Assembly, the articles in the constitution & the scholarly commentary on it are very contextualized and cannot be captured by 280 characters.

Requesting citizens to add context wherever necessary and be part of this discussion.

# Blogs
1. [Scientific Temper in India](https://samvidhanbot.substack.com/p/scientific-temper-in-india): Article on Scientific temper in India, mourning the loss of Science martyrs.  
2. [Appointing the umpire](https://samvidhanbot.substack.com/p/appointing-the-umpire): Article on the Supreme Court's judgement on the appointment of the Cheif Election Commissioner. Data and Visualisations can be found at: [Link](https://github.com/d-saikrishna/SamvidhanBot/tree/main/Blogs/ElectionCommission)


# How to build the bot?

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