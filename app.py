from logging import debug
from flask import Flask, request
import os
import psycopg2
import uuid
import json
from flask_cors import CORS

app = Flask(__name__)
# https://stackoverflow.com/a/64657739
CORS(app, support_credentials=True)
# https://devcenter.heroku.com/articles/heroku-postgresql#connecting-in-python

DATABASE_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL, sslmode='require')
# https://stackoverflow.com/a/43634941
conn.autocommit = True

cursor = conn.cursor()
try:
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS reviews (
        review_id varchar(64) PRIMARY KEY ,
        review_text varchar(256),
        review_rating ENUM('0', '1', '2', '3', '4', '5'),
        provider_id varchar(64),
        consumer_id varchar(256)
    );
    ''')
except psycopg2.Error:
    print('Error occurred while creating table')

@app.route('/health-check')
def health_check():
    return {'status': 200}

@app.route('/create-reveiw', methods=['POST'])
def create_review():
    pass
    # https://stackoverflow.com/a/67461897
    data = request.get_json()
    review_id = str(uuid.uuid4())
    consumer_id = data['consumer_id']
    provider_id = data['provider_id']
    review_text = data['review_text']
    review_rating = data['review_rating']
    query = '''
        INSERT INTO reviews (review_id, review_text, review_rating, provider_id, consumer_id)
        VALUES (%s, %s, %s, %s, %s)
    '''
    cursor.execute(query, [review_id, review_text, review_rating, provider_id, consumer_id])
    conn.commit()
    return {'status': 201, 'service_id': review_id}

@app.route('/delete-review/<review-id>', methods=['DELETE'])
def delete_review(review_id):
    query = '''
        DELETE FROM reviews WHERE review_id=%s
    '''
    cursor.execute(query, [str(review_id)])
    conn.commit()
    return {'status': 200}

@app.route('/get-all-reveiws/<user_id>')
def delete_service(user_id):
    query = '''
            SELECT * FROM reviews WHERE provider_id=%s
        '''
    cursor.execute(query, [str(user_id)])
    res = cursor.fetchAll()
    return {'status': 200, 'reviews': publish_reviews(res)}

# Helper functions
def publish_reviews(reviews):
    if len(reviews) == 0:
        return None
    res = []
    for r in reviews:
        res.append({
            'review_id': r[0],
            'review_text': r[1],
            'review_rating': r[2],
            'provider_id': r[3],
            'consumer_id': r[4]
        })
    return res

# https://www.youtube.com/watch?v=4eQqcfQIWXw
if __name__ == '__main__':
    port = os.environ.get('PORT', 5000)
    app.run(debug=True, host='0.0.0.0', port=port)