---
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
---

このファイルの名前の付け方をレビューしてください。このプロジェクトには命名規則のルールがありません。

```typescript
export interface IUserRepository {
  Find_User(UserId: string): Promise<user_record | undefined>;
}

export type user_record = {
  DisplayName: string;
};

export enum connectionState {
  idle,
  CONNECTED,
}

export class userService {
  private _repository: IUserRepository;

  constructor(Repository: IUserRepository) {
    this._repository = Repository;
  }
}
```
