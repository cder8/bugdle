from fastapi import FastAPI, Form
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import json, os, tempfile, subprocess, datetime, sys, random
from pathlib import Path
#from datetime import datetime


print(os.getcwd())
app = FastAPI(title="Bugdle")

BASE_DIR = Path(__file__).parent
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

PUZZLE_DIR = BASE_DIR / "puzzles"

def evaluate_submission(user_fix_line, correct_fix_line, user_code, correct_code):
    """
    Compare user's fix vs. the correct fix line.
    Returns one of: 'green', 'yellow', or 'none'
    """
    if user_fix_line != correct_fix_line:
        return "none"   # wrong line entirely
    elif user_code.strip() == correct_code.strip():
        return "green"  # correct line + correct fix
    else:
        return "yellow" # correct line but wrong fix


def get_daily_puzzle_name():
    # Rotate daily based on date
    puzzles = sorted(f for f in os.listdir(PUZZLE_DIR) if f.endswith(".json"))
    day_index = datetime.date.today().toordinal() % len(puzzles)
    return puzzles[day_index]


def load_daily_puzzle():
    path = os.path.join(PUZZLE_DIR, get_daily_puzzle_name())
    with open(path) as f:
        return json.load(f)


@app.get("/")
def home():
    return FileResponse("static/index.html")


@app.get("/puzzle")
def get_puzzle():
    p = load_daily_puzzle()
    return {
        "id": p["id"],   # <-- include id
        "title": p["title"],
        "description": p["description"],
        "snippet": p["snippet"],
        "difficulty": p.get("difficulty", "Unknown")
    }


@app.get("/puzzle/random")
def get_random_puzzle():
    puzzles = sorted(f for f in os.listdir(PUZZLE_DIR) if f.endswith(".json"))
    filename = random.choice(puzzles)
    path = os.path.join(PUZZLE_DIR, filename)
    with open(path) as f:
        puzzle = json.load(f)
    return {
        "id": puzzle["id"],  # <-- include id
        "title": puzzle["title"],
        "description": puzzle["description"],
        "snippet": puzzle["snippet"],
        "difficulty": puzzle.get("difficulty", "Unknown")
    }


@app.post("/submit")
def submit_fix(code: str = Form(...), puzzle_id: str = Form(...)):
    puzzle_file = os.path.join(PUZZLE_DIR, f"{puzzle_id}.json")
    if not os.path.exists(puzzle_file):
        return JSONResponse({"correct": False, "error": "Puzzle not found"}, status_code=404)

    with open(puzzle_file) as f:
        puzzle = json.load(f)

    user_code_lines = code.strip().count("\n") + 1  # number of lines in user's code

    # Save user code + tests temporarily
    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as tmp:
        tmp.write(code + "\n\n" + "\n".join(puzzle["tests"]))
        tmp_path = tmp.name

    try:
        subprocess.run(
            ["python", tmp_path],
            check=True,
            timeout=2,
            capture_output=True,
            text=True
        )
        result_data = {"correct": True, "explanation": puzzle["explanation"]}

    except subprocess.CalledProcessError as e:
        full_output = (e.stdout or "") + "\n" + (e.stderr or "")

        # Find the line number inside user code only
        line_hint = None
        for line in full_output.splitlines():
            if "File" in line and ", line " in line:
                try:
                    error_line = int(line.split(", line ")[1].split(",")[0])
                    if error_line <= user_code_lines:
                        line_hint = error_line
                        break
                except ValueError:
                    pass

        # Determine partial vs error
        status = "partial" if "AssertionError" in full_output or "wrong output" in full_output.lower() else "error"
        error_summary = full_output.splitlines()[-1] if full_output else "Error occurred"
        result_data = {
            "correct": False,
            "status": status,
            "line_hint": line_hint,
            "fix_line": puzzle.get("fix_line"),
            "error": f"❌ Hint: {error_summary}",
        }

    except subprocess.TimeoutExpired:
        result_data = {"correct": False, "error": "❌ Execution timed out. Try a simpler fix."}
    finally:
        os.remove(tmp_path)

    return JSONResponse(result_data)


@app.get("/puzzle/date/{date_str}")
def get_puzzle_by_date(date_str: str):
    """Return the puzzle for a specific date (YYYY-MM-DD). Only allow today or past."""
    try:
        dt = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return JSONResponse({"error": "Invalid date format"}, status_code=400)

    today = datetime.date.today()
    if dt > today:
        return JSONResponse({"error": "You cannot access future puzzles"}, status_code=403)

    puzzles = sorted(f for f in os.listdir(PUZZLE_DIR) if f.endswith(".json"))
    day_index = dt.toordinal() % len(puzzles)
    path = os.path.join(PUZZLE_DIR, puzzles[day_index])

    with open(path) as f:
        puzzle = json.load(f)

    return {
        "id": puzzle["id"],
        "title": puzzle["title"],
        "description": puzzle["description"],
        "snippet": puzzle["snippet"],
        "difficulty": puzzle.get("difficulty", "Unknown")
    }
