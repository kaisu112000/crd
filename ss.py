import subprocess
import re
import time
import random
import math

CHUNK_SIZE = 5
NUMBERS_FILE = "n.txt"
HITS_FILE = "hits.txt"
MIN_DELAY = 5
MAX_DELAY = 10


def get_numbers():
    with open(NUMBERS_FILE, "r") as f:
        return [line.strip() for line in f if line.strip()]


def save_remaining(numbers):
    with open(NUMBERS_FILE, "w") as f:
        if numbers:
            f.write("\n".join(numbers) + "\n")


def append_hits(hits):
    with open(HITS_FILE, "a") as f:
        for hit in hits:
            f.write(hit + "\n")


def run_batch(batch):
    input_data = "\n".join(batch) + "\n\n"

    result = subprocess.run(
        ["python3.12", "new.py"],
        input=input_data,
        text=True,
        capture_output=True
    )

    return result.stdout


def extract_hits(output):
    hits = []

    pattern = re.findall(
        r"\+(\d+).*?Success\s*:\s*(\d+)/\d+",
        output,
        re.DOTALL
    )

    for number, success_count in pattern:
        if int(success_count) > 0:
            hits.append(number)

    return hits


def main():
    numbers = get_numbers()
    total_numbers = len(numbers)

    if total_numbers == 0:
        print("No numbers found.")
        return

    total_batches = math.ceil(total_numbers / CHUNK_SIZE)

    print("=" * 50)
    print(f"Total Numbers : {total_numbers}")
    print(f"Batch Size    : {CHUNK_SIZE}")
    print(f"Total Batches : {total_batches}")
    print("=" * 50)

    batch_count = 0

    while True:
        numbers = get_numbers()

        if not numbers:
            print("\n✅ All numbers processed.")
            break

        batch_count += 1
        batch = numbers[:CHUNK_SIZE]
        remaining = numbers[CHUNK_SIZE:]

        print(f"\n🚀 Processing Batch {batch_count}/{total_batches}")
        print(f"Numbers: {batch}")

        output = run_batch(batch)

        hits = extract_hits(output)

        if hits:
            print(f"🔥 Hits Found: {hits}")
            append_hits(hits)
        else:
            print("No hits this batch.")

        save_remaining(remaining)

        print(f"Remaining numbers: {len(remaining)}")

        if remaining:
            delay = random.randint(MIN_DELAY, MAX_DELAY)
            print(f"⏳ Waiting {delay} seconds before next batch...")
            time.sleep(delay)


if __name__ == "__main__":
    main()
