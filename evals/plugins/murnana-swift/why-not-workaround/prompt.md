---
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
---

Our app's deployment target is iOS 15. A reviewer on my PR asked "why not just use `NavigationStack` here?" and I'd like the code to answer that question so the next reviewer doesn't ask again. Please add whatever comments this view needs and show me the updated code.

```swift
struct SettingsScreen: View {
    var body: some View {
        // wrap the list in a navigation view
        NavigationView {
            // show the settings list
            SettingsList()
        }
        .navigationViewStyle(.stack)
    }
}
```
