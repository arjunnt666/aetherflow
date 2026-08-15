# Recovery

agent runs die. plan for it.

recommended pattern in this codebase shape:
- checkpoint after each successful tool call
- store run id + step index in durable storage
- on restart, skip completed steps and resume from the next pending node

the public tree sketches the hooks. wire a real store before trusting production traffic.
