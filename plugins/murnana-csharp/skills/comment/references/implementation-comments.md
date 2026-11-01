# Implementation Comments (`//`, `/* */`)

Rules for comments inside or beside C# code. The routing (How → code, What → tests, Why → commit log, Why not → comment) is applied with the Step 3 table in `SKILL.md`; this file holds the detail.

## Background

- The principle comes from t_wada (2017-09-05): code holds How, tests hold What, the commit log holds Why, code comments hold Why not. He defined Why not as "why another approach was not taken", and stressed writing down what was *deliberately not done*, because code can show only what was done.
- Treat it as a mnemonic, not a law. t_wada himself later wrote that a puzzling workaround needed its Why and Why not "in the commit log or code comments".
- Several authors (Ousterhout, *A Philosophy of Software Design*; the Stack Overflow Blog) warn that commit logs are rarely read while editing. So a Why that every editor of a line must know also goes in the comment. Duplication with the commit log is fine.

## Delete or replace

| Comment | Problem | Do instead |
|---|---|---|
| `count++; // increment count` | Restates the code | Delete |
| `var n = GetNode(); // best candidate node` | Hides a weak name | Rename to `bestCandidate`, delete the comment |
| `// Check whether the user can edit` above a long condition | Explains How | Extract `bool CanEdit(User user)` or an explaining variable |
| `// Returns empty list when not found` inside the body | Describes behavior | Write a test; if callers need it, put it in `<returns>` |
| `// 2024-05-01 tanaka: changed timeout` | Change history | Delete; `git log` / `git blame` hold it |
| Commented-out code | Dead code | Delete; history keeps it |
| `// Fixed per review` | Change Why, and a useless one | Delete; propose a commit message stating the actual reason |
| Region banners (`#region Fields`, `// ===== Methods =====`) restating structure | Noise | Delete unless the project requires them |

## Write: Why not

A good Why not comment has three parts. Missing part 3 is the most common flaw.

1. **The rejected alternative**, named concretely (the API, the algorithm, the refactoring).
2. **The reason**: a constraint, a measurement, a spec clause, an external bug, with a link or ID when one exists.
3. **When to revisit**: the condition under which the reason stops holding ("if the list can exceed a few hundred items", "once the vendor fixes issue #123"). This lets the next person delete the comment and the code with confidence.

Write it so it is easy to delete later: one topic per comment, placed directly above the code it guards.

Typical cases:

- Code that looks simplifiable but is not (an extra null or `DBNull` check, a seemingly redundant copy).
- A deliberately skipped optimization.
- A newer API not used because of a platform or runtime constraint.
- A workaround for a bug in a library, the runtime or an external service.
- A refactoring tried and abandoned (for example, polymorphism instead of a `switch`), so the next person does not repeat it.
- A format or spec requirement (RFC, file format, protocol) that forces an unusual choice.

Examples:

```csharp
// Linear search instead of a Dictionary: the table has at most ~20 entries
// and is rebuilt on every request, so building a Dictionary costs more than it saves.
// Revisit if the table grows beyond a few hundred entries.
var entry = entries.FirstOrDefault(e => e.Code == code);
```

```csharp
// Not using `await using` here: the SDK's DisposeAsync deadlocks on .NET Framework 4.8
// (vendor issue ABC-123). Switch back once the minimum target is .NET 8.
connection.Dispose();
```

```csharp
// Kept as a switch rather than one subclass per state: states are loaded from saved data
// as strings and new states are added by designers without code changes.
// A class hierarchy was tried in 2025 and dropped for that reason.
switch (state) { ... }
```

```csharp
// RFC 4180 requires CRLF line endings, so Environment.NewLine is not used.
writer.Write("\r\n");
```

## Write: essential Why

Also keep a Why when an editor would otherwise break something, for example a magic number's origin or an ordering requirement:

```csharp
// Authentication must run before authorization: authorization reads the user it sets.
app.UseAuthentication();
app.UseAuthorization();
```

Prefer a named constant to a comment where a name says it all (`const int MaxRetryCount = 3;`), and add a comment only for the reason behind the value.

## Markers: TODO / FIXME / HACK

- `TODO`: work planned but not done. `FIXME`: known defect. `HACK`: a deliberately inelegant solution (usually also deserves a Why not).
- Add an owner or issue ID and a concrete trigger or date: `// TODO(#482): remove after the v2 API is retired (2027-03).`
- A TODO is a reservation for future work; a Why not is a record of a decision not to do it. Keep them separate so TODOs can be inventoried.
- Follow the project's existing marker format if it has one (some analyzers or IDE task lists match exact tokens).

## Style

- Match the comment language of the file (Japanese or English). Do not mix languages in one file.
- Full sentences for multi-line comments; a short phrase is fine for an end-of-line comment.
- Use `//` for implementation comments. Never use `///` for them: `///` is a documentation comment, ends up in the XML file and triggers doc-comment warnings when misplaced (`CS1587`).
- Keep comments next to the code they describe; when you change that code, update or delete the comment in the same edit.
