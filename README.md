```bash
# After cloning
cd bugdle/
python -m venv .venv      # creates virtual environment in .venv folder
```

### Windows
```bash
.venv\Scripts\activate
```
### macOS/Linux
```bash
source .venv/bin/activate
```

### Then
```bash
pip install -r requirements.txt

# This will create a new server at 127.0.0.1:8000
uvicorn app:app --reload
```
