# Streamlit Cloud デプロイガイド

このガイドでは、GitHubにコードをプッシュしてStreamlit Cloudでアプリを公開する手順を説明します。

## 前提条件

- GitHubアカウントを持っていること
- Streamlit Cloudアカウントを持っていること（https://share.streamlit.io/ で無料登録可能）
- OpenAI APIキーを取得済みであること

## デプロイ手順

### 1. GitHubリポジトリの準備

#### 1-1. リポジトリの作成（まだ作成していない場合）

1. GitHubにログイン
2. 右上の「+」→「New repository」をクリック
3. リポジトリ名を入力（例: `streamlit-llm-app`）
4. 「Public」または「Private」を選択
5. 「Create repository」をクリック

#### 1-2. ローカルリポジトリの初期化とコミット

プロジェクトディレクトリで以下のコマンドを実行：

```bash
# Gitリポジトリの初期化（まだの場合）
git init

# すべてのファイルをステージング
git add .

# コミット
git commit -m "Initial commit: Streamlit LLM app"

# GitHubリポジトリをリモートとして追加（YOUR_USERNAMEとYOUR_REPO_NAMEを置き換え）
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

# メインブランチを設定
git branch -M main

# GitHubにプッシュ
git push -u origin main
```

**重要**: `.env`ファイルは`.gitignore`に含まれているため、Gitにコミットされません。これは正しい動作です。

### 2. Streamlit Cloudでのデプロイ

#### 2-1. Streamlit Cloudにログイン

1. https://share.streamlit.io/ にアクセス
2. 「Sign in」をクリック
3. GitHubアカウントでログイン

#### 2-2. 新しいアプリを作成

1. ダッシュボードで「New app」をクリック
2. 以下の情報を入力：
   - **Repository**: 先ほどプッシュしたGitHubリポジトリを選択
   - **Branch**: `main`（または使用しているブランチ名）
   - **Main file path**: `app.py`
3. 「Advanced settings」をクリック

#### 2-3. APIキーをSecretsに設定

**重要**: この手順は必須です。Secretsを設定しないと、アプリでAPIキーエラーが表示されます。

1. 「Advanced settings」を開いた状態で、「Secrets」セクション（またはタブ）を確認
2. テキストエリアに以下を**正確に**入力：

**方法1（推奨）: TOML形式**
```toml
OPENAI_API_KEY = "sk-あなたの実際のAPIキー"
```

**方法2: シンプル形式**
```
OPENAI_API_KEY=sk-あなたの実際のAPIキー
```

**入力時の注意点**: 
- `sk-`で始まる実際のOpenAI APIキーに置き換えてください
- TOML形式を使用する場合、**ダブルクォート（`"`）**で囲んでください（シングルクォート`'`は使用しない）
- 等号（`=`）の前後にスペースを入れないでください（方法2の場合）
- 余分なスペースや改行がないか確認してください
- コピー&ペーストする際に、見えない文字が入らないように注意してください

3. **必ず「Save」ボタンをクリック**して保存してください
4. 保存後、アプリが自動的に再デプロイされます（通常10-30秒）
5. 再デプロイが完了するまで待ってから、アプリをリロードして確認してください

**確認方法**: 
- アプリをリロードして、エラーメッセージが表示されなくなれば成功です
- まだエラーが表示される場合は、Secretsの内容を再度確認してください

#### 2-4. デプロイ

1. 「Deploy」をクリック
2. デプロイが完了するまで待ちます（通常1-2分）
3. デプロイが完了すると、アプリのURLが表示されます

### 3. デプロイ後の確認

1. アプリのURLにアクセス
2. エラーメッセージが表示されないことを確認
3. チャットボックスにメッセージを入力して、AIからの応答が返ってくることを確認

## トラブルシューティング

### APIキーエラーが表示される場合

**ステップ1: Secretsの設定を確認**

1. Streamlit Cloudのダッシュボード（https://share.streamlit.io/）にアクセス
2. アプリを選択して、「Manage app」をクリック
3. 「Secrets」タブ（またはセクション）をクリック
4. 以下の点を確認：
   - `OPENAI_API_KEY`が存在するか
   - 値が正しく設定されているか（`sk-`で始まる完全なAPIキーか）
   - 余分なスペースや改行がないか
   - 引用符の種類が正しいか（ダブルクォート`"`を使用）

**ステップ2: Secretsを再設定**

もし設定が間違っている、または存在しない場合：

1. Secretsのテキストエリアに以下を入力：
   ```toml
   OPENAI_API_KEY = "sk-あなたの実際のAPIキー"
   ```
   （実際のAPIキーに置き換えてください）

2. **必ず「Save」ボタンをクリック**して保存

3. 保存後、アプリが自動的に再デプロイされます（通常10-30秒）

4. 再デプロイが完了するまで待ってから、アプリをリロード

**ステップ3: それでも解決しない場合**

- ブラウザのキャッシュをクリアして、アプリを再度開く
- Streamlit Cloudの「Logs」を確認して、エラーメッセージがないか確認
- APIキーが有効かどうか確認（https://platform.openai.com/ で確認）
- アプリを一度削除して、再度デプロイしてみる

### デプロイが失敗する場合

1. Streamlit Cloudのダッシュボードでアプリを選択
2. 「Manage app」→「Logs」をクリック
3. エラーメッセージを確認
4. よくある原因：
   - `requirements.txt`に必要なパッケージが含まれていない
   - `app.py`に構文エラーがある
   - ファイルパスが正しくない

### コードを更新した場合

1. 変更をコミット・プッシュ：
   ```bash
   git add .
   git commit -m "Update: 変更内容の説明"
   git push
   ```
2. Streamlit Cloudが自動的に変更を検知して再デプロイします
3. 数分待ってからアプリを確認してください

## 注意事項

- **ローカル環境**: `.env`ファイルを使用してAPIキーを設定します（詳細は [`SETUP.md`](SETUP.md) を参照）
- **Streamlit Cloud**: `.env`ファイルはGitにコミットされないため、Streamlit Cloudでは使用できません。代わりに、Secrets機能を使用してAPIキーを安全に管理します
- APIキーは機密情報です。GitHubにコミットしないでください（`.gitignore`に`.env`が含まれているため、自動的に除外されます）
- Streamlit Cloudの無料プランには制限があります（詳細は公式サイトを確認）

## 参考リンク

- Streamlit Cloud: https://share.streamlit.io/
- Streamlit Cloud ドキュメント: https://docs.streamlit.io/streamlit-community-cloud
- OpenAI API: https://platform.openai.com/

