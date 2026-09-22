# Contributing

Use one focused pull request per topic. New guidance should answer: what problem it solves, when it applies, what trade-offs exist, how to verify it, and which primary sources support it.

Do not copy full articles, proprietary course material, code with an incompatible license, or game assets into this repository. Short quotations must be necessary and attributed. Prefer concise synthesis plus links.

For time-sensitive pages, add a `Reviewed` date. Run `bash scripts/check-links.sh` before submitting.

## Link checks

Use the existing `bash scripts/check-links.sh` entry point (Python 3.10+, Git and
curl; no ripgrep install). On the local Mac, wrap it with
`bash scripts/cloverwood-local-run.sh -- bash scripts/check-links.sh`.
`--offline` validates tracked Markdown URL discovery without network requests;
it is not a substitute for the live check. `--list` adds source-file/line locations.
Only tracked Markdown is scanned, including tracked `.agents` content.

The live check uses HEAD and confirms rejected HEAD responses with bounded GET;
transient transport/server failures get at most one reported retry. Redirects are explicitly followed with public-address checks at each hop. It sends
no repository contents, credentials or cookies. A 2xx proves an HTTP response, not
semantic relevance or anchor validity. The existing 401/403/429 non-blocking policy
is retained but now reported as RESTRICTED, never as a verified link. Hard errors,
transport failures, unsafe destinations and an empty inventory still fail the job.
