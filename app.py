import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv

# .envファイルから環境変数を読み込む
load_dotenv()

# ページ設定
st.set_page_config(
    page_title="AIチャットボット",
    page_icon="🤖",
    layout="wide"
)

# OpenAI APIキーの取得関数
def get_api_key():
    """Streamlit Cloudのシークレットまたは環境変数からAPIキーを取得"""
    api_key = None
    
    # Streamlit Cloudのシークレットから取得を試みる
    try:
        if hasattr(st, 'secrets') and st.secrets:
            api_key = st.secrets.get("OPENAI_API_KEY")
    except (KeyError, AttributeError, TypeError):
        pass
    
    # シークレットがない場合は環境変数から取得
    if not api_key:
        api_key = os.getenv('OPENAI_API_KEY')
    
    return api_key

# APIキーの取得
api_key = get_api_key()

# APIキーが設定されていない場合の処理
if not api_key:
    st.error("⚠️ OpenAI APIキーが設定されていません。")
    st.info("""
    **APIキーの設定方法：**
    
    1. **ローカル実行の場合（推奨）：**
       - プロジェクトルートに`.env`ファイルを作成し、以下を追加：
       ```
       OPENAI_API_KEY=your_api_key_here
       ```
    
    2. **Streamlit Cloudの場合：**
       - 「Manage app」→「Secrets」で以下を追加：
       ```
       OPENAI_API_KEY=your_api_key_here
       ```
    
    3. **その他の方法：**
       - `.streamlit/secrets.toml`ファイルを作成（または環境変数を設定）
       ```
       OPENAI_API_KEY = "your_api_key_here"
       ```
    """)
    st.stop()

# OpenAIクライアントの初期化（グローバル変数ではなく、関数内で使用）
def get_openai_client():
    """OpenAIクライアントを取得"""
    if not api_key:
        return None
    try:
        return OpenAI(api_key=api_key)
    except Exception as e:
        st.error(f"OpenAIクライアントの初期化に失敗しました: {str(e)}")
        return None

client = get_openai_client()
if client is None:
    st.stop()

# セッション状態の初期化
if "messages" not in st.session_state:
    st.session_state.messages = []

# チャット履歴の表示
chat_container = st.container()
with chat_container:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# ユーザー入力
if prompt := st.chat_input("メッセージを入力してください..."):
    # ユーザーメッセージを追加
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # AI応答を生成
    with st.chat_message("assistant"):
        with st.spinner("考え中..."):
            try:
                # 会話履歴を構築
                messages_for_api = [
                    {"role": "system", "content": "あなたは親切で役立つアシスタントです。日本語で丁寧に回答してください。"}
                ]
                # 直近の会話履歴を追加（最新10件まで）
                for msg in st.session_state.messages[-10:]:
                    messages_for_api.append({"role": msg["role"], "content": msg["content"]})
                
                # OpenAI APIを呼び出し
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=messages_for_api,
                    temperature=0.7,
                    max_tokens=500
                )
                
                ai_response = response.choices[0].message.content
                st.markdown(ai_response)
                
                # AI応答をセッション状態に追加
                st.session_state.messages.append({"role": "assistant", "content": ai_response})
                
            except Exception as e:
                error_message = f"エラーが発生しました: {str(e)}"
                st.error(error_message)
                st.session_state.messages.append({"role": "assistant", "content": error_message})

# サイドバー
with st.sidebar:
    st.header("⚙️ 設定")
    
    # チャット履歴のクリア
    if st.button("🗑️ チャット履歴をクリア", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    
    st.markdown("---")
    st.info("""
    **使い方：**
    1. 下のテキストボックスにメッセージを入力
    2. Enterキーを押すか送信ボタンをクリック
    3. AIからの返信が表示されます
    
    **注意：**
    - OpenAI APIの使用には料金がかかる場合があります
    - チャット履歴は最新10件まで保持されます
    """)
