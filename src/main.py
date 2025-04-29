import os
import shutil
from markdown_block import markdown_to_html_node, extract_title

def copy_static(from_path, to_path):
    ls_path = os.listdir(from_path)
    for path in ls_path:
        full_path = os.path.join(from_path, path)
        if os.path.isfile(full_path):
            shutil.copy(full_path, to_path)
        else:
            dir_path = os.path.join(to_path, path)
            os.mkdir(dir_path)
            copy_static(full_path, dir_path)

def process_static(from_path, to_path):
    if os.path.exists(to_path):
        shutil.rmtree(to_path)
    os.makedirs(to_path, exist_ok=True)
    copy_static(from_path, to_path)

def main():
    process_static("static", "public")
    
    # Process the main index file
    generate_page("content/index.md", 'template.html', 'public/index.html')
    
    # Process all other markdown files
    extract_files()

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as file:
        markdown_content = file.read()
    with open(template_path) as file:
        template_content = file.read()
    
    # Convert markdown to HTML
    markdown_node = markdown_to_html_node(markdown_content)
    html_content = markdown_node.to_html()
    
    # Extract title from the markdown
    title = f"<h1>{extract_title(markdown_content)}</h1>"
    
    # Replace placeholders in the template
    template_content = template_content.replace("{{ Content }}", html_content)
    template_content = template_content.replace("{{ Title }}", title)
    
    # Write the final HTML to the destination
    with open(dest_path, "w") as file:
        file.write(template_content)
    
    print(f"Generated page at {dest_path}")

def get_files(directory, arr):
    for item in os.listdir(directory):
        full_path = os.path.join(directory, item)
        if os.path.isfile(full_path) and full_path.endswith('.md'):
            arr.append(full_path)
        elif os.path.isdir(full_path):
            get_files(full_path, arr)
    return arr

def extract_files():
    arr = []
    files = get_files("content", arr)
    print(files)
    
    # Process each file
    for file_path in files:
        # Determine the output path
        output_path = file_path.replace("content/", "public/").replace(".md", ".html")
        # Ensure directory exists
        output_dir = os.path.dirname(output_path)
        os.makedirs(output_dir, exist_ok=True)
        # Generate page
        generate_page(file_path, 'template.html', output_path)

main()