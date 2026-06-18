import os
import csv

FNAME = "Trade Statement From 2024-09-02 To 2026-06-12.csv"
IN_DIR = os.path.join('..', 'Downloads')
IN_PATH = os.path.join(IN_DIR, FNAME)
MAX_ROWS = 999

def split_csv(in_path, max_rows=999):
    if not os.path.isfile(in_path):
        raise FileNotFoundError(f"Input file not found: {in_path}")

    base = os.path.splitext(os.path.basename(in_path))[0]
    out_dir = os.path.dirname(in_path)

    with open(in_path, newline='', encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        try:
            header = next(reader)
        except StopIteration:
            return []

        part = 1
        out_paths = []
        rows_written = 0
        out_file = None
        writer = None

        def open_new():
            nonlocal part, out_file, writer, rows_written
            if out_file:
                out_file.close()
            out_name = f"{base}_part{part}.csv"
            out_path = os.path.join(out_dir, out_name)
            out_file = open(out_path, 'w', newline='', encoding='utf-8')
            writer = csv.writer(out_file)
            writer.writerow(header)
            out_paths.append(out_path)
            rows_written = 0
            part += 1
            return out_path

        open_new()
        for row in reader:
            if rows_written >= max_rows:
                open_new()
            writer.writerow(row)
            rows_written += 1

        if out_file:
            out_file.close()

    return out_paths


if __name__ == '__main__':
    try:
        outputs = split_csv(IN_PATH, MAX_ROWS)
        for p in outputs:
            print(p)
    except Exception as e:
        print('Error:', e)
