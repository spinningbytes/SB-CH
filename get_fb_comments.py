import json
import datetime
import csv
import time
from nltk.tokenize import sent_tokenize
try:
    from urllib.request import urlopen, Request
except ImportError:
    from urllib2 import urlopen, Request

app_id = "<APP_ID>" # Insert Id
app_secret = "<APP_SECRET>"  # Insert Secret
file_id = "facebook.csv"
result_file = "output.csv"

access_token = app_id + "|" + app_secret


def request_until_succeed(url):
    req = Request(url)
    success = False
    while success is False:
        try:
            response = urlopen(req)
            if response.getcode() == 200:
                success = True
        except Exception as e:
            print(e)
            time.sleep(5)

            print("Error for URL {}: {}".format(url, datetime.datetime.now()))
            print("Retrying.")

    return response.read()


def unicode_decode(text):
    try:
        return text.encode('utf-8').decode()
    except UnicodeDecodeError:
        return text.encode('utf-8')


def scrapeFacebookComments(file_id, result_file, access_token):
    with open(file_id, 'r', encoding='utf8') as f, \
            open(result_file, 'w', encoding='utf8', newline='') as o:
        input_file = csv.DictReader(f)
        output_file = csv.DictWriter(o, 
                                     fieldnames=[
                                         'sentence_id', 
                                         'sentence_text'])

        output_file.writeheader()

        num_processed = 0
        scrape_starttime = datetime.datetime.now()
        base = "https://graph.facebook.com/v2.12"
        parameters = "/?access_token={}".format(access_token)

        print("Scraping {} Comments: {}\n".format(
            file_id, scrape_starttime))

        comment_contents = {}

        for row in input_file:
            if row['comment_id'] in comment_contents:
                comment = comment_contents[row['comment_id']]
            else:
                node = "/{}".format(row['comment_id'])
                url = base + node + parameters
                comment = json.loads(request_until_succeed(url))
                comment_contents[row['comment_id']] = comment # cache result in case of reuse

            comment_message = '' if 'message' not in comment \
                              or comment['message'] is '' else \
                              unicode_decode(comment['message'])

            sentence_texts = sent_tokenize(comment_message,
                                            language='german')
            sentence_text = sentence_texts[int(row['sentence_number'])]

            output_file.writerow({'sentence_id': row['sentence_id'],
                                    'sentence_text': sentence_text})

            num_processed += 1
            if num_processed % 100 == 0:
                print("{} Comments Processed: {}".format(
                    num_processed, datetime.datetime.now()))

        print("\nDone!\n{} Comments Processed in {}".format(
            num_processed, datetime.datetime.now() - scrape_starttime))


if __name__ == '__main__':
    scrapeFacebookComments(file_id, result_file, access_token)
