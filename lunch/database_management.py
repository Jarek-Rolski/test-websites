import boto3
import json
import os
from io import BytesIO

s3_client = boto3.client('s3')

def list_json_files(bucket, folder):
        if len(folder)!=0:
            if folder[-1] != '/':
                folder = folder + '/'
        contents = []
        response = s3_client.list_objects(Bucket=bucket, Prefix = folder, Delimiter='/')
        if 'Contents' in response.keys():
            contents += response['Contents']
        while response['IsTruncated'] == True:
            token = response['NextContinuationToken']
            response = s3_client.list_objects(Bucket=bucket, Prefix = folder, Delimiter='/', ContinuationToken=token)
            if 'Contents' in response.keys():
                contents += response['Contents']
        listdir = [c['Key'] for c in contents if c['Key'][-5:]=='.json']
        if len(folder)!=0:
            listdir = [d.split(folder)[1] for d in listdir]
        return listdir

s3 = boto3.resource('s3')

def read_json(bucket, folder, filename):
        input_object = s3.Object(bucket, os.path.join(folder, filename).replace("\\", "/"))
        body_bytes = input_object.get()['Body'].read()    
        json_string = body_bytes.decode('utf-8')
        return json.loads(json_string)


def write_json(bucket, folder, filename, dictionary):
        output_file_name = os.path.join(folder, filename).replace("\\", "/")

        dictionary_bytes = json.dumps(dictionary).encode('utf-8')
        json_buffer = BytesIO(dictionary_bytes)

        object = s3.Object(bucket, output_file_name)
        object.put(Body=json_buffer.getvalue())

from datetime import datetime
bucket = os.environ["BUCKET"]
restautrants_folder = "RestaurantsDB/Restaurants"
review_folder = "RestaurantsDB/Reviews"
rating_folder = "RestaurantsDB/Rating"

def add_restaurant(name, location):
    write_json(bucket,restautrants_folder,name+".json",{'Name': name, 'location': location})

def add_review(name, text, quality, quantity, price, overall):
    timestamp = datetime.timestamp(datetime.now())
    write_json(bucket,review_folder,str(timestamp)+".json",{'Name': name, 'text': text, 'quality': quality, 'quantity': quantity, 'price': price, 'overall': overall})

def list_restaurants():
    files = list_json_files(bucket, restautrants_folder)
    restaurants = [read_json(bucket, restautrants_folder, file) for file in files]
    return restaurants

def list_reviews():
    files = list_json_files(bucket, review_folder)
    reviews = [read_json(bucket, review_folder, file) for file in files]
    return reviews

def overall_rating():
    all_reviews = list_reviews()
    names = set([review['Name'] for review in all_reviews])
    overall_r = []
    for name in names:
        reviews = [review for review in all_reviews if review['Name']==name]
        quality = [review['quality'] for review in reviews]
        quality = sum(quality)/len(quality)
        quantity = [review['quantity'] for review in reviews]
        quantity = sum(quantity)/len(quantity)
        price = [review['price'] for review in reviews]
        price = sum(price)/len(price)
        overall = [review['overall'] for review in reviews]
        overall = sum(overall)/len(overall)
        overall_r.append({'Name': name, 'quality': quality, 'quantity': quantity, 'price': price, 'overall': overall})
    return overall_r

def list_rating():
    files = list_json_files(bucket, rating_folder)
    rating = [read_json(bucket, rating_folder, file) for file in files]
    return rating

def save_rating():
    ratings = overall_rating()
    for rating in ratings:
        write_json(bucket,rating_folder,rating['Name']+".json",rating)