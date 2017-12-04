import tweepy
import os
from urllib.request import Request, urlopen
import random

consumer_key = ""
consumer_secret = ""

access_token = ""
access_token_secret = ""


def getTweet(keyword):
    # 트위터 앱의 Keys and Access Tokens 탭 참조(자신의 설정 값을 넣어준다)

    # 1. 인증요청(1차) : 개인 앱 정보
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

    # 2. access 토큰 요청(2차) - 인증요청 참조변수 이용
    auth.set_access_token(access_token, access_token_secret)

    # 3. twitter API 생성
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    search = []
    cursor = tweepy.Cursor(api.search, q=keyword + " -filter:retweets",
                           include_entities=True, result_type="recent", lang="ko",
                           ).items()
    for tweet in cursor:
        try:
            print("\rSearching...", end='')
            if 'RT @' not in tweet.text:
                if 'media' in tweet.extended_entities:
                    for media in tweet.extended_entities['media']:
                        if media['type'] == 'photo':
                            image_uri = media['media_url'] + ':large'
                            search.append(image_uri)
        except AttributeError:
            continue

    return search


def getTweetbyID(userid):
    # 트위터 앱의 Keys and Access Tokens 탭 참조(자신의 설정 값을 넣어준다)

    # 1. 인증요청(1차) : 개인 앱 정보
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

    # 2. access 토큰 요청(2차) - 인증요청 참조변수 이용
    auth.set_access_token(access_token, access_token_secret)

    # 3. twitter API 생성
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    search = []
    cursor = tweepy.Cursor(api.user_timeline, screen_name=userid,
                           include_entities=True, result_type="recent", lang="ko",
                           ).items()
    for tweet in cursor:
        try:
            print("\rSearching...", end='')
            if 'RT @' not in tweet.text:
                if '프리뷰' not in tweet.text and 'preview' not in tweet.text \
                        and 'Preview' not in tweet.text and 'PREVIEW' not in tweet.text:
                    if 'media' in tweet.extended_entities:
                        for media in tweet.extended_entities['media']:
                            if media['type'] == 'photo':
                                image_uri = media['media_url'] + ':large'
                                search.append(image_uri)
        except AttributeError:
            continue

    return search


def downloadImage(finalList):
    i = 1
    print()
    if not os.path.isdir("./downloads/"):
        os.mkdir('./downloads/')
    for url in finalList:
        print("\rDownloading... (" + str(i) + "/" + str(len(finalList)) + ")", end='')
        if not os.path.isfile("./downloads/" + url[27:-6]):
            f = open("./downloads/" + url[27:-6], "wb")
        else:
            input("중복된 파일이 존재합니다.")
            f = open("./downloads/" + url[27:-6] + "_" + str(random.randint(1, 1000000)), "wb")
        download_url = Request(url)
        f.write(urlopen(download_url).read())
        f.close()
        i += 1
    print("\n다운로드가 완료되었습니다.\n")
    main()


def main():
    print("Twitter Search Image Downloader - by lmwljw98")

    while True:
        key = input("Options : 1. 키워드 검색\n          2. 타임라인 검색 (exclude previews)\n          3. 종료 : ")
        if key == "1":
            print("※ 최근 1주일 이내의 사진만 검색이 가능합니다. ※\n")
            keyword = input("원하는 키워드를 입력하세요. : ")
            finalList = list(set(getTweet(keyword)))
            break
        elif key == "2":
            keyword = input("\n검색을 원하는 아이디를 입력하세요. : ")
            finalList = list(set(getTweetbyID(keyword)))
            break
        elif key == "3":
            return
        else:
            print("올바른 명령을 입력해주세요.\n")

    if len(finalList) > 0:
        print("\n\n%d개의 이미지가 발견되었습니다." % len(finalList))

        while True:
            answer = input("다운로드 하시겠습니까? (Y/N) : ")
            if answer == "Y" or answer == "y":
                downloadImage(finalList)
                break
            elif answer == "N" or answer == "n":
                print()
                main()
                break
            else:
                print("올바른 명령을 입력해주세요.\n")
    else:
        print("\n\n이미지를 발견하지 못하였습니다.")
        main()


if __name__ == "__main__":
    main()
