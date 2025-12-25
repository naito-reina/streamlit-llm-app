# GitHubプッシュが反映されない場合のトラブルシューティング

## 確認手順

以下のコマンドを順番に実行して、問題を特定してください。

### 1. Gitの状態を確認

```bash
git status
```

**確認ポイント:**
- コミットされていない変更がないか
- 現在のブランチ名

### 2. リモートリポジトリの設定を確認

```bash
git remote -v
```

**確認ポイント:**
- `origin`が正しいGitHubリポジトリのURLを指しているか
- URLが `https://github.com/naito-reina/streamlit-llm-app.git` になっているか

### 3. ブランチを確認

```bash
git branch -a
```

**確認ポイント:**
- 現在のブランチ名（`main`または`master`）
- リモートブランチの状態

### 4. コミット履歴を確認

```bash
git log --oneline -5
```

**確認ポイント:**
- 最新のコミットが存在するか
- コミットメッセージが正しいか

### 5. リモートとの差分を確認

```bash
git log origin/main..HEAD
```

**確認ポイント:**
- ローカルにリモートにないコミットがあるか

## よくある問題と解決方法

### 問題1: コミットされていない変更がある

**症状:**
```
Changes not staged for commit:
  modified:   app.py
```

**解決方法:**
```bash
git add .
git commit -m "Update files"
git push origin main
```

### 問題2: 別のブランチにプッシュしている

**症状:**
- GitHub上で別のブランチを見ている
- `main`ブランチに変更が反映されていない

**解決方法:**
```bash
# 現在のブランチを確認
git branch

# mainブランチに切り替え
git checkout main

# 変更をコミット・プッシュ
git add .
git commit -m "Update files"
git push origin main
```

### 問題3: リモートの変更を取得していない

**症状:**
```
! [rejected]        main -> main (fetch first)
```

**解決方法:**
```bash
git pull origin main
git push origin main
```

### 問題4: リモートリポジトリのURLが間違っている

**症状:**
- `git remote -v`で表示されるURLが間違っている

**解決方法:**
```bash
# リモートURLを削除
git remote remove origin

# 正しいURLを追加
git remote add origin https://github.com/naito-reina/streamlit-llm-app.git

# 再度プッシュ
git push -u origin main
```

### 問題5: ブラウザのキャッシュ

**症状:**
- プッシュは成功しているが、GitHub上で古い内容が表示される

**解決方法:**
- ブラウザのハードリフレッシュ（Ctrl + F5 または Ctrl + Shift + R）
- GitHubのページをリロード
- 別のブラウザで確認

## 完全なプッシュ手順（再確認）

```bash
# 1. 現在の状態を確認
git status

# 2. 変更をステージング
git add .

# 3. コミット
git commit -m "Update: 変更内容の説明"

# 4. リモートの変更を取得（必要に応じて）
git pull origin main

# 5. プッシュ
git push origin main
```

## 確認方法

プッシュ後、以下で確認してください：

1. **GitHubのWebサイトで確認**
   - https://github.com/naito-reina/streamlit-llm-app にアクセス
   - ファイルの更新日時を確認
   - 最新のコミット履歴を確認

2. **コマンドで確認**
   ```bash
   git log origin/main --oneline -5
   ```

3. **ブラウザのキャッシュをクリア**
   - Ctrl + F5 でハードリフレッシュ


