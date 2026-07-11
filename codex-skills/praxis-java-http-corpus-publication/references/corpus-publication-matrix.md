# Corpus Publication Matrix

| Example state | Use | Required evidence |
| --- | --- | --- |
| `llmOperational` | Safe confirmed read/discovery path | Published proof and narrow smoke |
| `protectedContract` | Header/auth/write contract reading | Source of truth and protection metadata |
| `referenceOnly` | Legacy, caveat, or illustrative evidence | Explicit limitation and no default lane |

Every request and payload is manifest-tracked. Generated LLM files derive from
the manifest. A corpus failure is classified against the canonical owner before
any flag or example is changed.
