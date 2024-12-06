autopep8 -r --in-place --aggressive --aggressive --max-line-length=79 fivc && \
autopep8 -r --in-place --aggressive --aggressive --max-line-length=79 tests && \
flake8 fivc && \
flake8 tests
