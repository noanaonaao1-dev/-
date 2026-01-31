# GitHub & 管理画面 連携ガイド

このブログには、ブラウザから記事を投稿・更新できる「管理画面」があります。その仕組みと設定方法を解説します。

## 1. 仕組み
管理画面から「公開」ボタンを押すと、以下のことが起こります：
1. Cloudflare Workers があなたの代わりに GitHub API を叩きます。
2. GitHubのリポジトリに自動的にコミット＆プッシュされます。
3. Cloudflare Pages の自動ビルドが走り、数分後にサイトが更新されます。

## 2. 設定（準備するもの）
この機能を使うには、Cloudflare Pages の環境変数に以下を追加する必要があります。

- `GITHUB_TOKEN`: あなたの GitHub Personal Access Token。
  - 作成場所: GitHubの「Settings」→「Developer settings」→「Personal access tokens (classic)」
  - 権限: `repo` にチェックを入れてください。
- `GITHUB_REPO`: リポジトリ名（例: `yourname/py-auto-blog`）
- `GITHUB_BRANCH`: デプロイ対象のブランチ名（通常は `main`）

## 3. 注意点（ミスの要因）
- **トークンの有効期限:** 期限が切れると管理画面からの投稿ができなくなります。
- **直接編集との競合:** GitHub上で直接ファイルを編集した直後に管理画面を使うと、エラー（コンフリクト）が起きる場合があります。一度ローカルで `git pull` するか、最新の状態を確認してから操作してください。
