from instagrapi import Client
import json, time, random, os

# Reading the config file and converting it to a dictionary
with(open("config.json", "r")) as f: config = json.load(f)
print("Config File Loaded")
USERNAME = config['username']
PASSWORD = config['password']
USERS_TO_SCRAPE = config['usernameToScrape']


def userScrapeFollowLike(username, password):
    if os.name == 'nt': os.system('cls')
    else: os.system('clear')

    print("Logging into: " + username + "...")
    # Logging into the account using the config
    cl = Client()
    cl.login(username, password)
    print("Logged into: " + username)
    print("Entering 30 seconds wait")
    time.sleep(30)
    for user in USERS_TO_SCRAPE:
        print("Scraping User: " + user)
        # Getting the user's info
        userID = cl.user_id_from_username(user)
        time.sleep(5 + (random.random() * 5))

        # Getting the user's posts
        posts = cl.user_medias(int(userID), amount=5)
        time.sleep(5 + (random.random() * 5))

        # Looping through the posts
        for post in posts:
            print("    Scraping post: https://www.instagram.com/p/" + post.code)
            # Getting all the users who liked the post
            mediaLikers = cl.media_likers(post.id)
            time.sleep(5 + (random.random() * 5))

            # Loop through the likers
            for liker in mediaLikers:
                # Getting the userID from their username
                userID = cl.user_id_from_username(liker.username)
                # Checking if user is a bot (or a private account)
                userDict = cl.user_info_by_username(liker.username).dict()
                if userDict['is_private'] == False:
                    time.sleep(5 + (random.random() * 5))
                    cl.user_follow(userID)
                    time.sleep(5 + (random.random() * 5))
                    userPosts = cl.user_medias(int(userID), amount=2)
                    for userPost in userPosts:
                        cl.media_like(userPost.id)
                        time.sleep(5 + (random.random() * 5))
                    print("        Followed & Liked: " + str(liker.username))
                    time.sleep(25 + (random.random() * 5))
                else:
                    print("        Skipping Bot/Private Account: " + str(liker.username))
                    time.sleep(10 + (random.random() * 5))

    print("FINISHED")


userScrapeFollowLike(USERNAME, PASSWORD)
