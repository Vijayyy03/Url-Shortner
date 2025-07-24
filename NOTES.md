# NOTES.md

## AI Tool Usage
- **Tool Used:** ChatGPT (OpenAI)
- **Usage:**
  - Guidance on project structure and step-by-step implementation
  - Code generation for Flask endpoints, utility functions, and in-memory storage
  - Writing and organizing test cases
  - Troubleshooting and environment setup
  - Explanations and user guidance

## Implementation Notes
- All assignment requirements were followed strictly (no web UI, no external DB, etc.).
- The project is organized into `app/` (code) and `tests/` (tests).
- In-memory storage is used for URL mappings, click counts, and timestamps.
- Thread safety is ensured with a lock.
- At least 5 tests cover all core functionality and error cases.
- All tests pass as of submission.

## Additional Notes
- If running tests on Windows, set the environment variable before running pytest:
  ```
  $env:PYTHONPATH="."
  pytest
  ```
- The API can be tested using curl, Postman, or any HTTP client.
- No significant code was rejected; all AI-generated code was reviewed and accepted as appropriate for the assignment. 