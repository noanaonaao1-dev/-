# 記事投稿・装飾ガイド

1つのファイルで英語（EN）と日本語（JP）の両方を管理します。

## 基本フォーマット
`content/` フォルダに `.html` ファイルを作成し、以下の形式で記述します。

```html
---
slug: my-new-tool
date: "2024-01-31"
tags: ["python", "automation"]
popular: true (人気記事にする場合)
---

[EN]
TITLE: English Title
DESC: Short description for search and cards.
BODY:
<p>English content here...</p>
[/EN]

[JP]
TITLE: 日本語のタイトル
DESC: 検索結果やカードに表示される短い説明文。
BODY:
<p>日本語のコンテンツをここに書きます...</p>
[/JP]
```

## 多彩な表現（装飾クラス）
より詳細なデザインガイドは `CSS_STYLE_GUIDE_JP.txt` を参照してください。
`BODY:` セクション内で以下のHTMLクラスを使用して、記事を装飾できます。

### 1. メッセージボックス
- `<div class="alert-info">...</div>`: 青色の情報ボックス
- `<div class="alert-success">...</div>`: 緑色の成功・Tipsボックス
- `<div class="alert-warning">...</div>`: 黄色の警告・注意ボックス

### 2. 強調・リスト
- プログラミングコードは `<pre><code>...</code></pre>` で囲むとコピーボタンが自動付与されます。
- `prose` クラスが適用されているため、標準的な `<h1>`, `<h2>`, `<ul>`, `<ol>` 等は自動で綺麗にスタイリングされます。

## 静的フォールバック
Cloudflare Workers（Functions）の無料枠制限に達した場合でも、検索機能は `metadata.json` を直接読み込むモードに自動で切り替わり、継続して動作します（統計機能のみ停止します）。
