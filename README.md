# Hugo to S3 using AWS Lambda
An AWS lambda function used to compile a hugo website from a git repository into a S3 bucket.

To use zip the main.py, git-2.14.0.tar, and the hugo binary then upload to AWS Lambda.

Add the following Environment variables to the function and it should work anytime it is triggered.
GIT_REPO //the full URL to the Hugo site repository
S3_BUCKET //the name of the bucket you want the content copied to when complete 

The function to install git in the Lambda is based off of the work done by [bcongdon](https://github.com/bcongdon/git_lambda).
