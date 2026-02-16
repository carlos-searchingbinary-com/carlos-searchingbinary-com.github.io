#!/usr/bin/env python3
"""
SearchingBinary Blog Builder

Usage:
    python3 build-blog.py

Reads .md files from blog/posts/, generates:
    - blog/index.html        (blog listing page)
    - blog/<slug>/index.html  (individual post pages)

Markdown files must have YAML-style frontmatter:
    ---
    title: My Post Title
    description: A short summary for SEO.
    date: 2026-02-16
    author: Carlos Martins
    tags: tag1, tag2
    ---

    Post content in markdown...
"""

import os
import re
import glob
import markdown
from datetime import datetime

DIR = os.path.dirname(os.path.abspath(__file__))
POSTS_DIR = os.path.join(DIR, "blog", "posts")
BLOG_DIR = os.path.join(DIR, "blog")
SITE_URL = "https://searchingbinary.com"

# ─── Brand colors & styles (matching main site) ───

POST_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | SearchingBinary Blog</title>
    <meta name="description" content="{description}">
    <link rel="canonical" href="{canonical_url}">

    <link rel="icon" type="image/x-icon" href="/favicon.ico">
    <link rel="icon" type="image/png" sizes="32x32" href="/assets/logos/favicon-32x32.png">
    <link rel="apple-touch-icon" sizes="180x180" href="/assets/logos/apple-touch-icon-180x180.png">

    <meta property="og:type" content="article">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{description}">
    <meta property="og:url" content="{canonical_url}">
    <meta property="og:site_name" content="SearchingBinary">
    <meta property="og:image" content="{site_url}/assets/logos/og-image-1200x630.png">
    <meta property="article:published_time" content="{iso_date}">
    <meta property="article:author" content="{author}">
    <meta name="twitter:card" content="summary_large_image">

    <meta name="theme-color" content="#0a1628">

    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": "{title}",
        "description": "{description}",
        "datePublished": "{iso_date}",
        "author": {{
            "@type": "Person",
            "name": "{author}",
            "url": "https://www.linkedin.com/in/cmartinspt/"
        }},
        "publisher": {{
            "@type": "Organization",
            "name": "SearchingBinary",
            "logo": {{
                "@type": "ImageObject",
                "url": "{site_url}/assets/logos/logo-full-dark-800x200.png"
            }}
        }},
        "mainEntityOfPage": "{canonical_url}",
        "keywords": "{tags}"
    }}
    </script>

    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;1,9..40,300;1,9..40,400&display=swap" rel="stylesheet">
    <style>
        *, *::before, *::after {{ margin: 0; padding: 0; box-sizing: border-box; }}

        :root {{
            --navy: #0a1628;
            --navy-soft: #1a2a44;
            --gold: #c8a45e;
            --gold-light: #e8d5a0;
            --gold-pale: #f5ecd4;
            --cream: #faf8f4;
            --white: #ffffff;
            --gray-100: #f4f3f1;
            --gray-200: #e8e6e2;
            --gray-400: #a09b93;
            --gray-600: #6b6560;
            --text: #1a1714;
            --text-secondary: #5a554f;
            --font-serif: 'Instrument Serif', Georgia, serif;
            --font-sans: 'DM Sans', -apple-system, sans-serif;
        }}

        html {{ scroll-behavior: smooth; -webkit-font-smoothing: antialiased; }}
        body {{ font-family: var(--font-sans); color: var(--text); background: var(--cream); line-height: 1.6; }}

        nav {{
            padding: 1.5rem 3rem;
            display: flex;
            align-items: center;
            justify-content: space-between;
            border-bottom: 1px solid var(--gray-200);
        }}

        .nav-logo {{
            font-family: var(--font-serif);
            font-size: 1.35rem;
            color: var(--navy);
            text-decoration: none;
            letter-spacing: -0.01em;
        }}
        .nav-logo span {{ color: var(--gold); }}

        .nav-links {{
            display: flex;
            gap: 2.5rem;
            list-style: none;
        }}
        .nav-links a {{
            font-size: 0.85rem;
            font-weight: 400;
            color: var(--gray-600);
            text-decoration: none;
            letter-spacing: 0.06em;
            text-transform: uppercase;
            transition: color 0.3s ease;
        }}
        .nav-links a:hover {{ color: var(--navy); }}

        .post-header {{
            max-width: 720px;
            margin: 5rem auto 3rem;
            padding: 0 2rem;
        }}

        .post-meta {{
            font-size: 0.8rem;
            font-weight: 400;
            letter-spacing: 0.1em;
            text-transform: uppercase;
            color: var(--gold);
            margin-bottom: 1rem;
        }}

        .post-header h1 {{
            font-family: var(--font-serif);
            font-size: clamp(2rem, 4vw, 3rem);
            font-weight: 400;
            color: var(--navy);
            letter-spacing: -0.02em;
            line-height: 1.15;
        }}

        .post-header .description {{
            font-size: 1.1rem;
            font-weight: 300;
            color: var(--text-secondary);
            margin-top: 1rem;
            line-height: 1.6;
        }}

        .post-divider {{
            width: 48px;
            height: 1px;
            background: var(--gold);
            margin: 2rem 0;
        }}

        .post-content {{
            max-width: 720px;
            margin: 0 auto 5rem;
            padding: 0 2rem;
        }}

        .post-content h2 {{
            font-family: var(--font-serif);
            font-size: 1.8rem;
            font-weight: 400;
            color: var(--navy);
            margin: 2.5rem 0 1rem;
            letter-spacing: -0.01em;
        }}

        .post-content h3 {{
            font-family: var(--font-serif);
            font-size: 1.3rem;
            font-weight: 400;
            color: var(--navy);
            margin: 2rem 0 0.75rem;
        }}

        .post-content p {{
            font-size: 1rem;
            font-weight: 300;
            color: var(--text-secondary);
            line-height: 1.85;
            margin-bottom: 1.25rem;
        }}

        .post-content strong {{
            font-weight: 500;
            color: var(--text);
        }}

        .post-content a {{
            color: var(--gold);
            text-decoration: underline;
            text-underline-offset: 3px;
            transition: color 0.3s ease;
        }}
        .post-content a:hover {{ color: var(--navy); }}

        .post-content ul, .post-content ol {{
            margin: 1rem 0 1.25rem 1.5rem;
            color: var(--text-secondary);
        }}
        .post-content li {{
            font-size: 1rem;
            font-weight: 300;
            line-height: 1.85;
            margin-bottom: 0.5rem;
        }}

        .post-content blockquote {{
            border-left: 2px solid var(--gold);
            padding-left: 1.5rem;
            margin: 1.5rem 0;
            font-style: italic;
            color: var(--gray-600);
        }}

        .post-content code {{
            font-size: 0.9em;
            background: var(--gray-100);
            padding: 0.15rem 0.4rem;
            border-radius: 3px;
        }}

        .post-content pre {{
            background: var(--navy);
            color: var(--cream);
            padding: 1.5rem;
            border-radius: 4px;
            overflow-x: auto;
            margin: 1.5rem 0;
        }}
        .post-content pre code {{
            background: none;
            padding: 0;
            color: inherit;
        }}

        .post-tags {{
            display: flex;
            gap: 0.5rem;
            flex-wrap: wrap;
            margin-top: 1rem;
        }}

        .post-tag {{
            font-size: 0.7rem;
            font-weight: 400;
            letter-spacing: 0.05em;
            text-transform: uppercase;
            color: var(--gray-600);
            background: var(--gray-100);
            padding: 0.3rem 0.7rem;
            border-radius: 2px;
        }}

        .back-link {{
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            font-size: 0.85rem;
            font-weight: 400;
            letter-spacing: 0.05em;
            text-transform: uppercase;
            color: var(--gray-600);
            text-decoration: none;
            transition: color 0.3s ease;
        }}
        .back-link:hover {{ color: var(--navy); }}

        footer {{
            background: var(--navy);
            border-top: 1px solid rgba(200, 164, 94, 0.1);
            padding: 2rem 3rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .footer-logo {{
            font-family: var(--font-serif);
            font-size: 1rem;
            color: rgba(250, 248, 244, 0.4);
        }}
        .footer-logo span {{ color: var(--gold); opacity: 0.5; }}
        .footer-copy {{
            font-size: 0.75rem;
            font-weight: 300;
            color: rgba(250, 248, 244, 0.25);
        }}

        ::selection {{ background: var(--gold-pale); color: var(--navy); }}

        @media (max-width: 768px) {{
            nav {{ padding: 1rem 1.5rem; }}
            .nav-links {{ display: none; }}
            .post-header, .post-content {{ padding: 0 1.5rem; }}
            .post-header {{ margin-top: 3rem; }}
        }}
    </style>
</head>
<body>
    <nav aria-label="Main navigation">
        <a href="/" class="nav-logo" aria-label="SearchingBinary - Home">Searching<span>Binary</span></a>
        <ul class="nav-links">
            <li><a href="/#services">Services</a></li>
            <li><a href="/#about">About</a></li>
            <li><a href="/blog/">Blog</a></li>
            <li><a href="/#contact">Contact</a></li>
        </ul>
    </nav>

    <main>
        <article>
            <div class="post-header">
                <a href="/blog/" class="back-link">&larr; All posts</a>
                <p class="post-meta">{date_display} &middot; {author}</p>
                <h1>{title}</h1>
                <p class="description">{description}</p>
                <div class="post-tags">
                    {tags_html}
                </div>
                <div class="post-divider"></div>
            </div>

            <div class="post-content">
                {content}
            </div>
        </article>
    </main>

    <footer>
        <div class="footer-logo">Searching<span>Binary</span></div>
        <p class="footer-copy">&copy; 2026 SearchingBinary. All rights reserved.</p>
    </footer>
</body>
</html>"""

INDEX_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Blog | SearchingBinary</title>
    <meta name="description" content="Insights on investment, business strategy, AI, cloud, and technology leadership from SearchingBinary.">
    <link rel="canonical" href="{site_url}/blog/">

    <link rel="icon" type="image/x-icon" href="/favicon.ico">
    <link rel="icon" type="image/png" sizes="32x32" href="/assets/logos/favicon-32x32.png">
    <link rel="apple-touch-icon" sizes="180x180" href="/assets/logos/apple-touch-icon-180x180.png">

    <meta property="og:type" content="website">
    <meta property="og:title" content="Blog | SearchingBinary">
    <meta property="og:description" content="Insights on investment, business strategy, AI, cloud, and technology leadership.">
    <meta property="og:url" content="{site_url}/blog/">
    <meta property="og:site_name" content="SearchingBinary">
    <meta property="og:image" content="{site_url}/assets/logos/og-image-1200x630.png">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="theme-color" content="#0a1628">

    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;1,9..40,300;1,9..40,400&display=swap" rel="stylesheet">
    <style>
        *, *::before, *::after {{ margin: 0; padding: 0; box-sizing: border-box; }}

        :root {{
            --navy: #0a1628;
            --navy-soft: #1a2a44;
            --gold: #c8a45e;
            --gold-light: #e8d5a0;
            --gold-pale: #f5ecd4;
            --cream: #faf8f4;
            --white: #ffffff;
            --gray-100: #f4f3f1;
            --gray-200: #e8e6e2;
            --gray-400: #a09b93;
            --gray-600: #6b6560;
            --text: #1a1714;
            --text-secondary: #5a554f;
            --font-serif: 'Instrument Serif', Georgia, serif;
            --font-sans: 'DM Sans', -apple-system, sans-serif;
            --ease-out-expo: cubic-bezier(0.16, 1, 0.3, 1);
        }}

        html {{ scroll-behavior: smooth; -webkit-font-smoothing: antialiased; }}
        body {{ font-family: var(--font-sans); color: var(--text); background: var(--cream); line-height: 1.6; }}

        nav {{
            padding: 1.5rem 3rem;
            display: flex;
            align-items: center;
            justify-content: space-between;
            border-bottom: 1px solid var(--gray-200);
        }}
        .nav-logo {{
            font-family: var(--font-serif);
            font-size: 1.35rem;
            color: var(--navy);
            text-decoration: none;
            letter-spacing: -0.01em;
        }}
        .nav-logo span {{ color: var(--gold); }}
        .nav-links {{
            display: flex;
            gap: 2.5rem;
            list-style: none;
        }}
        .nav-links a {{
            font-size: 0.85rem;
            font-weight: 400;
            color: var(--gray-600);
            text-decoration: none;
            letter-spacing: 0.06em;
            text-transform: uppercase;
            transition: color 0.3s ease;
        }}
        .nav-links a:hover {{ color: var(--navy); }}

        .blog-header {{
            max-width: 900px;
            margin: 5rem auto 4rem;
            padding: 0 2rem;
        }}
        .section-label {{
            font-size: 0.75rem;
            font-weight: 500;
            letter-spacing: 0.2em;
            text-transform: uppercase;
            color: var(--gold);
            margin-bottom: 1rem;
        }}
        .blog-header h1 {{
            font-family: var(--font-serif);
            font-size: clamp(2rem, 4vw, 3.2rem);
            font-weight: 400;
            color: var(--navy);
            letter-spacing: -0.02em;
            line-height: 1.15;
        }}
        .section-divider {{
            width: 48px;
            height: 1px;
            background: var(--gold);
            margin: 2rem 0;
        }}

        .posts-list {{
            max-width: 900px;
            margin: 0 auto 5rem;
            padding: 0 2rem;
        }}

        .post-item {{
            display: block;
            text-decoration: none;
            padding: 2.5rem 0;
            border-bottom: 1px solid var(--gray-200);
            transition: padding-left 0.4s var(--ease-out-expo);
        }}
        .post-item:first-child {{
            border-top: 1px solid var(--gray-200);
        }}
        .post-item:hover {{
            padding-left: 1rem;
        }}

        .post-item-date {{
            font-size: 0.75rem;
            font-weight: 400;
            letter-spacing: 0.1em;
            text-transform: uppercase;
            color: var(--gold);
            margin-bottom: 0.5rem;
        }}

        .post-item-title {{
            font-family: var(--font-serif);
            font-size: 1.5rem;
            color: var(--navy);
            margin-bottom: 0.5rem;
            letter-spacing: -0.01em;
            transition: color 0.3s ease;
        }}
        .post-item:hover .post-item-title {{
            color: var(--gold);
        }}

        .post-item-desc {{
            font-size: 0.95rem;
            font-weight: 300;
            color: var(--text-secondary);
            line-height: 1.6;
        }}

        .post-item-tags {{
            display: flex;
            gap: 0.5rem;
            flex-wrap: wrap;
            margin-top: 0.75rem;
        }}
        .post-tag {{
            font-size: 0.65rem;
            font-weight: 400;
            letter-spacing: 0.05em;
            text-transform: uppercase;
            color: var(--gray-600);
            background: var(--gray-100);
            padding: 0.2rem 0.6rem;
            border-radius: 2px;
        }}

        footer {{
            background: var(--navy);
            border-top: 1px solid rgba(200, 164, 94, 0.1);
            padding: 2rem 3rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .footer-logo {{
            font-family: var(--font-serif);
            font-size: 1rem;
            color: rgba(250, 248, 244, 0.4);
        }}
        .footer-logo span {{ color: var(--gold); opacity: 0.5; }}
        .footer-copy {{
            font-size: 0.75rem;
            font-weight: 300;
            color: rgba(250, 248, 244, 0.25);
        }}

        ::selection {{ background: var(--gold-pale); color: var(--navy); }}

        @media (max-width: 768px) {{
            nav {{ padding: 1rem 1.5rem; }}
            .nav-links {{ display: none; }}
            .blog-header, .posts-list {{ padding: 0 1.5rem; }}
            .blog-header {{ margin-top: 3rem; }}
        }}
    </style>
</head>
<body>
    <nav aria-label="Main navigation">
        <a href="/" class="nav-logo" aria-label="SearchingBinary - Home">Searching<span>Binary</span></a>
        <ul class="nav-links">
            <li><a href="/#services">Services</a></li>
            <li><a href="/#about">About</a></li>
            <li><a href="/blog/">Blog</a></li>
            <li><a href="/#contact">Contact</a></li>
        </ul>
    </nav>

    <main>
        <div class="blog-header">
            <p class="section-label">Insights</p>
            <h1>Thoughts on strategy, technology, and building</h1>
            <div class="section-divider"></div>
        </div>

        <div class="posts-list">
            {posts_html}
        </div>
    </main>

    <footer>
        <div class="footer-logo">Searching<span>Binary</span></div>
        <p class="footer-copy">&copy; 2026 SearchingBinary. All rights reserved.</p>
    </footer>
</body>
</html>"""

POST_ITEM_TEMPLATE = """<a href="/blog/{slug}/" class="post-item">
    <p class="post-item-date">{date_display}</p>
    <h2 class="post-item-title">{title}</h2>
    <p class="post-item-desc">{description}</p>
    <div class="post-item-tags">
        {tags_html}
    </div>
</a>"""


def parse_frontmatter(content):
    """Parse YAML-style frontmatter from markdown content."""
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)', content, re.DOTALL)
    if not match:
        return {}, content

    meta = {}
    for line in match.group(1).strip().split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            meta[key.strip()] = value.strip()

    return meta, match.group(2)


def slugify(filename):
    """Convert filename to URL slug: 2026-02-16-my-post.md -> my-post"""
    name = os.path.splitext(os.path.basename(filename))[0]
    # Remove date prefix
    name = re.sub(r'^\d{4}-\d{2}-\d{2}-', '', name)
    return name


def format_date(date_str):
    """Format date string for display."""
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        return dt.strftime("%B %d, %Y")
    except (ValueError, TypeError):
        return date_str


def build_tags_html(tags_str):
    """Convert comma-separated tags to HTML."""
    if not tags_str:
        return ""
    tags = [t.strip() for t in tags_str.split(",")]
    return "\n".join(f'<span class="post-tag">{tag}</span>' for tag in tags if tag)


def build():
    """Build all blog pages."""
    md = markdown.Markdown(extensions=['extra', 'codehilite', 'toc'])

    # Find all posts
    post_files = sorted(glob.glob(os.path.join(POSTS_DIR, "*.md")), reverse=True)

    if not post_files:
        print("No posts found in blog/posts/")
        return

    posts = []

    for filepath in post_files:
        with open(filepath, 'r') as f:
            raw = f.read()

        meta, body = parse_frontmatter(raw)
        slug = slugify(filepath)
        title = meta.get('title', slug.replace('-', ' ').title())
        description = meta.get('description', '')
        date = meta.get('date', '')
        author = meta.get('author', 'SearchingBinary')
        tags = meta.get('tags', '')

        # Convert markdown to HTML
        md.reset()
        html_content = md.convert(body)

        # Build post page
        post_dir = os.path.join(BLOG_DIR, slug)
        os.makedirs(post_dir, exist_ok=True)

        post_html = POST_TEMPLATE.format(
            title=title,
            description=description,
            canonical_url=f"{SITE_URL}/blog/{slug}/",
            site_url=SITE_URL,
            iso_date=date,
            date_display=format_date(date),
            author=author,
            tags=tags,
            tags_html=build_tags_html(tags),
            content=html_content,
        )

        post_path = os.path.join(post_dir, "index.html")
        with open(post_path, 'w') as f:
            f.write(post_html)

        print(f"  Built: blog/{slug}/index.html")

        posts.append({
            'title': title,
            'description': description,
            'date': date,
            'date_display': format_date(date),
            'slug': slug,
            'tags': tags,
            'tags_html': build_tags_html(tags),
        })

    # Sort by frontmatter date (newest first)
    posts.sort(key=lambda p: p['date'], reverse=True)

    # Build index page
    posts_html = "\n".join(
        POST_ITEM_TEMPLATE.format(**post) for post in posts
    )

    index_html = INDEX_TEMPLATE.format(
        site_url=SITE_URL,
        posts_html=posts_html,
    )

    index_path = os.path.join(BLOG_DIR, "index.html")
    with open(index_path, 'w') as f:
        f.write(index_html)

    print(f"  Built: blog/index.html ({len(posts)} posts)")
    print(f"\nDone! {len(posts)} post(s) generated.")


if __name__ == "__main__":
    print("Building SearchingBinary blog...\n")
    build()
