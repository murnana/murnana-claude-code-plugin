---
name: ue5-docs
description: Answer Unreal Engine 5 questions (features, C++ API, Blueprint, errors, settings) from Epic's official documentation via web search. Use before answering any UE5 question, even if the user doesn't ask for docs.
allowed-tools: Read Glob WebSearch AskUserQuestion
---

# Unreal Engine 5 Docs

Answer an Unreal Engine 5 question from Epic's official documentation (`dev.epicgames.com`), in Japanese, with source URLs.

## Rules

1. **Use WebSearch only.** `dev.epicgames.com` is rendered by JavaScript, so WebFetch returns an empty page for every URL on it. Don't try WebFetch, not even once.
2. **Know the engine version before searching.** APIs and settings differ between 5.x releases, so an answer for the wrong version can be wrong.
3. **Answer from the search results.** Don't fill gaps from memory. If the results don't cover something, say that it was not found.

## Step 1: Fix the version

Stop at the first source that gives a version such as `5.4`:

1. The user's message or earlier conversation.
2. A `*.uproject` file in the working directory (Glob `**/*.uproject`, then Read it): the `EngineAssociation` value, when it looks like `5.4`. A GUID there means a source build; it gives no version.
3. Ask with the `AskUserQuestion` tool, never as plain reply text, and wait for the answer before searching. Question: 「使用している Unreal Engine のバージョンを教えてください。」 Options: the three newest 5.x releases you know of; the user can type another via "Other". Without the tool, ask in the reply.

Ask at most once per conversation: reuse the version for every later UE5 question unless the user names another.

## Step 2: Search

Run WebSearch with the version in the query:

| Question type | Query |
|---|---|
| Feature, concept, setting, error | `<keywords> Unreal Engine 5.<minor> documentation dev.epicgames.com` |
| C++ class or function | `<class or function name> Unreal Engine API dev.epicgames.com` |

- Search in English, even when the question is in Japanese: the documentation is indexed in English.
- If the first results are thin, search again with other keywords (the class name, the editor menu name, the error text). Two or three searches are normal.
- Prefer results under these paths. Other sites (forums, blogs) only support what the documentation says, and are labeled as such in the answer:
  - Main documentation for 5.X: `https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-engine-5-<minor>-documentation`
  - C++ API reference: `https://dev.epicgames.com/documentation/en-us/unreal-engine/API`

## Step 3: Answer in Japanese

Use this shape. Leave out the code section when there is no code.

````markdown
## <トピック>

<説明。対象バージョンを最初に書く>

### コード例

```cpp
// sample
```

### 参考

- [<ページタイトル>](<URL>)
````

- Code and identifiers stay in English.
- List every URL the answer relies on under 参考.
- When a result is for another 5.x version than the user's, say which version it is for.
- When a feature was added, changed or deprecated in a specific version, say so.
- When nothing relevant is found, say so and point to the Epic Developer Community forums (`https://forums.unrealengine.com/`) instead of guessing.
