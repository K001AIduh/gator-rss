import os
import shutil
import sys
from pathlib import Path
from markdown_to_html import markdown_to_html_node
from generate_page import generate_page


def copy_static(source_dir, dest_dir):
    """
    Recursively copy the contents of source_dir to dest_dir.
    If dest_dir exists, it will be deleted first to ensure a clean copy.

    Args:
        source_dir (str): Path to the source directory
        dest_dir (str): Path to the destination directory
    """
    # Ensure paths are absolute
    source_dir = os.path.abspath(source_dir)
    dest_dir = os.path.abspath(dest_dir)

    # Delete destination directory if it exists
    if os.path.exists(dest_dir):
        print(f"Removing existing directory: {dest_dir}")
        shutil.rmtree(dest_dir)

    # Create destination directory
    print(f"Creating directory: {dest_dir}")
    os.makedirs(dest_dir)

    # Copy files and directories recursively
    for item in os.listdir(source_dir):
        source_item = os.path.join(source_dir, item)
        dest_item = os.path.join(dest_dir, item)

        if os.path.isdir(source_item):
            # If it's a directory, recursively copy it
            print(f"Copying directory: {source_item} -> {dest_item}")
            copy_static(source_item, dest_item)
        else:
            # If it's a file, copy it
            print(f"Copying file: {source_item} -> {dest_item}")
            shutil.copy2(source_item, dest_item)


def generate_pages_recursive(
    dir_path_content, template_path, dest_dir_path, base_path="/"
):
    """
    Recursively generate HTML pages from markdown files in the content directory.

    Args:
        dir_path_content (str): Path to the content directory containing markdown files
        template_path (str): Path to the HTML template file
        dest_dir_path (str): Path to the destination directory for generated HTML files
        base_path (str): Base path for all URLs (default: "/")
    """
    # Convert paths to absolute paths
    dir_path_content = os.path.abspath(dir_path_content)
    template_path = os.path.abspath(template_path)
    dest_dir_path = os.path.abspath(dest_dir_path)

    # Ensure the destination directory exists
    os.makedirs(dest_dir_path, exist_ok=True)

    # Walk through all files and directories in the content directory
    for root, dirs, files in os.walk(dir_path_content):
        # Calculate the relative path from the content directory
        rel_path = os.path.relpath(root, dir_path_content)

        # Create the corresponding directory in the destination
        if rel_path != ".":
            dest_subdir = os.path.join(dest_dir_path, rel_path)
            os.makedirs(dest_subdir, exist_ok=True)

        # Process each markdown file
        for file in files:
            if file.endswith(".md"):
                # Get the full path to the markdown file
                md_file_path = os.path.join(root, file)

                # Determine the destination HTML file path
                if file == "index.md":
                    # For index.md files, keep the same directory structure
                    if rel_path == ".":
                        html_file_path = os.path.join(dest_dir_path, "index.html")
                    else:
                        html_file_path = os.path.join(
                            dest_dir_path, rel_path, "index.html"
                        )
                else:
                    # For other markdown files, create a subdirectory with the file name
                    file_name = os.path.splitext(file)[0]
                    if rel_path == ".":
                        html_file_path = os.path.join(
                            dest_dir_path, file_name, "index.html"
                        )
                    else:
                        html_file_path = os.path.join(
                            dest_dir_path, rel_path, file_name, "index.html"
                        )

                # Ensure the destination directory exists
                os.makedirs(os.path.dirname(html_file_path), exist_ok=True)

                # Generate the HTML page with the specified base path
                generate_page(md_file_path, template_path, html_file_path, base_path)


def main():
    # Get the base path from command line arguments or default to "/"
    base_path = sys.argv[1] if len(sys.argv) > 1 else "/"

    # Ensure base_path ends with a slash
    if not base_path.endswith("/"):
        base_path += "/"

    # Set up paths
    current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    static_dir = os.path.join(current_dir, "static")
    docs_dir = os.path.join(current_dir, "docs")  # Changed from "public" to "docs"
    content_dir = os.path.join(current_dir, "content")
    template_path = os.path.join(current_dir, "template.html")

    # Copy static files
    print("Copying static files...")
    copy_static(static_dir, docs_dir)

    # Generate all pages recursively with the specified base path
    generate_pages_recursive(content_dir, template_path, docs_dir, base_path)

    print("Static site generation complete!")
    print(f"Site built with base path: {base_path}")


if __name__ == "__main__":
    main()
