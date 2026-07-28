---
name: GitHub_Actions_CI
description: Teaches the Swarm how to generate robust GitHub Actions workflows for continuous integration.
---

When the user asks to "Configure CI/CD" or "Setup GitHub Actions", the Deployment Agent MUST create the following physical file path: `.github/workflows/ci.yml`.

The `content` of the file MUST match this robust boilerplate:

```yaml
name: yAI Continuous Integration
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
      - name: Install Dependencies
        run: npm ci
      - name: Run Linter
        run: npm run lint
      - name: Run Tests
        run: npm test
```
