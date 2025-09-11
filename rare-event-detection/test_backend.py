#!/usr/bin/env python3
"""
Test script for the Rare Event Detection backend API
Run this script to test all endpoints with sample data
"""

import requests
import json
import base64
from PIL import Image
import io
import os

# Configuration
API_BASE_URL = "http://localhost:8000"

def create_test_image(color, size=(224, 224), text=""):
    """Create a simple test image with specified color"""
    img = Image.new('RGB', size, color=color)
    
    # Add some text if provided
    if text:
        try:
            from PIL import ImageDraw, ImageFont
            draw = ImageDraw.Draw(img)
            # Try to use default font
            try:
                font = ImageFont.load_default()
            except:
                font = None
            
            # Calculate text position (center)
            if font:
                bbox = draw.textbbox((0, 0), text, font=font)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]
            else:
                text_width, text_height = len(text) * 6, 11  # Rough estimate
            
            x = (size[0] - text_width) // 2
            y = (size[1] - text_height) // 2
            
            draw.text((x, y), text, fill='white', font=font)
        except ImportError:
            pass  # Skip text if PIL doesn't support it
    
    return img

def save_test_image(img, filename):
    """Save test image to file"""
    img.save(filename)
    return filename

def test_health_check():
    """Test the health check endpoint"""
    print("🔍 Testing health check...")
    try:
        response = requests.get(f"{API_BASE_URL}/health")
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Health check passed!")
            print(f"   Device: {result.get('device', 'unknown')}")
            print(f"   Models loaded: {result.get('models_loaded', {})}")
            print(f"   Reference count: {result.get('reference_count', 0)}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def test_upload_references():
    """Test uploading reference images"""
    print("\n📚 Testing reference image upload...")
    
    # Create test reference images
    test_images = [
        (create_test_image('red', text="Fire"), "fire.jpg", "A dangerous fire spreading"),
        (create_test_image('blue', text="Flood"), "flood.jpg", "Severe flooding in the area"),
        (create_test_image('gray', text="Storm"), "storm.jpg", "Powerful storm with lightning"),
        (create_test_image('orange', text="Volcano"), "volcano.jpg", "Volcanic eruption with lava")
    ]
    
    files = []
    captions = []
    temp_files = []
    
    try:
        # Save test images and prepare for upload
        for img, filename, caption in test_images:
            filepath = f"/tmp/{filename}"
            save_test_image(img, filepath)
            temp_files.append(filepath)
            
            files.append(('files', (filename, open(filepath, 'rb'), 'image/jpeg')))
            captions.append(('captions', caption))
        
        # Upload references
        response = requests.post(
            f"{API_BASE_URL}/upload_references",
            files=files + captions
        )
        
        # Close file handles
        for _, (_, file_handle, _) in files:
            file_handle.close()
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Reference upload successful!")
            print(f"   Status: {result.get('status')}")
            print(f"   Count: {result.get('count')}")
            print(f"   Message: {result.get('message')}")
            return True
        else:
            print(f"❌ Reference upload failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Reference upload error: {e}")
        return False
    finally:
        # Clean up temporary files
        for filepath in temp_files:
            try:
                os.remove(filepath)
            except:
                pass

def test_classify_image():
    """Test image classification"""
    print("\n🔍 Testing image classification...")
    
    # Create a test image for classification
    test_img = create_test_image('purple', text="Rare Event")
    test_file = "/tmp/test_classify.jpg"
    
    try:
        save_test_image(test_img, test_file)
        
        with open(test_file, 'rb') as f:
            files = {'file': ('test.jpg', f, 'image/jpeg')}
            response = requests.post(f"{API_BASE_URL}/classify", files=files)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Classification successful!")
            print(f"   Label: {result.get('label')}")
            print(f"   Similarity: {result.get('similarity', 0):.4f}")
            print(f"   All similarities: {result.get('all_similarities', [])}")
            return True
        else:
            print(f"❌ Classification failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Classification error: {e}")
        return False
    finally:
        try:
            os.remove(test_file)
        except:
            pass

def test_describe_image():
    """Test image description"""
    print("\n📝 Testing image description...")
    
    # Create a test image for description
    test_img = create_test_image('green', text="Nature")
    test_file = "/tmp/test_describe.jpg"
    
    try:
        save_test_image(test_img, test_file)
        
        with open(test_file, 'rb') as f:
            files = {'file': ('test.jpg', f, 'image/jpeg')}
            response = requests.post(f"{API_BASE_URL}/describe", files=files)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Description successful!")
            print(f"   Description: {result.get('description')}")
            return True
        else:
            print(f"❌ Description failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Description error: {e}")
        return False
    finally:
        try:
            os.remove(test_file)
        except:
            pass

def test_generate_image():
    """Test synthetic image generation"""
    print("\n🎨 Testing image generation...")
    
    caption = "A rare purple lightning storm over mountains"
    
    try:
        data = {'caption': caption}
        response = requests.post(f"{API_BASE_URL}/generate", data=data)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Generation successful!")
            print(f"   Caption: {result.get('caption')}")
            
            # Check if image data is present
            image_data = result.get('image', '')
            if image_data.startswith('data:image/'):
                print(f"   Image generated: {len(image_data)} characters")
                
                # Optionally save the generated image
                try:
                    # Extract base64 data
                    base64_data = image_data.split(',')[1]
                    image_bytes = base64.b64decode(base64_data)
                    
                    with open('/tmp/generated_test.png', 'wb') as f:
                        f.write(image_bytes)
                    print(f"   Saved generated image to: /tmp/generated_test.png")
                except Exception as e:
                    print(f"   Could not save image: {e}")
            else:
                print(f"   Warning: No valid image data received")
            
            return True
        else:
            print(f"❌ Generation failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Generation error: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Starting Rare Event Detection API Tests")
    print("=" * 50)
    
    # Test results
    results = {}
    
    # Run tests in order
    results['health'] = test_health_check()
    
    if results['health']:
        results['upload'] = test_upload_references()
        
        if results['upload']:
            results['classify'] = test_classify_image()
            results['describe'] = test_describe_image()
        else:
            print("\n⚠️ Skipping classification and description tests (no references uploaded)")
            results['classify'] = False
            results['describe'] = False
        
        results['generate'] = test_generate_image()
    else:
        print("\n❌ Backend not available. Skipping all tests.")
        results.update({
            'upload': False,
            'classify': False,
            'describe': False,
            'generate': False
        })
    
    # Print summary
    print("\n" + "=" * 50)
    print("📊 Test Summary:")
    print("-" * 20)
    
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{test_name.capitalize():12} {status}")
    
    total_tests = len(results)
    passed_tests = sum(results.values())
    
    print(f"\nTotal: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests == total_tests:
        print("🎉 All tests passed! Your backend is working correctly.")
    else:
        print("⚠️ Some tests failed. Check the backend server and try again.")
    
    return passed_tests == total_tests

if __name__ == "__main__":
    main()