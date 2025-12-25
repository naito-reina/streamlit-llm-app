# AIチャットボット（Streamlit版）

StreamlitとOpenAI APIを使用したシンプルなAIチャットボットアプリケーションです。

## セットアップ

### ローカル環境での実行

1. 必要なパッケージをインストール:
```bash
pip install -r requirements.txt
```

2. OpenAI APIキーを設定:

**方法1: Streamlitのシークレットファイルを使用（推奨）**
- `.streamlit/secrets.toml`ファイルを作成:
```toml
OPENAI_API_KEY = "your_api_key_here"
```

**方法2: 環境変数を使用**
```bash
# Windows (コマンドプロンプト)
set OPENAI_API_KEY=your_api_key_here

# Windows (PowerShell)
$env:OPENAI_API_KEY="your_api_key_here"

# Linux/Mac
export OPENAI_API_KEY=your_api_key_here
```

3. アプリケーションを起動:
```bash
streamlit run app.py
```

4. ブラウザで自動的に開きます（通常は `http://localhost:8501`）

### Streamlit Cloudでのデプロイ

1. GitHubリポジトリにコードをプッシュ
2. Streamlit Cloud（https://streamlit.io/cloud）にログイン
3. 「New app」をクリック
4. リポジトリとブランチを選択
5. 「Advanced settings」を開き、「Secrets」に以下を追加:
```
OPENAI_API_KEY=your_api_key_here
```
6. 「Deploy」をクリック

## 使い方

1. ブラウザでアプリを開く
2. 下部のテキストボックスにメッセージを入力
3. Enterキーを押すか送信ボタンをクリック
4. AIからの返信が表示されます
5. サイドバーの「チャット履歴をクリア」ボタンで会話をリセットできます

## 機能

- 🤖 OpenAI GPT-3.5-turboを使用したチャットボット
- 💬 会話履歴の保持（最新10件）
- 🗑️ チャット履歴のクリア機能
- 📱 レスポンシブデザイン

## 注意事項

- OpenAI APIキーが必要です。https://platform.openai.com/ で取得できます。
- APIの使用には料金がかかる場合があります。
- チャット履歴は最新10件まで保持されます（メモリ効率のため）。

## トラブルシューティング

### APIキーエラーが表示される場合

- Streamlit Cloud: 「Manage app」→「Secrets」でAPIキーが正しく設定されているか確認
- ローカル環境: `.streamlit/secrets.toml`または環境変数が正しく設定されているか確認
