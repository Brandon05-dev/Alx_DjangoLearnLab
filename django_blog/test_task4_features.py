#!/usr/bin/env python3
"""
Test script to verify Task 4 features are implemented correctly.
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_blog.settings')
django.setup()

def test_tagwidget_in_forms():
    """Test if TagWidget is properly used in forms.py"""
    print("Testing TagWidget implementation...")
    
    try:
        from blog.forms import PostForm
        from taggit.forms import TagWidget
        
        # Create form instance
        form = PostForm()
        
        # Check if tags field exists and uses TagWidget
        if 'tags' in form.fields:
            widget = form.fields['tags'].widget
            if isinstance(widget, TagWidget):
                print("✅ TagWidget() is properly used in PostForm")
                return True
            else:
                print(f"❌ Tags field uses {type(widget)} instead of TagWidget")
                return False
        else:
            print("❌ Tags field not found in PostForm")
            return False
            
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_search_functionality():
    """Test if search functionality is implemented"""
    print("\nTesting search functionality...")
    
    try:
        from blog.views import search_posts
        from django.test import RequestFactory
        from django.contrib.auth.models import User
        
        # Create a request factory
        factory = RequestFactory()
        request = factory.get('/search/', {'q': 'test'})
        
        # Test search view
        response = search_posts(request)
        
        if hasattr(response, 'status_code') and response.status_code == 200:
            print("✅ Search functionality is working")
            return True
        else:
            print("❌ Search functionality has issues")
            return False
            
    except Exception as e:
        print(f"❌ Error testing search functionality: {e}")
        return False

def test_url_configuration():
    """Test if URL configuration is complete"""
    print("\nTesting URL configuration...")
    
    try:
        from django.urls import reverse
        from django.test import RequestFactory
        
        # Test if search URL is configured
        search_url = reverse('search-posts')
        print(f"✅ Search URL configured: {search_url}")
        
        # Test if posts-by-tag URL is configured
        tag_url = reverse('posts-by-tag', kwargs={'tag_name': 'test'})
        print(f"✅ Posts by tag URL configured: {tag_url}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing URL configuration: {e}")
        return False

def main():
    """Run all tests"""
    print("=== Testing Task 4 Features ===\n")
    
    results = []
    results.append(test_tagwidget_in_forms())
    results.append(test_search_functionality())
    results.append(test_url_configuration())
    
    print(f"\n=== Results ===")
    passed = sum(results)
    total = len(results)
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All Task 4 features are implemented correctly!")
    else:
        print("⚠️ Some features need attention.")

if __name__ == '__main__':
    main()