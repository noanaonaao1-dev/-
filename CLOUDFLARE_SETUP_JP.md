# Cloudflare Pages セットアップガイド

このプロジェクトを Cloudflare Pages で公開するための手順です。

## 1. Cloudflare Pages プロジェクトの作成
1. Cloudflare ダッシュボードにログインし、「Workers & Pages」へ移動します。
2. 「Create application」->「Pages」->「Connect to Git」を選択します。
3. このリポジトリを選択します。

## 2. ビルド設定
ビルド設定画面で以下を入力してください：
- **Framework preset**: `None`
- **Build command**: `python jules.py`
- **Output directory**: `dist`

## 3. 環境変数の設定
「Settings」->「Environment variables」で以下の変数を追加します：
- `ADMIN_PASSWORD`: 管理画面（/admin/）に入るためのパスワード。
- (任意) `CLOUDFLARE_API_TOKEN`: KV同期用。
- (任意) `CLOUDFLARE_ACCOUNT_ID`: KV同期用。
- (任意) `CLOUDFLARE_KV_NAMESPACE_ID`: KV同期用。

## 4. KV名前空間のバインド
1. 「Workers & Pages」->「KV」で新しい名前空間（例：`BLOG_KV`）を作成します。
2. Pagesプロジェクトの「Settings」->「Functions」->「KV namespace bindings」へ移動します。
3. 「Variable name」に `BLOG_KV` を入力し、作成した名前空間を選択して保存します。

## 5. デプロイ
GitHubへ `push` すると自動的にビルドとデプロイが開始されます。
