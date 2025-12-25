# OpenAI APIキー設定ガイド

当課題でLLMアプリを開発するにあたり、OpenAI APIキーを設定する必要があります。

Google Colaboratoryではシークレット機能を活用して設定を行っていましたが、自分のPC上でOpenAI APIキーを設定するためには「.env」という名前のファイルにAPIキーを記載し、LLMとのやり取りを記述するファイルから読み込まなくてはいけません。

「.env」は、環境変数を記述するためのファイルです。環境変数とはシステム・アプリの設定用の変数であり、これを「.env」に記述して専用のコードで読み込むことにより、環境変数を設定できます。

## 手順4-1: 「.env」ファイルの作成

まずはVSCodeにセットしたフォルダ直下に「.env」という名前のファイルを作成してください。

**注意**: `.env`ファイルは`.gitignore`に含まれているため、Gitにコミットされません（安全です）。

## 手順4-2: OpenAI APIキーの記述

作成した「.env」ファイルに、以下の形式でご自身のOpenAI APIキーを記述してください。

```
OPENAI_API_KEY=ご自身のOpenAI APIキー
```

「ご自身のOpenAI APIキー」の部分を、実際のAPIキーに書き換えてください。文字列をクォーテーションで囲む必要はありません。

OpenAI APIキーを設定するためには、環境変数名を「OPENAI_API_KEY」とする必要があります。

## 手順4-3: 環境変数を読み込むためのパッケージをインストール

次の手順で、「.env」ファイルに記述した環境変数をメインファイルから読み込むコードを記述します。

その前準備として、環境変数を読み込むためのパッケージ「python-dotenv」を以下のコマンドでインストールしましょう。

```bash
pip install python-dotenv
```

または、`requirements.txt`からすべてのパッケージをインストールする場合：

```bash
pip install -r requirements.txt
```

（`requirements.txt`には既に`python-dotenv`が含まれています）

## 手順4-4: メインファイルから環境変数の読み込み

メインファイル「app.py」には既に以下のコードが記述されており、「.env」ファイルに記述した環境変数（今回の場合は「OPENAI_API_KEY」）が自動的に読み込まれます。

```python
from dotenv import load_dotenv
from pathlib import Path

# .envファイルから環境変数を読み込む
env_path = Path(__file__).parent / '.env'
if env_path.exists():
    load_dotenv(dotenv_path=env_path)
else:
    load_dotenv()
```

これにより、「app.py」にLLMとやり取りするコード（OpenAI APIを呼び出すコード）を記述して実行すると、Google ColaboratoryにおいてOpenAI APIキーが自動で参照されていたのと同じように、「.env」ファイルに記述したOpenAI APIキーが自動で参照されるようになります。

## OpenAI APIキーの取得方法

まだAPIキーを取得していない場合は、以下の手順で取得してください：

1. https://platform.openai.com/ にアクセス
2. アカウントにログイン（または新規登録）
3. 「API keys」セクションに移動
4. 「Create new secret key」をクリック
5. キー名を入力して作成
6. **重要**: 表示されたAPIキーをコピー（一度しか表示されません）

## 確認方法

アプリを起動して、エラーメッセージが表示されなければ設定成功です。

```bash
streamlit run app.py
```

## Streamlit Cloudでデプロイする場合

Streamlit Cloudにデプロイする場合は、`.env`ファイルを直接使用することはできません（セキュリティ上の理由でGitにコミットできないため）。代わりに、Streamlit CloudのSecrets機能を使用してください。

詳細な手順は [`DEPLOY.md`](DEPLOY.md) を参照してください。


