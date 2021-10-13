CREATE TABLE reviews (
    review_id varchar(64),
    review_text varchar(256),
    review_rating ENUM('0', '1', '2', '3', '4', '5'),
    provider_id varchar(64),
    consumer_id varchar(256)
);