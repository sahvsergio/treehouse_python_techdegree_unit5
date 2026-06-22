import os
import requests
import traceback
from dotenv import load_dotenv

# Automatically injects everything from your .env file into os.getenv()
load_dotenv()  

# --- TREEHOUSE & WORDPRESS PIPELINES ---

def get_treehouse_data():
    TREEHOUSE_DATA = os.getenv('TREEHOUSE_DATA')
    try:
        response = requests.get(TREEHOUSE_DATA)
        response.raise_for_status()
        return response.json()
    except Exception:
        print("❌ ERROR: Treehouse fetch failed.")
        traceback.print_exc()
        return {}

def extract_wordpress_blog():
    wordpress_url = os.getenv('ESL_BUFF_URL')
    try:
        response = requests.get(wordpress_url)
        response.raise_for_status()
        posts_json = response.json()
        
        wordpress_elements = []
        for post in posts_json[:3]:
            title = post.get('title', {}).get('rendered', 'Untitled')
            link = post.get('link', '#')
            raw_excerpt = post.get('excerpt', {}).get('rendered', 'No description available.')
            
            wordpress_elements.append({
                'title': title,
                'url': link,
                'source': 'WordPress',
                'description': raw_excerpt[:150] + "..." if len(raw_excerpt) > 150 else raw_excerpt
            })
        print("✅ SUCCESS: Extracted WordPress items.")
        return wordpress_elements
    except Exception:
        print("❌ ERROR: WordPress extraction failed.")
        traceback.print_exc()
        return []


# --- INDEPENDENT BLOGGER PIPELINES ---

def extract_blogger_sahvsergio():
    """Extracts from your first individual Blogger setup."""
    blog_id = os.getenv('SAHVSERGIO_BLOG_ID')
    api_key = os.getenv('BLOGGER_API_KEY')
    if not blog_id or not api_key: return []
    
    try:
        url = f"https://www.googleapis.com/blogger/v3/blogs/{blog_id}/posts?key={api_key}"
        response = requests.get(url)
        response.raise_for_status()
        posts = response.json().get('items', [])
        
        elements = []
        for post in posts[:3]:
            elements.append({
                'title': post.get('title', 'Untitled'),
                'url': post.get('url', '#'),
                'source': 'Blogger - Site sahvsergio',
                'description': post.get('content', '')[:150] + "..."
            })
        print(f"✅ SUCCESS: Extracted Blogger sahvsergio ({blog_id[:6]}...)")
        return elements
    except Exception:
        print("❌ ERROR: Blogger One failed.")
        traceback.print_exc()
        return []


def extract_blogger_unana():
    """Extracts from your second individual Blogger setup."""
    blog_id = os.getenv('UNANA_BLOG')
    api_key = os.getenv('BLOGGER_API_KEY')
    if not blog_id or not api_key: return []
    
    try:
        url = f"https://www.googleapis.com/blogger/v3/blogs/{blog_id}/posts?key={api_key}"
        response = requests.get(url)
        response.raise_for_status()
        posts = response.json().get('items', [])
        
        elements = []
        for post in posts[:3]:
            elements.append({
                'title': post.get('title', 'Untitled'),
                'url': post.get('url', '#'),
                'source': 'Blogger - unana',
                'description': post.get('content', '')[:150] + "..."
            })
        print(f"✅ SUCCESS: Extracted Blogger unana ({blog_id[:6]}...)")
        return elements
    except Exception:
        print("❌ ERROR: Blogger unana failed.")
        traceback.print_exc()
        return []


def extract_blogger_gepido():
    """Extracts from your third individual Blogger setup."""
    blog_id = os.getenv('GEPIDO_BLOG_ID')
    api_key = os.getenv('BLOGGER_API_KEY')
    if not blog_id or not api_key: return []
    
    try:
        url = f"https://www.googleapis.com/blogger/v3/blogs/{blog_id}/posts?key={api_key}"
        response = requests.get(url)
        response.raise_for_status()
        posts = response.json().get('items', [])
        
        elements = []
        for post in posts[:3]:
            elements.append({
                'title': post.get('title', 'Untitled'),
                'url': post.get('url', '#'),
                'source': 'Blogger - Site gepido',
                'description': post.get('content', '')[:150] + "..."
                
            })
        print(f"✅ SUCCESS: Extracted Blogger gepido ({blog_id[:6]}...)")
        return elements
    except Exception:
        print("❌ ERROR: Blogger gepido failed.")
        traceback.print_exc()
        return []


# 🤠 INDEPENDENT CONTROL PLAYGROUND
if __name__ == "__main__":
    print("--- RUNNING DECOUPLED PIPELINES ---")
    
    # 1. Fetch individual outputs into separate blocks
    treehouse_profile = get_treehouse_data()
    wp_posts = extract_wordpress_blog()
    
    b1_posts = extract_blogger_sahvsergio()
    b2_posts = extract_blogger_unana()
    b3_posts = extract_blogger_gepido() # If you want to drop this blog later, just comment out or delete this line!
    
    # 2. Control exactly what gets appended to the final pool on the fly
    all_blog_posts = wp_posts + b1_posts + b2_posts + b3_posts
    
    print("\n==================================================")
    print(f"📋 Total Aggregated Posts Loaded: {len(all_blog_posts)}")
    print("==================================================")
    for index, post in enumerate(all_blog_posts, 1):
        print(f"   [{index}] ({post['source']}) {post['title']} {post['description']}")