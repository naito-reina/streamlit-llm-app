import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
import os
from dotenv import load_dotenv
from pathlib import Path

# .envファイルから環境変数を読み込む
# app.pyと同じディレクトリの.envファイルを読み込む
env_path = Path(__file__).parent / '.env'
# .envファイルが存在する場合は読み込む
if env_path.exists():
    load_dotenv(dotenv_path=env_path)
else:
    # .envファイルが存在しない場合も、デフォルトの場所を試す
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
        if hasattr(st, 'secrets'):
            # Streamlit CloudのSecretsは辞書のようにアクセス可能
            # まず、直接アクセスを試みる
            try:
                api_key = st.secrets["OPENAI_API_KEY"]
            except (KeyError, TypeError):
                # 辞書形式でない場合、getメソッドを試す
                try:
                    api_key = st.secrets.get("OPENAI_API_KEY")
                except (AttributeError, TypeError):
                    pass
    except Exception:
        # エラーが発生した場合は無視して次へ
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
    
    **ローカル実行の場合（推奨）：**
    
    1. プロジェクトルート（`app.py`と同じディレクトリ）に`.env`ファイルを作成
    2. 以下の形式でご自身のOpenAI APIキーを記述：
       ```
       OPENAI_API_KEY=ご自身のOpenAI APIキー
       ```
    3. 文字列をクォーテーションで囲む必要はありません
    4. ファイルを保存して、アプリを再起動してください
    
    **Streamlit Cloudの場合：**
    
    1. https://share.streamlit.io/ にアクセスしてログイン
    2. ダッシュボードでアプリを選択
    3. 「Manage app」ボタンをクリック
    4. 「Secrets」タブ（またはセクション）をクリック
    5. テキストエリアに以下のいずれかの形式で**正確に**入力：
       ```toml
       OPENAI_API_KEY = "sk-あなたの実際のAPIキー"
       ```
       または
       ```
       OPENAI_API_KEY=sk-あなたの実際のAPIキー
       ```
    6. **必ず「Save」ボタンをクリック**して保存（重要！）
    7. 保存後、アプリが自動的に再デプロイされます（通常10-30秒）
    8. 再デプロイが完了するまで待ってから、このページをリロードしてください
    
    **よくある間違い：**
    - Secretsを入力したが、保存ボタンを押していない
    - 引用符の種類が間違っている（`'`ではなく`"`を使用）
    - 余分なスペースや改行が入っている
    - 再デプロイを待たずに確認している
    
    **詳細な手順は [`SETUP.md`](SETUP.md) を参照してください。**
    """)
    st.stop()

# LangChain ChatOpenAIの初期化
def get_chat_model():
    """LangChain ChatOpenAIモデルを取得"""
    if not api_key:
        return None
    try:
        return ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0.7,
            max_tokens=500,
            api_key=api_key
        )
    except Exception as e:
        st.error(f"ChatOpenAIモデルの初期化に失敗しました: {str(e)}")
        st.warning("""
        **このエラーは依存関係のバージョン互換性の問題です。**
        
        **解決方法：**
        1. `requirements.txt`を更新して、GitHubにプッシュしてください
        2. Streamlit Cloudでアプリが自動的に再デプロイされるまで待ってください（通常1-2分）
        3. 再デプロイ後、このページをリロードしてください
        
        **確認事項：**
        - `langchain-openai>=0.1.0`が`requirements.txt`に含まれているか
        - `langchain-core>=0.1.0`が`requirements.txt`に含まれているか
        - 変更をGitHubにプッシュしたか
        """)
        return None

chat_model = get_chat_model()
if chat_model is None:
    st.stop()

# セッション状態の初期化
if "messages" not in st.session_state:
    st.session_state.messages = []
if "expert_type" not in st.session_state:
    st.session_state.expert_type = "法務"

# 専門家の種類とシステムメッセージのマッピング
EXPERT_SYSTEM_MESSAGES = {
    "法務": "あなたは「社内法務ヘルプデスク一次受付ボット」です。目的は、社内メンバーの自己解決を促し、法務部への問い合わせ件数を減らすことです。",
    "営業": "あなたは「社内営業ヘルプデスク一次受付ボット」です。目的は、社内メンバーの自己解決を促し、営業部への問い合わせ件数を減らすことです。"
}

def generate_response(user_input: str, expert_type: str, messages: list, chat_model: ChatOpenAI) -> str:
    """
    入力されたテキストと専門家タイプから回答を生成する関数
    
    Args:
        user_input: ユーザーが入力したテキスト
        expert_type: ラジオボタンで選択された専門家タイプ（"法務"または"営業"）
        messages: 会話履歴のリスト（辞書形式: {"role": "user"/"assistant", "content": "..."}）
        chat_model: LangChainのChatOpenAIモデル
    
    Returns:
        str: AIの応答テキスト
    
    Raises:
        Exception: API呼び出し時にエラーが発生した場合
    """
    # 選択された専門家に応じたシステムメッセージを取得
    system_message_content = EXPERT_SYSTEM_MESSAGES.get(
        expert_type,
        "あなたは親切で役立つアシスタントです。日本語で丁寧に回答してください。"
    )
    
    # ChatPromptTemplateを作成
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", system_message_content),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}")
    ])
    
    # 会話履歴をLangChainのメッセージ形式に変換（最新10件まで）
    chat_history = []
    for msg in messages[-10:-1]:  # 最後のユーザーメッセージは除く
        if msg["role"] == "user":
            chat_history.append(HumanMessage(content=msg["content"]))
        elif msg["role"] == "assistant":
            chat_history.append(AIMessage(content=msg["content"]))
    
    # Chainを作成して実行
    chain = prompt_template | chat_model
    
    # 応答を生成
    response = chain.invoke({
        "chat_history": chat_history,
        "input": user_input
    })
    
    return response.content

# サイドバー
with st.sidebar:
    st.header("⚙️ 設定")
    
    # 専門家の選択
    st.subheader("👤 専門家の選択")
    expert_type = st.radio(
        "専門家の種類を選択してください：",
        options=["法務", "営業"],
        index=0 if st.session_state.expert_type == "法務" else 1,
        key="expert_radio"
    )
    
    # 専門家が変更された場合、セッション状態を更新
    if expert_type != st.session_state.expert_type:
        st.session_state.expert_type = expert_type
        st.info(f"専門家を「{expert_type}」に変更しました。")
    
    st.markdown("---")
    
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

# チャット履歴の表示
chat_container = st.container()
with chat_container:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# ユーザー入力
if user_input := st.chat_input("メッセージを入力してください..."):
    # ユーザーメッセージを追加
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # AI応答を生成
    with st.chat_message("assistant"):
        with st.spinner("考え中..."):
            try:
                # 関数を呼び出して応答を生成
                ai_response = generate_response(
                    user_input=user_input,
                    expert_type=st.session_state.expert_type,
                    messages=st.session_state.messages,
                    chat_model=chat_model
                )
                st.markdown(ai_response)
                
                # AI応答をセッション状態に追加
                st.session_state.messages.append({"role": "assistant", "content": ai_response})
                
            except Exception as e:
                error_message = f"エラーが発生しました: {str(e)}"
                st.error(error_message)
                st.session_state.messages.append({"role": "assistant", "content": error_message})
