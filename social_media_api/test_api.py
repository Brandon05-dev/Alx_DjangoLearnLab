#!/usr/bin/env python3
"""
Test script for Social Media API functionality
Run this script to test the basic API endpoints
"""
import requests
import json

BASE_URL = 'http://127.0.0.1:8000/api'
headers = {'Content-Type': 'application/json'}

def test_user_registration():
    """Test user registration"""
    print("🔐 Testing user registration...")
    data = {
        "username": "testuser1",
        "email": "test1@example.com",
        "password": "testpass123",
        "password_confirm": "testpass123",
        "first_name": "Test",
        "last_name": "User1"
    }
    
    response = requests.post(f'{BASE_URL}/accounts/register/', 
                           headers=headers, json=data)
    
    if response.status_code == 201:
        print("✅ User registration successful!")
        return response.json()['token']
    else:
        print(f"❌ Registration failed: {response.text}")
        return None

def test_user_login():
    """Test user login"""
    print("\n🔑 Testing user login...")
    data = {
        "username": "testuser1",
        "password": "testpass123"
    }
    
    response = requests.post(f'{BASE_URL}/accounts/login/', 
                           headers=headers, json=data)
    
    if response.status_code == 200:
        print("✅ User login successful!")
        return response.json()['token']
    else:
        print(f"❌ Login failed: {response.text}")
        return None

def test_create_post(token):
    """Test post creation"""
    print("\n📝 Testing post creation...")
    auth_headers = {**headers, 'Authorization': f'Token {token}'}
    data = {
        "content": "Hello from the Social Media API! This is my first post. 🚀"
    }
    
    response = requests.post(f'{BASE_URL}/posts/', 
                           headers=auth_headers, json=data)
    
    if response.status_code == 201:
        print("✅ Post creation successful!")
        return response.json()['id']
    else:
        print(f"❌ Post creation failed: {response.text}")
        return None

def test_list_posts(token):
    """Test listing posts"""
    print("\n📋 Testing post listing...")
    auth_headers = {**headers, 'Authorization': f'Token {token}'}
    
    response = requests.get(f'{BASE_URL}/posts/', headers=auth_headers)
    
    if response.status_code == 200:
        posts = response.json()
        print(f"✅ Found {len(posts)} posts!")
        return posts
    else:
        print(f"❌ Post listing failed: {response.text}")
        return []

def test_like_post(token, post_id):
    """Test liking a post"""
    print(f"\n❤️ Testing post like (Post ID: {post_id})...")
    auth_headers = {**headers, 'Authorization': f'Token {token}'}
    
    response = requests.post(f'{BASE_URL}/posts/{post_id}/like/', 
                           headers=auth_headers)
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Post like successful! Liked: {result['liked']}")
        return True
    else:
        print(f"❌ Post like failed: {response.text}")
        return False

def test_create_comment(token, post_id):
    """Test creating a comment"""
    print(f"\n💬 Testing comment creation (Post ID: {post_id})...")
    auth_headers = {**headers, 'Authorization': f'Token {token}'}
    data = {
        "text": "Great post! Thanks for sharing. 👍"
    }
    
    response = requests.post(f'{BASE_URL}/posts/{post_id}/comments/', 
                           headers=auth_headers, json=data)
    
    if response.status_code == 201:
        print("✅ Comment creation successful!")
        return response.json()['id']
    else:
        print(f"❌ Comment creation failed: {response.text}")
        return None

def test_get_profile(token):
    """Test getting user profile"""
    print("\n👤 Testing profile retrieval...")
    auth_headers = {**headers, 'Authorization': f'Token {token}'}
    
    response = requests.get(f'{BASE_URL}/accounts/profile/', 
                          headers=auth_headers)
    
    if response.status_code == 200:
        profile = response.json()
        print(f"✅ Profile retrieved! Username: {profile['username']}")
        return profile
    else:
        print(f"❌ Profile retrieval failed: {response.text}")
        return None

def test_get_notifications(token):
    """Test getting notifications"""
    print("\n🔔 Testing notifications...")
    auth_headers = {**headers, 'Authorization': f'Token {token}'}
    
    response = requests.get(f'{BASE_URL}/notifications/', 
                          headers=auth_headers)
    
    if response.status_code == 200:
        notifications = response.json()
        print(f"✅ Found {len(notifications)} notifications!")
        return notifications
    else:
        print(f"❌ Notifications retrieval failed: {response.text}")
        return []

def main():
    """Run all tests"""
    print("🚀 Starting Social Media API Tests...\n")
    
    # Test registration
    token = test_user_registration()
    if not token:
        # Try login if registration fails (user might already exist)
        token = test_user_login()
    
    if not token:
        print("\n❌ Cannot proceed without authentication token")
        return
    
    print(f"\n🔑 Using token: {token[:20]}...")
    
    # Test profile
    test_get_profile(token)
    
    # Test post creation
    post_id = test_create_post(token)
    
    # Test post listing
    test_list_posts(token)
    
    if post_id:
        # Test liking
        test_like_post(token, post_id)
        
        # Test commenting
        test_create_comment(token, post_id)
        
        # Test notifications (should have some from likes/comments)
        test_get_notifications(token)
    
    print("\n🎉 API testing completed!")
    print("\n📖 Check the README.md for more detailed API documentation.")

if __name__ == "__main__":
    try:
        main()
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Make sure the Django server is running on http://127.0.0.1:8000/")
        print("Run: python manage.py runserver")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")