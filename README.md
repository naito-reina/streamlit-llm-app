# AIチャットボット

FlaskとOpenAI APIを使用したシンプルなAIチャットボットアプリケーションです。

## セットアップ

1. 必要なパッケージをインストール:
```bash
pip install -r requirements.txt
```

2. OpenAI APIキーを設定:
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
python app.py
```

4. ブラウザで `http://localhost:5000` にアクセス

## 使い方

1. ブラウザでアプリを開く
2. テキストボックスにメッセージを入力
3. 「送信」ボタンをクリックするか、Enterキーを押す
4. AIからの返信が表示されます

## 注意事項

- OpenAI APIキーが必要です。https://platform.openai.com/ で取得できます。
- APIの使用には料金がかかる場合があります。

