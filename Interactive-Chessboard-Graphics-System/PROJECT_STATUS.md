# Build and validation status

- Python source syntax compilation: passed (`py_compile`).
- Manual Computer Graphics unit tests: **7 passed** using `python -m unittest discover -s tests -v`.
- Algorithm screenshots: generated from the manual algorithms and included under `screenshots/`.
- Desktop chess UI: source is provided, but was not launched in the build runtime because `python-chess` was not installed there. Install `requirements.txt` and verify the GUI on the target Windows/VS Code machine.
- The report and presentation are initial editable drafts based on the uploaded PBL templates. Verify the Computer Graphics faculty name, course code, semester, and actual member task allocation before submission.
- The report intentionally distinguishes algorithm unit-test results from unperformed GUI end-to-end tests. Capture real chessboard screenshots after running the application.
