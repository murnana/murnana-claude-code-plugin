---
max_turns: 8
allowed_tools: [Read, Glob, Grep, Skill]
---

このコードの公開している部分に、使う人向けの説明（TSDoc comments）を書いてください。コードそのものは変えないでください。

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
