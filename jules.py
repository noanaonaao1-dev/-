import os
import yaml
import json
import markdown
from jinja2 import Environment, FileSystemLoader
from datetime import datetime, date
import re
from sync_kv import sync_kv

class JulesSSG:
    def __init__(self, content_dir='content', template_dir='templates', dist_dir='dist'):
        self.content_dir = content_dir
        self.template_dir = template_dir
        self.dist_dir = dist_dir
        self.env = Environment(loader=FileSystemLoader(template_dir))
        self.pages = []

    def parse_block(self, block_text):
        res = {}
        title_match = re.search(r'^TITLE:\s*(.*)$', block_text, re.M)
        desc_match = re.search(r'^DESC:\s*(.*)$', block_text, re.M)
        body_match = re.search(r'^BODY:\s*(.*)$', block_text, re.S | re.M)

        if title_match: res['title'] = title_match.group(1).strip()
        if desc_match: res['description'] = desc_match.group(1).strip()

        raw_body = ""
        if body_match:
            raw_body = body_match.group(1).strip()
        else:
            lines = block_text.split('\n')
            body_lines = [l for l in lines if not l.startswith('TITLE:') and not l.startswith('DESC:')]
            raw_body = '\n'.join(body_lines).strip()

        # Convert Markdown to HTML for the body
        res['body'] = markdown.markdown(raw_body, extensions=['extra', 'nl2br'])

        return res

    def parse_file(self, filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            raw_content = f.read()

        shared_meta = {}
        if raw_content.startswith('---'):
            parts = raw_content.split('---', 2)
            if len(parts) >= 3:
                try:
                    shared_meta = yaml.safe_load(parts[1])
                    body_area = parts[2]
                except yaml.YAMLError:
                    body_area = raw_content
            else:
                body_area = raw_content
        else:
            body_area = raw_content

        langs = {}
        for lang in ['EN', 'JP']:
            pattern = rf'\[{lang}\](.*?)\[/{lang}\]'
            match = re.search(pattern, body_area, re.S)
            if match:
                langs[lang.lower()] = self.parse_block(match.group(1))

        if 'slug' not in shared_meta:
            shared_meta['slug'] = os.path.splitext(os.path.basename(filepath))[0]

        if 'date' not in shared_meta:
            shared_meta['date'] = datetime.now().strftime('%Y-%m-%d')
        elif isinstance(shared_meta['date'], (datetime, date)):
            shared_meta['date'] = shared_meta['date'].strftime('%Y-%m-%d')

        if 'time' not in shared_meta:
            shared_meta['time'] = 5

        if 'env' not in shared_meta:
            shared_meta['env'] = 'None'

        return shared_meta, langs

    def build(self):
        if not os.path.exists(self.dist_dir):
            os.makedirs(self.dist_dir)

        # Process articles
        for root, _, files in os.walk(self.content_dir):
            for file in files:
                if file.endswith('.html') or file.endswith('.md'):
                    src_path = os.path.join(root, file)
                    shared_meta, lang_data = self.parse_file(src_path)

                    for lang, data in lang_data.items():
                        dist_lang_dir = os.path.join(self.dist_dir, lang)
                        os.makedirs(dist_lang_dir, exist_ok=True)

                        dest_path = os.path.join(dist_lang_dir, f"{shared_meta['slug']}.html")

                        metadata = shared_meta.copy()
                        metadata.update(data)
                        metadata['lang'] = lang
                        metadata['url'] = f'/{lang}/{shared_meta["slug"]}.html'
                        metadata['stats_id'] = shared_meta['slug']

                        self.pages.append(metadata)

                        template = self.env.get_template('article.html')
                        output = template.render(content=data['body'], meta=metadata, pages=self.pages, lang=lang)

                        with open(dest_path, 'w', encoding='utf-8') as f:
                            f.write(output)

        # Generate index pages
        for lang in ['en', 'jp']:
            lang_pages = [p for p in self.pages if p['lang'] == lang]
            lang_pages.sort(key=lambda x: x['date'], reverse=True)

            template = self.env.get_template('index.html')
            output = template.render(pages=lang_pages, lang=lang, all_pages=self.pages)

            os.makedirs(os.path.join(self.dist_dir, lang), exist_ok=True)
            index_path = os.path.join(self.dist_dir, lang, 'index.html')
            with open(index_path, 'w', encoding='utf-8') as f:
                f.write(output)

        # Root redirect with language detection
        root_index = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>PROG-AUTO-LAB</title>
    <script>
        (function() {
            var lang = navigator.language || navigator.userLanguage;
            if (lang && lang.toLowerCase().startsWith('ja')) {
                window.location.href = '/jp/';
            } else {
                window.location.href = '/en/';
            }
        })();
    </script>
    <noscript>
        <meta http-equiv="refresh" content="0;url=/en/">
    </noscript>
</head>
<body>
    <p>Redirecting... <a href="/en/">Click here</a> if you are not redirected.</p>
</body>
</html>"""
        with open(os.path.join(self.dist_dir, 'index.html'), 'w') as f:
            f.write(root_index)

        # Export metadata for KV
        with open(os.path.join(self.dist_dir, 'metadata.json'), 'w', encoding='utf-8') as f:
            json.dump(self.pages, f, ensure_ascii=False, indent=2)

        # Admin page
        admin_dist = os.path.join(self.dist_dir, 'admin')
        os.makedirs(admin_dist, exist_ok=True)
        admin_template = self.env.get_template('admin.html')
        with open(os.path.join(admin_dist, 'index.html'), 'w', encoding='utf-8') as f:
            f.write(admin_template.render())

        # Optional: Sync to Cloudflare KV if credentials exist
        sync_kv()

if __name__ == '__main__':
    ssg = JulesSSG()
    ssg.build()
    print("Build complete!")
