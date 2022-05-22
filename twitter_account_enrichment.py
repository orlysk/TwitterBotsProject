from typing import List, Dict
import pandas as pd
import json
import requests

bearer_token1 = "AAAAAAAAAAAAAAAAAAAAAK%2FHbgEAAAAAcNNLTzuXuV6ThP3fz30PTJOx294%3DAGpkjKXSxcxnEzeyPJB7XVbeP20TjmLhzpdpMndBB0gIiYk5Dk"
bearer_token2 = "AAAAAAAAAAAAAAAAAAAAACxLcAEAAAAA%2FBABpl1rAAUCCN%2F7ClajopC%2BgZw%3DAmKhcPF9A1qoMvtfrlAjQiVfy3RiiNJKEJvhT2uBgr5Obd0n10"


def get_users_lookup_url(account_ids: List[str]) -> str:
    account_ids_str = ','.join(account_ids)
    url = f"https://api.twitter.com/2/users?ids={account_ids_str}"
    return url


def get_user_tweets_url(account_id: str) -> str:
    # Returns most recent
    url = f"https://api.twitter.com/2/users/{account_id}/tweets"
    return url


def get_user_followers_url(account_id: str) -> str:
    url = f"https://api.twitter.com/2/users/{account_id}/followers"
    return url


def get_user_following_url(account_id: str) -> str:
    url = f"https://api.twitter.com/2/users/{account_id}/following"
    return url


def create_auth_headers() -> Dict[str, str]:
    return {"Authorization": "Bearer {}".format(bearer_token2)}


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
        "user.fields": "id,username,created_at,description,location,pinned_tweet_id,protected,public_metrics,"
                       "verified,withheld"
    }

    users_lookup_url = get_users_lookup_url(accounts_ids)
    print(users_lookup_url)

    json_response = connect_to_endpoint(users_lookup_url, users_lookup_params)

    if 'data' in json_response:
        return json_response['data']


def get_user_tweets(account_id: str) -> Dict:
    user_tweets_params = {
        "tweet.fields": "attachments,context_annotations,conversation_id,created_at,entities,id,in_reply_to_user_id,lang,public_metrics,reply_settings,source,text,referenced_tweets",
        "max_results": 10
    }
    user_tweets_url = get_user_tweets_url(account_id)

    json_response = connect_to_endpoint(user_tweets_url, user_tweets_params)

    if 'data' in json_response:
        return json_response['data']


def get_user_followers(account_id: str) -> Dict:
    user_followers_params = {
        "user.fields": "created_at,description,id,location,name,pinned_tweet_id,public_metrics,username",
        "max_results": 1000
    }
    user_tweets_url = get_user_followers_url(account_id)

    json_response = connect_to_endpoint(user_tweets_url, user_followers_params)

    if 'data' in json_response:
        return json_response['data']


def get_user_following(account_id: str) -> Dict:
    user_followers_params = {
        "user.fields": "created_at,description,entities,id,location,name,pinned_tweet_id,public_metrics,username",
        "max_results": 1000
    }
    user_following_url = get_user_following_url(account_id)

    json_response = connect_to_endpoint(user_following_url, user_followers_params)

    if 'data' in json_response:
        return json_response['data']


def create_single_account_file():
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


def get_accounts_enriched(accounts_ids: List[str]):
    enriched_users = []
    try:
        for i in range(0, len(accounts_ids), 100):
            current_account_ids = accounts_ids[i:i+100]
            enriched_users_res = enrich_users(current_account_ids)
            if enriched_users_res:
                enriched_users.extend(enriched_users_res)
    except Exception as e:
        print(f"error: {e}")
        return enriched_users

    return enriched_users


def get_accounts_tweets(accounts_ids: List[str]):
    tweets_per_account = {}
    try:
        for account_id in accounts_ids:
            current_account_tweets_res = get_user_tweets(account_id)
            tweets_per_account[account_id] = current_account_tweets_res
    except Exception as e:
        print(f"error: {e}")
        return tweets_per_account

    return tweets_per_account


def get_accounts_followers(accounts_ids: List[str]):
    followers_per_account = {}
    try:
        for account_id in accounts_ids:
            current_account_followers_res = get_user_followers(account_id)
            followers_per_account[account_id] = current_account_followers_res
    except Exception as e:
        print(f"error: {e}")
        return followers_per_account

    return followers_per_account


def get_accounts_followings(accounts_ids: List[str]):
    following_per_account = {}
    try:
        for account_id in accounts_ids:
            current_account_following_res = get_user_following(account_id)
            following_per_account[account_id] = current_account_following_res
    except Exception as e:
        print(f"error: {e}")
        return following_per_account

    return following_per_account


def create_accounts_details_csv():
    # dt18 = pd.read_csv("data_sets/original_data_sets/midterm-2018/midterm-2018.csv")
    dt18 = pd.read_csv("data_sets/original_data_sets/twitter_human_bots_dataset/twitter_human_bots_dataset.csv")
    accounts_ids = [str(i) for i in dt18.id.tolist()]
    enriched_users = get_accounts_enriched(accounts_ids)

    columns_names = ["id", "username", "created_at", "description", "location", "pinned_tweet_id", "protected",
                     "following_count", "tweet_count", "listed_count", "verified", "withheld", "account_type"]
    new_data = {column_name: [] for column_name in columns_names}

    for row in enriched_users:
        current_account_id = int(row['id'])
        for column_name in columns_names:
            if column_name == "account_type":
                new_data[column_name].append(dt18.loc[dt18['id'] == current_account_id].account_type.iloc[0])
            elif column_name in ("following_count", "tweet_count", "listed_count"):
                new_data[column_name].append(row["public_metrics"][column_name])
            else:
                new_data[column_name].append(row.get(column_name))
