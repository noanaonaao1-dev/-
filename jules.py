import os
import yaml
import json
from jinja2 import Environment, FileSystemLoader
from datetime import datetime
import re

class JulesSSG:
    def __init__(self, content_dir='content', template_dir='templates', dist_dir='dist'):
        self.content_dir = content_dir
        self.template_dir = template_dir
        self.dist_dir = dist_dir
        self.env = Environment(loader=FileSystemLoader(template_dir))
        self.pages = []

    def parse_file(self, filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        frontmatter = {}
        # Try to parse YAML frontmatter
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                try:
                    frontmatter = yaml.safe_load(parts[1])
                    content = parts[2]
                except yaml.YAMLError:
                    pass

        # If title not in frontmatter, try extracting from <title> tag
        if 'title' not in frontmatter:
            title_match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE | re.DOTALL)
            if title_match:
                frontmatter['title'] = title_match.group(1).strip()
            else:
                frontmatter['title'] = os.path.basename(filepath)

        # Default values
        if 'date' not in frontmatter:
            frontmatter['date'] = datetime.now().strftime('%Y-%m-%d')

        return frontmatter, content

    def build(self):
        if not os.path.exists(self.dist_dir):
            os.makedirs(self.dist_dir)

        # Process articles
        for lang in ['en', 'jp']:
            lang_dir = os.path.join(self.content_dir, lang)
            dist_lang_dir = os.path.join(self.dist_dir, lang)
            if not os.path.exists(lang_dir):
                continue
            if not os.path.exists(dist_lang_dir):
                os.makedirs(dist_lang_dir)

            for root, _, files in os.walk(lang_dir):
                for file in files:
                    if file.endswith('.html'):
                        src_path = os.path.join(root, file)
                        rel_path = os.path.relpath(src_path, lang_dir)
                        dest_path = os.path.join(dist_lang_dir, rel_path)

                        os.makedirs(os.path.dirname(dest_path), exist_ok=True)

                        metadata, body = self.parse_file(src_path)
                        metadata['lang'] = lang
                        metadata['url'] = f'/{lang}/{rel_path}'
                        self.pages.append(metadata)

                        template = self.env.get_template('article.html')
                        output = template.render(content=body, meta=metadata, pages=self.pages, lang=lang)

                        with open(dest_path, 'w', encoding='utf-8') as f:
                            f.write(output)

        # Generate index pages
        for lang in ['en', 'jp']:
            lang_pages = [p for p in self.pages if p['lang'] == lang]
            lang_pages.sort(key=lambda x: x['date'], reverse=True)

            template = self.env.get_template('index.html')
            output = template.render(pages=lang_pages, lang=lang)

            index_path = os.path.join(self.dist_dir, lang, 'index.html')
            with open(index_path, 'w', encoding='utf-8') as f:
                f.write(output)

        # Admin page
        admin_dist = os.path.join(self.dist_dir, 'admin')
        os.makedirs(admin_dist, exist_ok=True)
        admin_template = self.env.get_template('admin.html')
        with open(os.path.join(admin_dist, 'index.html'), 'w', encoding='utf-8') as f:
            f.write(admin_template.render())

        # Root redirect or simple index
        root_index = """<!DOCTYPE html><html><head><meta http-equiv="refresh" content="0;url=/jp/"></head></html>"""
        with open(os.path.join(self.dist_dir, 'index.html'), 'w') as f:
            f.write(root_index)

        # Export metadata for KV
        with open(os.path.join(self.dist_dir, 'metadata.json'), 'w', encoding='utf-8') as f:
            json.dump(self.pages, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    ssg = JulesSSG()
    ssg.build()
    print("Build complete!")
