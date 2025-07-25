#!/usr/bin/env python3
"""
Test script for QR AI handler function
"""

def test_handler():
    """Test the handler function with sample input"""
    try:
        from handler import handler
        print("✅ Handler imported successfully")
        
        # Test data
        test_job = {
            'input': {
                'prompt': 'a billboard in NYC with a qrcode',
                'guidance_scale': 15,
                'num_inference_steps': 50,  # Reduced for faster testing
                'seed': 42
            }
        }
        
        print("🧪 Testing handler function...")
        print(f"Input: {test_job}")
        
        # Call handler
        result = handler(test_job)
        
        # Check results
        print("\n📊 Results:")
        print(f"Success: {result.get('success', 'Unknown')}")
        print(f"Format: {result.get('format', 'Unknown')}")
        
        if result.get('success'):
            image_data = result.get('image', '')
            print(f"Image data length: {len(image_data)} characters")
            print("✅ Handler test PASSED!")
            
            # Optionally save image for inspection
            if image_data:
                import base64
                with open('test_output.png', 'wb') as f:
                    f.write(base64.b64decode(image_data))
                print("💾 Test image saved as test_output.png")
        else:
            error = result.get('error', 'Unknown error')
            print(f"❌ Handler returned error: {error}")
            
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure all dependencies are installed: pip install -r requirements.txt")
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        print(f"Error type: {type(e).__name__}")

def test_imports():
    """Test if all required imports work"""
    print("🔍 Testing imports...")
    
    imports_to_test = [
        ("runpod", "runpod"),
        ("torch", "torch"),
        ("PIL", "PIL (Pillow)"),
        ("diffusers", "diffusers"),
        ("base64", "base64"),
        ("io", "io")
    ]
    
    failed_imports = []
    
    for module, display_name in imports_to_test:
        try:
            __import__(module)
            print(f"✅ {display_name}")
        except ImportError as e:
            print(f"❌ {display_name}: {e}")
            failed_imports.append(display_name)
    
    if failed_imports:
        print(f"\n⚠️  Missing dependencies: {', '.join(failed_imports)}")
        print("Run: pip install -r requirements.txt")
        return False
    else:
        print("\n✅ All imports successful!")
        return True

if __name__ == "__main__":
    print("🚀 Starting QR AI Handler Tests\n")
    
    # Test imports first
    if test_imports():
        print("\n" + "="*50)
        # Test handler function
        test_handler()
    else:
        print("\n❌ Cannot proceed with handler test due to missing dependencies")
    
    print("\n🏁 Test complete!")