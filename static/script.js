let editor;
let currentPuzzleId = null;

// Helper function to update editor & UI
function loadPuzzleFromJSON(puzzle) {
    currentPuzzleId = puzzle.id;  // store the puzzle's id
    document.getElementById("desc").innerText = puzzle.title + " — " + puzzle.description;
    document.getElementById("difficulty").innerText = "Difficulty: " + (puzzle.difficulty || "Unknown");

    if (editor) {
        editor.setValue(puzzle.snippet);
    } else {
        editor = CodeMirror(document.getElementById("editor"), {
            value: puzzle.snippet,
            mode: "python",
            theme: "dracula",
            lineNumbers: true,
            indentUnit: 4,
            tabSize: 4,
            indentWithTabs: false,
            lineWrapping: false,
        });
    }

    document.getElementById("result").innerText = "";
}

// Load a puzzle from a URL (daily, random, or by date)
async function loadPuzzle(url = "/puzzle") {
    const res = await fetch(url);
    if (!res.ok) {
        const errData = await res.json();
        document.getElementById("desc").innerText = errData.error || "Puzzle unavailable";
        document.getElementById("difficulty").innerText = "";
        if (editor) editor.setValue("");
        document.getElementById("result").innerText = "";
        return;
    }
    const puzzle = await res.json();
    loadPuzzleFromJSON(puzzle);
}

// Submit code fix
async function submitFix() {
    const code = editor.getValue();
    const formData = new FormData();
    formData.append("code", code);
    formData.append("puzzle_id", currentPuzzleId);

    const res = await fetch("/submit", { method: "POST", body: formData });
    const data = await res.json();

    const resultDiv = document.getElementById("result");

    // Clear previous highlights
    editor.getAllMarks().forEach(mark => mark.clear());
    for (let i = 0; i < editor.lineCount(); i++) {
        editor.removeLineClass(i, "background", "highlight-line");
    }

    if (data.correct) {
        resultDiv.innerHTML = "✅ Correct!<br><br>" + data.explanation;
        resultDiv.style.color = "#3fb950";
    } else {
        // Always highlight the fix line from the puzzle JSON
        if (data.fix_line) {
            const line = data.fix_line;
            if (line >= 0 && line < editor.lineCount()) {
                editor.addLineClass(line, "background", "highlight-line");
                editor.scrollIntoView({ line, ch: 0 }, 100);
            }
        }

        // Show message
        if (data.status === "partial") {
            resultDiv.innerHTML = `🟡 Almost there! Check line ${data.fix_line || "?"}.<br><br>${data.error || ""}`;
            resultDiv.style.color = "#e3b341";
        } else {
            resultDiv.innerText = "❌ " + (data.error || "Try again!");
            resultDiv.style.color = "#f85149";
        }
    }
}

// Initialize page
document.addEventListener("DOMContentLoaded", () => {
    // Load today's puzzle
    loadPuzzle();

    // Buttons
    document.getElementById("submitBtn").addEventListener("click", submitFix);
    document.getElementById("randomBtn").addEventListener("click", () => loadPuzzle("/puzzle/random"));

    // Initialize Flatpickr calendar
    flatpickr("#calendar-container", {
        inline: true,
        defaultDate: new Date(),
        maxDate: "today", // Disable future dates
        theme: "dark",
        onChange: async function (selectedDates) {
            if (selectedDates.length === 0) return;
            const dateStr = selectedDates[0].toISOString().split("T")[0]; // "YYYY-MM-DD"
            const res = await fetch(`/puzzle/date/${dateStr}`);
            if (!res.ok) {
                const errData = await res.json();
                document.getElementById("desc").innerText = errData.error || "Puzzle unavailable";
                document.getElementById("difficulty").innerText = "";
                if (editor) editor.setValue("");
                document.getElementById("result").innerText = "";
                return;
            }
            const puzzle = await res.json();
            loadPuzzleFromJSON(puzzle);
        }
    });
});
