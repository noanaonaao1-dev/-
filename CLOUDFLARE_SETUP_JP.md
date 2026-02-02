# Cloudflare Pages セットアップガイド

このプロジェクトを Cloudflare Pages で公開するための手順です。

## 1. Cloudflare Pages プロジェクトの作成
1. Cloudflare ダッシュボードにログインし、「Workers & Pages」へ移動します。
2. 「Create application」->「Pages」->「Connect to Git」を選択します。
3. このリポジトリを選択します。

## 2. ビルド設定
ビルド設定画面で以下を入力してください（**重要：デプロイコマンド欄は空欄にしてください**）：
- **Framework preset**: `None`
- **Build command**: `python jules.py`
- **Build output directory**: `dist`
- **Root directory**: （空欄）
- **Deployment command (デプロイコマンド)**: **（空欄・何も入力しない）**

※ GitHub連携を使用している場合、ビルド完了後に Cloudflare が自動でデプロイを行うため、追加のコマンドは不要です。

## 3. 環境変数の設定
「Settings（設定）」->「Environment variables（環境変数）」で以下の変数を追加します：

| 変数名 | 内容 |
| :--- | :--- |
| `ADMIN_PASSWORD` | 管理画面（/admin/）に入るためのパスワード。 |
| `CLOUDFLARE_API_TOKEN` | Cloudflare の API トークン（KVの読み書きに使用）。 |
| `CLOUDFLARE_ACCOUNT_ID` | Cloudflare のアカウント ID。 |
| `CLOUDFLARE_KV_NAMESPACE_ID` | 作成した KV 名前空間の ID。 |

**重要:** `CLOUDFLARE_` で始まる上記3つの変数を設定すると、ダッシュボードでの複雑なバインド設定なしで KV 機能が動作するようになります。

## 4. KV名前空間の作成
1. Cloudflare左メニューの「Workers & Pages」->「KV」を選択し、「名前空間を作成する」から `BLOG_KV` という名前で作成します。
2. 作成したPagesプロジェクトの個別ページを開きます。
3. 上部のタブから **「設定 (Settings)」** を選択します。
4. 左側のサイドバーにある **「Functions（または関数）」** をクリックします。
   - ※もし左側に「Functions」がない場合は、「ビルドとデプロイ」の下の方を確認するか、画面を下にスクロールしてみてください。
5. ページ中央の「KV名前空間のバインド (KV namespace bindings)」というセクションを見つけ、**「バインドを編集する (Edit binding)」** をクリックします。
6. **「バインドを追加する (Add binding)」** をクリックし、以下を入力します：
   - **変数名 (Variable name)**: `BLOG_KV`
   - **KV名前空間**: 先ほど作成した `BLOG_KV` を選択。
7. 「保存」をクリックします。

## 5. デプロイ
GitHubへ `push` すると自動的にビルドとデプロイが開始されます。
