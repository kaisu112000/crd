"""
Automation script to run ewfile.py with phone numbers from Lamix CSV.

Reads numbers from 'Lamix SMS  My SMS Numbers.csv', groups them into
batches of 5, and feeds each batch to 'uv run ewfile.py' automatically.

Usage:
    python run_ewfile.py                 # Process all numbers from the start
    python run_ewfile.py 100             # Start from number index 100
    python run_ewfile.py 100 200         # Process numbers from index 100 to 200
"""

import csv
import subprocess
import sys
import time
import os

# === Configuration ============================================================
CSV_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "Lamix SMS  My SMS Numbers.csv")
BATCH_SIZE = 5
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
WAIT_BETWEEN_BATCHES = 3   # seconds to wait between batches
TIMEOUT_PER_BATCH = 300    # 5 minutes timeout per batch
# ==============================================================================


def load_numbers(csv_path):
    """Read all phone numbers from the CSV 'Number' column."""
    numbers = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            num = row["Number"].strip().strip('"')
            if num:
                numbers.append(num)
    return numbers


def run_batch(batch, batch_num, total_batches):
    """Run ewfile.py with a batch of up to 5 numbers."""
    print(f"\n{'='*60}")
    print(f"  BATCH {batch_num}/{total_batches}  --  Numbers: {batch}")
    print(f"{'='*60}\n")

    # Build stdin input:
    #   - Each number on its own line
    #   - A blank line to finish number entry
    #   - An extra newline to press ENTER for "start validation"
    stdin_text = "\n".join(batch) + "\n\n\n"

    try:
        env = os.environ.copy()
        env["PYTHONIOENCODING"] = "utf-8"

        proc = subprocess.Popen(
            ["uv", "run", "ewfile.py"],
            cwd=SCRIPT_DIR,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
            env=env,
        )

        stdout, _ = proc.communicate(input=stdin_text, timeout=TIMEOUT_PER_BATCH)

        # Print the output
        if stdout:
            for line in stdout.splitlines():
                try:
                    print(f"  | {line}")
                except UnicodeEncodeError:
                    print(f"  | {line.encode('ascii', 'replace').decode()}")

        if proc.returncode != 0:
            print(f"  [!] ewfile.py exited with code {proc.returncode}")

        return proc.returncode if proc.returncode is not None else -1

    except subprocess.TimeoutExpired:
        proc.kill()
        print("  [!] Batch timed out after 5 minutes -- killed.")
        return -1
    except Exception as e:
        print(f"  [!] Error running batch: {e}")
        return -1


def main():
    # -- Load numbers ----------------------------------------------------------
    if not os.path.exists(CSV_FILE):
        print(f"[ERROR] CSV not found: {CSV_FILE}")
        sys.exit(1)

    numbers = load_numbers(CSV_FILE)
    print(f"[INFO] Loaded {len(numbers)} numbers from CSV")

    if not numbers:
        print("[ERROR] No numbers found in CSV!")
        sys.exit(1)

    # -- Parse start/end from command-line args --------------------------------
    start = 0
    end = len(numbers)

    if len(sys.argv) > 1:
        try:
            start = int(sys.argv[1])
        except ValueError:
            print("Usage: python run_ewfile.py [start_index] [end_index]")
            sys.exit(1)

    if len(sys.argv) > 2:
        try:
            end = int(sys.argv[2])
        except ValueError:
            print("Usage: python run_ewfile.py [start_index] [end_index]")
            sys.exit(1)

    numbers = numbers[start:end]
    total_batches = (len(numbers) + BATCH_SIZE - 1) // BATCH_SIZE

    print(f"[INFO] Processing numbers [{start} -> {start + len(numbers) - 1}]")
    print(f"[INFO] {len(numbers)} numbers in {total_batches} batches of {BATCH_SIZE}")
    print()

    # -- Process batches -------------------------------------------------------
    success = 0
    failed = 0

    for i in range(0, len(numbers), BATCH_SIZE):
        batch = numbers[i : i + BATCH_SIZE]
        batch_num = (i // BATCH_SIZE) + 1

        rc = run_batch(batch, batch_num, total_batches)
        if rc == 0:
            success += 1
        else:
            failed += 1

        # Brief pause between batches
        if i + BATCH_SIZE < len(numbers):
            print(f"\n  ... waiting {WAIT_BETWEEN_BATCHES}s before next batch ...\n")
            time.sleep(WAIT_BETWEEN_BATCHES)

    # -- Summary ---------------------------------------------------------------
    print(f"\n{'='*60}")
    print(f"  DONE -- {success} batches OK, {failed} batches failed")
    print(f"  Total numbers processed: {len(numbers)}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
