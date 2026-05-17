---
name: ue5-docs
description: Search Unreal Engine 5 official documentation to answer questions.
when_to_use: >
  Use this skill whenever the user asks about UE5 features, concepts, C++ APIs,
  Blueprint usage, error causes, or configuration. Trigger on keywords like
  "UE5", "Unreal Engine", "Blueprint", "GameplayAbility", "UObject", "AActor",
  "UActorComponent", etc. Always check the docs before answering UE5 code questions.
  Note: dev.epicgames.com is a JavaScript SPA — only WebSearch works, not WebFetch.
allowed-tools: Read Grep WebSearch
---

# Unreal Engine 5 Docs Skill

Search Epic Games' official documentation via WebSearch and answer in Japanese.

> **Note:** `dev.epicgames.com` is a JavaScript-rendered SPA. WebFetch returns empty content for all pages on this site. Use WebSearch exclusively.

## Version Awareness

**Before searching or answering, you must identify the exact UE version (e.g., 5.3, 5.4, 5.5).**

- If the version is stated in the question, use it directly.
- If the version is unclear, **stop and ask the user** before doing anything else:
  > 「使用しているUnreal Engineのバージョン（例: 5.4, 5.5）を教えてください。」
- Do not assume a version or proceed with a generic answer when the version is unknown.

## Documentation URLs

Base URL pattern for version `5.X`:

| Content | URL pattern |
|---|---|
| Main docs | `https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-engine-5-{minor}-documentation` |
| C++ API reference | `https://dev.epicgames.com/documentation/en-us/unreal-engine/API` |

**Examples:**
- UE 5.4 → `https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-engine-5-4-documentation`
- UE 5.5 → `https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-engine-5-5-documentation`
- UE 5.7 → `https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-engine-5-7-documentation`

## Workflow

### Step 1: Search with WebSearch

Use this query, substituting the confirmed version:
```
<keywords> Unreal Engine 5.{minor} documentation dev.epicgames.com
```

For C++ API lookups:
```
<class or function name> Unreal Engine API dev.epicgames.com
```

Run multiple searches if needed to gather enough information.

### Step 2: Answer in Japanese

Summarize the search results and answer clearly in Japanese. Code samples may remain in English. Always include the source URLs at the end.

## Response Format

```
## [Topic]

[Explanation]

### Code Example (if applicable)
\`\`\`cpp
// sample
\`\`\`

### References
- [Doc title](URL)
```

## Notes

- Prefer version-specific pages over generic ones
- Note when a feature was added, changed, or deprecated in a particular version
- If information is not found, say so and suggest alternative resources (e.g., Epic Developer Community forums)
