---
name: Vercel_Deployment
description: Teaches the Swarm how to deploy a Next.js or React application to Vercel via CLI.
---

To deploy this application to Vercel, the Deployment Agent MUST execute the following exact `setup_commands` in the JSON array:

1. Install the Vercel CLI globally (if not already installed).
2. Run the `vercel build` command.
3. Run the `vercel deploy --prod --yes` command.

Example `setup_commands` output:
```json
[
  "npm install -g vercel@latest",
  "vercel link --yes",
  "vercel deploy --prod --yes"
]
```
