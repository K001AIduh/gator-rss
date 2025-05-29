import os
from extract_title import extract_title
from markdown_to_html import markdown_to_html_node


def generate_page(from_path, template_path, dest_path, base_path="/"):
    """
    Generate an HTML page from a markdown file using a template.

    Args:
        from_path (str): Path to the markdown file
        template_path (str): Path to the HTML template
        dest_path (str): Path where the generated HTML will be saved
        base_path (str): Base path for all URLs (default: "/")
    """
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    # Read the markdown file
    with open(from_path, "r") as f:
        markdown_content = f.read()

    # Read the template file
    with open(template_path, "r") as f:
        template_content = f.read()

    # Convert markdown to HTML
    html_node = markdown_to_html_node(markdown_content)
    html_content = html_node.to_html()

    # Extract title from markdown
    title = extract_title(markdown_content)

    # Replace placeholders in template
    final_html = template_content.replace("{{ Title }}", title)
    final_html = final_html.replace("{{ Content }}", html_content)

    # Replace hrefs and srcs with the correct base path
    final_html = final_html.replace('href="/', f'href="{base_path}')
    final_html = final_html.replace('src="/', f'src="{base_path}')

    # Create destination directory if it doesn't exist
    os.makedirs(os.path.dirname(os.path.abspath(dest_path)), exist_ok=True)

    # Write the final HTML to the destination file
    with open(dest_path, "w") as f:
        f.write(final_html)
