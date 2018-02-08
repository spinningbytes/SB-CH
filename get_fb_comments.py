import json
import datetime
import csv
import time
from nltk.tokenize import sent_tokenize
import hashlib

try:
    from urllib.request import urlopen, Request
except ImportError:
    from urllib2 import urlopen, Request

app_id = "<APP-ID>" # Insert Id
app_secret = "<APP-SECRET>"  # Insert Secret
file_id = "facebook.csv" # the source file
result_file = "output.csv" # the target file

access_token = app_id + "|" + app_secret


def request_until_succeed(url):
    """ Fetches an URL with urlopen
    retries until success (to deal with ratelimits) """
    req = Request(url)
    success = False
    while success is False:
        try:
            response = urlopen(req)
            if response.getcode() == 200:
                success = True
        except Exception as e:
            print(e)      
            if e.file:
                data = json.loads(e.file.read())
                if 'error' in data and 'error_subcode' in data['error'] and data['error']['error_subcode'] == 33:
                    return None
            time.sleep(5)

            print("Error for URL {}: {}".format(url, datetime.datetime.now()))
            print("Retrying.")

    return response.read()


def unicode_decode(text):
    """ tries to decode unicode to deal with python unicode strangeness """
    try:
        return text.encode('utf-8').decode()
    except UnicodeDecodeError:
        return text.encode('utf-8')


def scrapeFacebookComments(file_id, result_file, access_token):
    """ Reads lines in file_id and fetches relevant facebook comments,
    using the facebook graph api, saving the result to result_file """
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
                reply = request_until_succeed(url)
                
                if not reply:
                    print("Comment doesn't exists anymore: " + row['comment_id'])
                    continue
                
                try:
                    comment = json.loads(reply)
                except:
                    comment = json.loads(reply.decode('utf-8')) #python 3.5 and earlier bugfix
                comment_contents[row['comment_id']] = comment  # cache result in case of reuse

            comment_message = '' if 'message' not in comment \
                              or comment['message'] is '' else \
                              unicode_decode(comment['message'])

            sentence_texts = sent_tokenize(comment_message,
                                           language='german')
            sentence_text = sentence_texts[int(row['sentence_number'])]

            ha = hashlib.md5(sentence_text.encode()).hexdigest()

            if ha != row['md5_hash']:
                print("Wrong MD5 hash for comment: " + row['comment_id'] + ", " + sentence_text)
                continue

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
