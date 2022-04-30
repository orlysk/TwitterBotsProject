from typing import List, Dict
import json
import requests

bearer_token = "AAAAAAAAAAAAAAAAAAAAAK%2FHbgEAAAAAcNNLTzuXuV6ThP3fz30PTJOx294%3DAGpkjKXSxcxnEzeyPJB7XVbeP20TjmLhzpdpMndBB0gIiYk5Dk"


def get_users_lookup_url(account_ids: List[str]) -> str:
    account_ids_str = ','.join(account_ids)
    url = f"https://api.twitter.com/2/users?ids={account_ids_str}"
    return url


def get_user_tweets_url(account_id: str) -> str:
    url = f"https://api.twitter.com/2/users/{account_id}/tweets"
    return url


def get_user_followers_url(account_id: str) -> str:
    url = f"https://api.twitter.com/2/users/{account_id}/followers"
    return url


def get_user_following_url(account_id: str) -> str:
    url = f"https://api.twitter.com/2/users/{account_id}/following"
    return url


def create_auth_headers() -> Dict[str, str]:
    return {"Authorization": "Bearer {}".format(bearer_token)}


def connect_to_endpoint(url: str, params: Dict[str, str]) -> Dict:
    response = requests.request("GET", url, headers=create_auth_headers(), params=params)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()


def enrich_users(accounts_ids: List[str]) -> Dict:
    users_lookup_params = {
        "user.fields": "id,name,username,created_at,description,location,pinned_tweet_id,protected,public_metrics,"
                       "verified,withheld"
    }
    users_lookup_url = get_users_lookup_url(accounts_ids)

    json_response = connect_to_endpoint(users_lookup_url, users_lookup_params)

    return json_response['data']


def get_user_tweets(account_id: str) -> Dict:
    user_tweets_params = {
        "tweet.fields": "attachments,context_annotations,conversation_id,created_at,entities,id,in_reply_to_user_id,lang,public_metrics,reply_settings,source,text",
        "max_results": 100
    }
    user_tweets_url = get_user_tweets_url(account_id)

    json_response = connect_to_endpoint(user_tweets_url, user_tweets_params)

    return json_response['data']


def get_user_followers(account_id: str) -> Dict:
    user_followers_params = {
        "user.fields": "created_at,description,entities,id,location,name,pinned_tweet_id,public_metrics,username",
        "max_results": 1000
    }
    user_tweets_url = get_user_followers_url(account_id)

    json_response = connect_to_endpoint(user_tweets_url, user_followers_params)

    return json_response['data']


def get_user_following(account_id: str) -> Dict:
    user_followers_params = {
        "user.fields": "created_at,description,entities,id,location,name,pinned_tweet_id,public_metrics,username",
        "max_results": 1000
    }
    user_following_url = get_user_following_url(account_id)

    json_response = connect_to_endpoint(user_following_url, user_followers_params)

    return json_response['data']


user_account_id = "953692489"
enriched_user = enrich_users([user_account_id])
user_tweets = get_user_tweets(user_account_id)
user_followers = get_user_followers(user_account_id)
user_following = get_user_following(user_account_id)

res = {
    "user_details": enriched_user,
    "user_tweets": user_tweets,
    "user_followers": user_followers,
    "user_following": user_following
}

with open(f"res-{user_account_id}.json", "w") as fh:
    json.dump(res, fh)
