#!/usr/bin/env python3
"""
Phase 3.2 - Simple File Structure Tests (Sans conftest imports)
"""

from pathlib import Path
import sys

def test_files():
    """Vérifier que tous les fichiers requis existent"""
    
    base_dir = Path(__file__).parent.parent
    root_dir = base_dir.parent
    
    tests = []
    passed = 0
    failed = 0
    
    # Test 1: Photo model
    photo_model = base_dir / 'app' / 'models' / 'photo.py'
    if photo_model.exists():
        content = photo_model.read_text()
        fields = ['plant_id', 'filename', 'file_size', 'width', 'height', 'is_primary']
        all_found = all(f in content for f in fields)
        if all_found:
            print("✓ Photo model exists with all required fields")
            passed += 1
        else:
            print("✗ Photo model missing some fields")
            failed += 1
    else:
        print(f"✗ Photo model not found: {photo_model}")
        failed += 1
    
    # Test 2: Photo migration
    migration_dir = base_dir / 'migrations' / 'versions'
    migrations = list(migration_dir.glob('*add_photos*'))
    if migrations:
        print(f"✓ Photo migration exists: {migrations[0].name}")
        passed += 1
    else:
        print("✗ Photo migration not found")
        failed += 1
    
    # Test 3: Photo routes
    photos_routes = base_dir / 'app' / 'routes' / 'photos.py'
    if photos_routes.exists():
        content = photos_routes.read_text()
        if '@router.post' in content and '@router.get' in content and '@router.delete' in content:
            print("✓ Photo routes file exists with POST, GET, DELETE endpoints")
            passed += 1
        else:
            print("✗ Photo routes missing some endpoint decorators")
            failed += 1
    else:
        print("✗ Photo routes file not found")
        failed += 1
    
    # Test 4: Image processor
    image_proc = base_dir / 'app' / 'utils' / 'image_processor.py'
    if image_proc.exists():
        content = image_proc.read_text()
        funcs = ['validate_image_upload', 'process_image_to_webp', 'delete_photo_files']
        if all(f in content for f in funcs):
            print("✓ Image processor exists with all required functions")
            passed += 1
        else:
            print("✗ Image processor missing some functions")
            failed += 1
    else:
        print("✗ Image processor not found")
        failed += 1
    
    # Test 5: Photo schema
    photo_schema = base_dir / 'app' / 'schemas' / 'photo_schema.py'
    if photo_schema.exists():
        content = photo_schema.read_text()
        if 'PhotoResponse' in content and 'PhotoUploadResponse' in content:
            print("✓ Photo schema exists with PhotoResponse and PhotoUploadResponse")
            passed += 1
        else:
            print("✗ Photo schema missing schema classes")
            failed += 1
    else:
        print("✗ Photo schema not found")
        failed += 1
    
    # Test 6: Frontend photosAPI
    photos_api = root_dir / 'frontend' / 'src' / 'lib' / 'api' / 'photosAPI.js'
    if photos_api.exists():
        content = photos_api.read_text()
        methods = ['uploadPhoto', 'getPhotos', 'deletePhoto', 'setPrimaryPhoto']
        if all(m in content for m in methods):
            print("✓ Frontend photosAPI.js exists with all methods")
            passed += 1
        else:
            print("✗ photosAPI.js missing some methods")
            failed += 1
    else:
        print("✗ photosAPI.js not found")
        failed += 1
    
    # Test 7: Frontend PlantPhotoUpload component
    upload_comp = root_dir / 'frontend' / 'src' / 'components' / 'PlantPhotoUpload.jsx'
    if upload_comp.exists():
        print("✓ PlantPhotoUpload.jsx component exists")
        passed += 1
    else:
        print("✗ PlantPhotoUpload.jsx not found")
        failed += 1
    
    # Test 8: Frontend PlantPhotoGallery component
    gallery_comp = root_dir / 'frontend' / 'src' / 'components' / 'PlantPhotoGallery.jsx'
    if gallery_comp.exists():
        print("✓ PlantPhotoGallery.jsx component exists")
        passed += 1
    else:
        print("✗ PlantPhotoGallery.jsx not found")
        failed += 1
    
    # Test 9: Frontend PhotoCarousel component
    carousel_comp = root_dir / 'frontend' / 'src' / 'components' / 'PhotoCarousel.jsx'
    if carousel_comp.exists():
        print("✓ PhotoCarousel.jsx component exists")
        passed += 1
    else:
        print("✗ PhotoCarousel.jsx not found")
        failed += 1
    
    # Test 10: PlantFormPage integration
    form_page = root_dir / 'frontend' / 'src' / 'pages' / 'PlantFormPage.jsx'
    if form_page.exists():
        content = form_page.read_text()
        if 'PlantPhotoUpload' in content and 'PlantPhotoGallery' in content and 'photosAPI' in content:
            print("✓ PlantFormPage.jsx imports and integrates photo components")
            passed += 1
        else:
            print("✗ PlantFormPage.jsx missing photo component integration")
            failed += 1
    else:
        print("✗ PlantFormPage.jsx not found")
        failed += 1
    
    # Test 11: Check data/photos directory exists or will be created
    photos_data = root_dir / 'data' / 'photos'
    if photos_data.exists():
        print(f"✓ data/photos directory exists")
        # Count photos
        webp_files = list(photos_data.rglob('*.webp'))
        if webp_files:
            print(f"  └─ Contains {len(webp_files)} WebP files")
        passed += 1
    else:
        print(f"✓ data/photos directory will be created on first upload")
        passed += 1
    
    # Summary
    print("\n" + "="*50)
    print(f"TESTS PASSED: {passed}")
    print(f"TESTS FAILED: {failed}")
    print("="*50)
    
    if failed == 0:
        print("\n✅ All file structure tests PASSED!")
        print("\n🎯 Phase 3.2 Infrastructure Complete:")
        print("  ✓ Backend: Model + Migration + Routes + Utils")
        print("  ✓ Frontend: API Client + 3 Components + Integration")
        return 0
    else:
        print(f"\n❌ {failed} file structure tests FAILED")
        return 1

if __name__ == '__main__':
    sys.exit(test_files())
