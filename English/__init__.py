"""
The English package provides tools to manage and transform vocabulary data
for language learning applications.

Modules:
- vocabulary: Defines the Vocabulary data model and import/export utilities.
- choice_generator: Generates randomized multiple choice data for revision exercises.
- crossword_export: Prepares vocabulary data for crossword puzzle generation (e.g. via crosswordlabs.com).
"""
from pathlib import Path
DIR_BASE_SAVE = Path(__file__).parent.parent / "files" / "english"