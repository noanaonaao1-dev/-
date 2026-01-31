# PROG-AUTO-LAB (Jules SSG)

Python製の多言語自動化ブログ・フレームワーク。

## 構成
- **SSG**: `jules.py` (Python)
- **Frontend**: Tailwind CSS
- **Dynamic Features**: Cloudflare Pages Functions
- **Hosting**: Cloudflare Pages

## ローカル開発
1. 依存関係のインストール:
   ```bash
   pip install -r requirements.txt
   ```
2. ビルド:
   ```bash
   python jules.py
   ```
3. `dist` ディレクトリの内容をプレビュー。

## Cloudflare Pagesへのデプロイ
1. GitHubリポジトリにプッシュ。
2. Cloudflare Pagesで新しいプロジェクトを作成。
3. ビルド設定:
   - フレームワーク プリセット: なし
   - ビルドコマンド: `python jules.py`
   - 出力ディレクトリ: `dist`
4. 環境変数の設定:
   - `ADMIN_PASSWORD`: 管理画面用のパスワード
   - `CLOUDFLARE_API_TOKEN`: KV同期用（オプション）
   - `CLOUDFLARE_ACCOUNT_ID`: KV同期用（オプション）
   - `CLOUDFLARE_KV_NAMESPACE_ID`: KV同期用（オプション）
5. KV名前空間 `BLOG_KV` を作成し、Pagesプロジェクトにバインドしてください。

## Monetagの設定
`templates/base.html` 内の `data-zone="YOUR_ZONE_ID"` をご自身のIDに書き換えてください。
