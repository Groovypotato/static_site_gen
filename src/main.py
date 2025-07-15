from textnode import markdown_to_html_node,extract_title
import shutil
import os
import sys

basepath = "/"
if sys.argv[1]:
    basepath = sys.argv[1]

def copy_files_from_dir(source_directory,destination_directory):
    files_copied = []
    directories_created = []
    if os.path.exists(destination_directory):
        print(f"rmtree:{destination_directory}")
        shutil.rmtree(destination_directory)
        print(f"mkdir:{destination_directory}")
        os.makedirs(destination_directory, exist_ok=True)
    else:
        print(f"Directory {destination_directory} not found")
        print(f"mkdir:{destination_directory}")
        os.makedirs(destination_directory)
    source_contents = os.listdir(source_directory)
    print(f"list of contents from {source_directory}:{source_contents}")
    for item in source_contents:
        if os.path.isfile(source_directory+"/"+item):
            print(f"{source_directory}/{item} is a file:{os.path.isfile(source_directory+"/"+item)}")
            print(f"Copying {source_directory}/{item} to {destination_directory}/")
            shutil.copy(source_directory+"/"+item,destination_directory+"/"+item)
            files_copied.append(source_directory+"/"+item)
        else:
            print(f"{source_directory}/{item} is a file:{os.path.isfile(source_directory+"/"+item)}")
            print(f"Recursivley searching through folder {source_directory}/{item}")
            copy_files_from_dir(source_directory+"/"+item,destination_directory+"/"+item)
            directories_created.append(destination_directory+"/"+item)


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}.")
    try:
        with open(from_path,"r") as markdown:
            markdown_file = markdown.read()
        with open(template_path,"r") as template:
            template_file = template.read()
    except FileNotFoundError:
        print(f"Error: {from_path} not found.")
    HTML_string = str(markdown_to_html_node(markdown_file).to_html())
    title = extract_title(markdown_file)
    replacements = template_file.replace("{{ Title }}",title).replace("{{ Content }}",HTML_string).replace('href="/',f'href="{basepath}').replace('src="/',f'src="{basepath}')
    if os.path.exists(dest_path):
        with open(f"{dest_path}/index.html", "w") as new_index:
            new_index.write(replacements)
    else:
        os.makedirs(dest_path)
        with open(f"{dest_path}/index.html", "w") as new_index:
            new_index.write(replacements)
        
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    print(f"Make list of contents of {dir_path_content}")
    content_list = os.listdir(dir_path_content)
    for item in content_list:
        print(f"Check if {item} is a file")
        if os.path.isfile(f"{dir_path_content}/{item}") and item[-3:] == ".md":
            print(f"{item} was a file")
            print(f"Check if filepath exists in {dest_dir_path}")
            if not os.path.exists(dest_dir_path):
                print(f"{dest_dir_path} didnt exist")
                print(f"Making path {dest_dir_path}")
                os.makedirs(dest_dir_path)
            print(f"generating page from {dir_path_content}/{item} with {template_path} in {dest_dir_path}")
            generate_page(f"{dir_path_content}/{item}",template_path,dest_dir_path)
        elif not os.path.isfile(f"{dir_path_content}/{item}"):
            print(f"{item} was not a file")
            print(f"checking if {dest_dir_path} extists")
            if not os.path.exists(f"{dest_dir_path}/item"):
                print(f"{dest_dir_path} did not exist")
                print(f"Creating {dest_dir_path}")
                os.makedirs(f"{dest_dir_path}/{item}")
            print(f"Checking in {dir_path_content}/{item} for another file or folder. With template {template_path} and in {dest_dir_path}/{item}")
            generate_pages_recursive(f"{dir_path_content}/{item}",template_path,f"{dest_dir_path}/{item}")

def main():
   copy_files_from_dir("./static","./docs")
   generate_pages_recursive("./content","./template.html","./docs")

if __name__ == "__main__":
    main()