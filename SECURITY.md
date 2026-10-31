# Security boundaries

This is a local independent portfolio prototype, not a production security claim.

- No employer data, credentials or patient information is included.
- No arbitrary SQL, tool execution, pricing approval or write-back path exists.
- SQL report names are allowlisted; the data connection is query-only after load.
- Retrieved text is untrusted evidence, never a source of system instructions.
- The optional model has no tools and can only be contacted at a loopback origin.
- Generated output is bounded and must cite known retrieved IDs or abstain.
- HTML output escapes evidence, questions and model text before rendering.
- Raw questions and evidence are not intentionally logged by application code.

Pattern-based scope/injection checks are illustrative and incomplete. Valid source
IDs can accompany an unsupported generated claim. They do not establish entailment,
guard against all prompt injection, or enforce access controls over a larger corpus.
Do not connect this prototype to internal systems or publish it openly without
authentication, authorization, rate limits, transport review and additional testing.
