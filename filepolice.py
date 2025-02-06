import os

def should_exclude(item, path):
    # List of files and directories to exclude
    exclude_list = [
        # Previous exclusions
        "filepolice.py",
        "folder_structure_and_content.txt",
        ".pyc",
        ".DS_Store",
        ".git",
        ".gitignore",
        ".idea",
        ".vscode",
        "__pycache__",
        "node_modules",
        "venv",
        "env",
        ".env",
        "build",
        "dist",
        "*.log",
        "*.tmp",
        "*.swp",
        ".pytest_cache",
        ".mypy_cache",
        ".tox",
        ".coverage",
        "*.egg-info",
        ".ipynb_checkpoints",
        # Front-end related exclusions
        "*.scss",
        "*.css",
        ".js",
        "db.sqlite3",
        "*.sass",
        "*.less",
        "*.vue",
        "*.json",
        "*.map",
        "*.woff",
        "*.woff2",
        "*.eot",
        "*.ttf",
        "*.otf",
        "*.svg",
        "*.png",
        "*.jpg",
        "*.jpeg",
        "*.gif",
        "*.ico",
        "*.webp",
        "*.min.js",
        "*.min.css",
        "package.json",
        "package-lock.json",
        "yarn.lock",
        "bower.json",
        "Gruntfile.js",
        "gulpfile.js",
        "webpack.config.js",
        "tsconfig.json",
        "babel.config.js",
        ".babelrc",
        ".eslintrc",
        ".stylelintrc",
        "bower_components",
        "gen-lang-client-0877968897-dbded6b0bfa2.json",
        "encoded-key.txt",
        "neo4j_kenya_ewakili.pem",
        "odk_central.pem",
        "readme.md",
        "UI.md",,
        "vendor",
        "assets",
        "public",
        "dist",
        "libs",
        "external",
        "third-party",
        "3rdparty",
        "project docs"
        "cdn",
        "migrations",
    ]
    
    # Check if the item matches any in the exclude list
    for exclude_item in exclude_list:
        if exclude_item.startswith("*"):
            if item.lower().endswith(exclude_item[1:]):
                return True
        elif item.lower() == exclude_item.lower():
            return True
    
    # Check if the path contains any of the static/vendor related directories
    static_vendor_dirs = ["docs" ,"static", "staticfiles","vendor", "assets", "public", "dist", "libs", "external", "third-party", "3rdparty", "cdn","data"]
    for dir_name in static_vendor_dirs:
        if dir_name.lower() in path.lower().split(os.sep):
            return True
    
    return False

def write_folder_structure(base_path, output_file, indent=""):
    for item in sorted(os.listdir(base_path)):
        full_path = os.path.join(base_path, item)
        relative_path = os.path.relpath(full_path, start=base_path)
        
        if should_exclude(item, full_path):
            continue
        
        if os.path.isdir(full_path):
            output_file.write(f"{indent}. {relative_path}/\n")
            write_folder_structure(full_path, output_file, indent + "  ")
        else:
            output_file.write(f"{indent}. {relative_path}\n")
            # Write file content
            output_file.write(f"{indent}  Content:\n")
            try:
                with open(full_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                # Add indentation to each line of the content
                indented_content = "\n".join(f"{indent}  {line}" for line in content.splitlines())
                output_file.write(indented_content + "\n")
            except Exception as e:
                output_file.write(f"{indent}  Unable to read file: {str(e)}\n")
            output_file.write("\n")  # Add a blank line after each file's content

def main():
    base_folder = os.getcwd()  # Use the current working directory
    output_file_name = "folder_structure_and_content.txt"
    
    with open(output_file_name, 'w', encoding='utf-8') as output_file:
        output_file.write(f"Folder structure and content for: {base_folder}\n\n")
        write_folder_structure(base_folder, output_file)
    
    print(f"Folder structure and content have been written to {output_file_name}")

if __name__ == "__main__":
    main()