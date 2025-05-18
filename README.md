# Custom Tools

## Description
This project contains a collection of tools and scripts designed to assist with different tasks.

### Scripts
#### `create_english_files.py`
A Python script that generates:

- a crossword puzzle text file
- a multiple choice question set
- an Anki-compatible CSV file

### `create_english_files.sh`
A shell script that wraps the `create_english_files.py` Python script.


## Scripts
### English tools
I've created a collection of scripts that can help you with English learning.
`create_english_file.py` is a script that can be used to create English files for crossword, choices and anki.
`create_english_file.sh` is a shell script that can be used to create English files for crossword, choices and anki.

## Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   ```
2. Navigate to the project directory:
   ```bash
   cd tool
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
### English tools
To make the tool accessible from anywhere, create an alias:
```bash
alias english-tools="$(pwd)/create_english_files.sh
```
To get help, run: `english-tools -h`

## License
This project is licensed under the MIT License.
