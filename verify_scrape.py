#!/usr/bin/env python3
"""
Verify that the website scrape was complete
"""

import os
from pathlib import Path

def check_file_exists(path):
    """Check if a file or directory exists"""
    return Path(path).exists()

def main():
    base_dir = Path("www.offmenu.design")
    
    if not base_dir.exists():
        print("ERROR: www.offmenu.design directory not found!")
        return False
    
    print("Verifying website scrape...")
    print("=" * 50)
    
    # Check key files and directories
    checks = [
        ("index.html", base_dir / "index.html"),
        ("approach.html", base_dir / "approach.html"),
        ("blog.html", base_dir / "blog.html"),
        ("pricing.html", base_dir / "pricing.html"),
        ("services.html", base_dir / "services.html"),
        ("terms.html", base_dir / "terms.html"),
        ("_next directory", base_dir / "_next"),
        ("_next/static/chunks (JS/CSS)", base_dir / "_static" / "chunks"),  # Wrong path, will fix
        ("images directory", base_dir / "images"),
        ("fonts directory", base_dir / "fonts"),
        ("logos directory", base_dir / "logos"),
        ("blog directory", base_dir / "blog"),
        ("work directory", base_dir / "work"),
        ("robots.txt", base_dir / "robots.txt"),
        ("manifest.webmanifest", base_dir / "manifest.webmanifest"),
    ]
    
    # Fix the incorrect path
    checks[5] = ("_next/static/chunks (JS/CSS)", base_dir / "_next" / "static" / "chunks")
    
    all_good = True
    for name, path in checks:
        if check_file_exists(path):
            print(f"✓ {name}: FOUND")
        else:
            print(f"✗ {name}: MISSING")
            all_good = False
    
    # Check some specific files
    print("\nChecking specific assets:")
    specific_files = [
        ("CSS file", "_next/static/chunks/3db27d7fc86f31bd.css?dpl=dpl_CMaNBewzF47fxz1p3XvUzPJCUq82.css"),
        ("JS file", "_next/static/chunks/89260d75f0f9a8b4.js?dpl=dpl_CMaNBewzF47fxz1p3XvUzPJCUq82"),
        ("Font file", "fonts/Neue Montreal/PPNeueMontreal-Variable.woff2"),
        ("Work image", "images/work/super/block-1773917682983.jpg"),
        ("Blog image", "images/blog/design-an-agent-harness/thumbnail.png"),
    ]
    
    for name, rel_path in specific_files:
        file_path = base_dir / rel_path
        if check_file_exists(file_path):
            print(f"✓ {name}: FOUND")
        else:
            print(f"✗ {name}: MISSING")
            all_good = False
    
    print("\n" + "=" * 50)
    if all_good:
        print("✓ All checks passed! The website scrape appears complete.")
    else:
        print("✗ Some checks failed. The scrape may be incomplete.")
    
    # Show total size and file count
    total_size = sum(f.stat().st_size for f in base_dir.rglob('*') if f.is_file())
    file_count = len(list(base_dir.rglob('*')))
    
    print(f"\nStatistics:")
    print(f"- Total files: {file_count}")
    print(f"- Total size: {total_size / (1024*1024):.1f} MB")
    
    return all_good

if __name__ == "__main__":
    main()
