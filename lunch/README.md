# Flask-wtforms-Example

ENVIRONMET VARIABLE: BUCKET=bucket
python main.py --root_path="/test"

run on ec2:
docker run --name lunch_time -d -p 80:8080 \
     --restart always \
     -e BUCKET="***" \
     --log-driver=awslogs \
     --log-opt awslogs-region=*** \
     --log-opt awslogs-group=*** \
     --log-opt awslogs-create-group=true \
     example-website --root_path="/lunch"

run locally:
docker run --name lunch_time -d -p 80:8080 \
     --restart always \
     -e BUCKET="***" \
     -e AWS_ACCESS_KEY_ID=*** \
     -e AWS_SECRET_ACCESS_KEY=*** \
     -e AWS_DEFAULT_REGION=*** \
     examplewebsite