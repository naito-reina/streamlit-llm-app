# APIキー設定ガイド

## OpenAI APIキーの取得方法

1. https://platform.openai.com/ にアクセス
2. アカウントにログイン（または新規登録）
3. 「API keys」セクションに移動
4. 「Create new secret key」をクリック
5. キー名を入力して作成
6. **重要**: 表示されたAPIキーをコピー（一度しか表示されません）

## 設定方法

### Streamlit Cloudで設定する場合

1. Streamlit Cloudのアプリページで「Manage app」をクリック
2. 「Secrets」タブを開く
3. 以下の形式で追加：
   ```
   OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```
   （`sk-`で始まる実際のAPIキーに置き換えてください）
4. 「Save」をクリック
5. アプリが自動的に再デプロイされます

### ローカル環境で設定する場合

1. `.streamlit/secrets.toml`ファイルを作成
2. 以下の内容を記述：
   ```toml
   OPENAI_API_KEY = "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
   ```
   （`sk-`で始まる実際のAPIキーに置き換えてください）
3. ファイルを保存
4. アプリを再起動

**注意**: `.streamlit/secrets.toml`ファイルは`.gitignore`に含まれているため、Gitにコミットされません（安全です）。

## 確認方法

アプリを起動して、エラーメッセージが表示されなければ設定成功です。


