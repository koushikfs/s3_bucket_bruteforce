# S3 Bucket Brute-force Script

This tool is used to brute-force Amazon S3 bucket names based on a provided word list. It can optionally prepend a substring to each word in the wordlist to form the bucket names. The script checks if the buckets exist and whether the user has access to them.

## Features

- Checks if S3 buckets exist.
- Prints bucket names in green if they exist.
- Prints bucket names in red if they exist but access is forbidden.
- Shows progress percentage and the number of buckets scanned.
- Supports multi-threading for faster execution.
- Allows specifying an AWS region.

## Requirements

- Python 3.x
- boto3
- colorama

## Installation

   git clone https://github.com/koushikfs/s3_bucket_bruteforce.git
   cd s3-bruteforce
   pip install -r requirements.txt

## Usage

   python3 s3_bruteforce.py /path/to/wordlist.txt [--sub SUBSTRING] [--threads THREADS] [--region REGION]
   
   --sub "**test123**"

   brute forcing:
   1. test123{wordlist_word1}
   2. test123{wordlist_word2}
   3. test123{wordlist_word3} ...continues

   --threads
   
   specify the number of threads to be used, default is **20**

   --region
   
   specify the region, default will be **eu-west-2**
