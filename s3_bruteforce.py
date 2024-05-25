import boto3
import re
import argparse
from botocore.exceptions import ClientError
from concurrent.futures import ThreadPoolExecutor, as_completed
from colorama import Fore, Style, init
import threading


init(autoreset=True)


bucket_name_regex = re.compile(r'^[a-zA-Z0-9.\-_]{1,255}$')
arn_regex = re.compile(r'^arn:(aws).*:(s3|s3-object-lambda):[a-z\-0-9]*:[0-9]{12}:accesspoint[/:][a-zA-Z0-9\-.]{1,63}$|^arn:(aws).*:s3-outposts:[a-z\-0-9]+:[0-9]{12}:outpost[/:][a-zA-Z0-9\-]{1,63}[/:]accesspoint[/:][a-zA-Z0-9\-]{1,63}$')

progress_lock = threading.Lock()
progress_count = 0

def check_bucket(bucket_name, region):
    s3 = boto3.client('s3', region_name=region)
    try:
        s3.head_bucket(Bucket=bucket_name)
        return Fore.GREEN + f"Bucket found: {bucket_name}" + Style.RESET_ALL
    except ClientError as e:
        error_code = int(e.response['Error']['Code'])
        if error_code == 404:
            return None
        elif error_code == 403:
            return Fore.RED + f"Bucket exists but access is forbidden: {bucket_name}" + Style.RESET_ALL
        else:
            return f"Error checking bucket {bucket_name}: {e}"

def validate_and_check_bucket(name, sub, region):
    bucket_name = f"{sub}{name}" if sub else name
    if bucket_name_regex.match(bucket_name) or arn_regex.match(bucket_name):
        return check_bucket(bucket_name, region)
    else:
        return f"Invalid bucket name: {bucket_name}"

def main(wordlist, sub, num_threads, region):
    global progress_count
    with open(wordlist, 'r') as file:
        words = [line.strip() for line in file]
    total_buckets = len(words)

    def update_progress():
        global progress_count
        with progress_lock:
            progress_count += 1
            percentage = (progress_count / total_buckets) * 100
            print(Fore.GREEN + f"{percentage:.2f}% completed - {progress_count} buckets scanned", end='\r', flush=True)

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        future_to_bucket = {executor.submit(validate_and_check_bucket, word, sub, region): word for word in words}
        try:
            for future in as_completed(future_to_bucket):
                try:
                    result = future.result()
                    if result:
                        print("\n" + result)
                    update_progress()
                except Exception as exc:
                    print(f'Generated an exception: {exc}')
        except KeyboardInterrupt:
            pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="S3 Bucket Brute-force Script")
    parser.add_argument('wordlist', type=str, help='Path to the wordlist file')
    parser.add_argument('--sub', type=str, default='', help='Substring to prepend to each word')
    parser.add_argument('--threads', type=int, default=20, help='Number of concurrent threads')
    parser.add_argument('--region', type=str, default='eu-west-2', help='AWS region to use')
    args = parser.parse_args()
    main(args.wordlist, args.sub, args.threads, args.region)

