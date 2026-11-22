---
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
---

マージする前に、このコードをレビューしてください。プロジェクトに決まったルールはありません。

```rust
use std::cell::RefCell;
use std::ffi::CString;
use std::os::raw::c_char;
use std::rc::Rc;

pub struct Node {
    pub name: String,
    pub parent: RefCell<Option<Rc<Node>>>,
    pub children: RefCell<Vec<Rc<Node>>>,
}

pub fn attach(parent: &Rc<Node>, child: &Rc<Node>) {
    *child.parent.borrow_mut() = Some(Rc::clone(parent));
    parent.children.borrow_mut().push(Rc::clone(child));
}

extern "C" {
    fn native_log(message: *const c_char) -> i32;
}

pub fn log(message: &str) -> Result<(), String> {
    let raw = CString::new(message).map_err(|e| e.to_string())?.into_raw();
    let status = unsafe { native_log(raw) };
    if status != 0 {
        return Err(format!("native_log failed: {status}"));
    }
    unsafe { drop(CString::from_raw(raw)) };
    Ok(())
}
```
