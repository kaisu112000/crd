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


def append_hits(hits):
    with open(HITS_FILE, "a") as f:
        for hit in hits:
            f.write(hit + "\n")


def run_batch(batch):
    input_data = "\n".join(batch) + "\n\n"

    process = subprocess.Popen(
        ["python3.12", "new.py"],   # <-- your main file
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )

    output_lines = []

    # Send numbers
    process.stdin.write(input_data)
    process.stdin.flush()
    process.stdin.close()

    # Show LIVE output
    for line in process.stdout:
        print(line, end="")
        output_lines.append(line)

    process.wait()

    return "".join(output_lines)


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

    print("=" * 60)
    print(f"Total Numbers : {total_numbers}")
    print(f"Batch Size    : {CHUNK_SIZE}")
    print(f"Total Batches : {total_batches}")
    print("=" * 60)

    batch_count = 0

    for i in range(0, total_numbers, CHUNK_SIZE):
        batch_count += 1
        batch = numbers[i:i + CHUNK_SIZE]

        print("\n" + "=" * 60)
        print(f"🚀 Processing Batch {batch_count}/{total_batches}")
        print("=" * 60)

        output = run_batch(batch)

        hits = extract_hits(output)

        if hits:
            print("\n🔥 Hits Found:", hits)
            append_hits(hits)
        else:
            print("\nNo hits this batch.")

        # Delay before next batch
        if batch_count < total_batches:
            delay = random.randint(MIN_DELAY, MAX_DELAY)
            print(f"\n⏳ Waiting {delay} seconds before next batch...\n")
            time.sleep(delay)

    print("\n✅ ALL BATCHES COMPLETED.")
    print("🎯 Finished processing all numbers.")


if __name__ == "__main__":
    main()
