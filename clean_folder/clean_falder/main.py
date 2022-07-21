import os
from pathlib import Path
import sys
import shutil
from zipfile import ZipFile
import gzip
import tarfile

known_extensions = {
    "JPEG": "images", "PNG": "images", "JPG": "images", "SVG": "images", "BMP": "images",
    "AVI": "video", "MP4": "video", "MOV": "video", "MKV": "video",
    "DOC": "documents", "DOCX": "documents", "TXT": "documents",
    "PDF": "documents", "XLSX": "documents", "PPTX": "documents",
    "MP3": "audio", "OGG": "audio", "WAV": "audio", "AMR": "audio",
    "ZIP": "archives", "GZ": "archives", "TAR": "archives"  # , "RAR": "archives"
}
extention_found = set()
unknown_extentions = set()
file_logs = {
    "images": [], "video": [], "documents": [], "audio": [], "archives": []
}

# begin create translator to cyrillic block
CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")
TRANS = {}
for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(c)] = l
    TRANS[ord(c.upper())] = l.upper()
# end create translator to cyrillic block


def translate(name):
    return name.translate(TRANS)


def unzip(file, root_path, name):  # unzips archive "name" with path "file" to folder "root_path/archives/name"
    count = 0
    unzip_to_path = root_path.joinpath("archives").joinpath(name)
    while unzip_to_path.exists():
        count += 1
        unzip_to_path = root_path.joinpath("archives").joinpath(name + "_" + str(count))
    if count > 0:
        file_logs["archives"].append(str(file)[1+len(str(root_path)):] + " (unzipped to) archives/" + name + f"_{count}")
    else:
        file_logs["archives"].append(
            str(file)[1 + len(str(root_path)):] + " (unzipped to) archives/" + name)
    try:
        archive = ZipFile(file, 'r')
        archive.extractall(unzip_to_path)
        archive.close()
        os.remove(file)
        return 0
    except:
        pass
    try:
        archive = tarfile.open(file, 'r')
        archive.extractall(unzip_to_path)
        archive.close()
        os.remove(file)
        return 0
    except:
        pass


# def ungz(file, root_path, name):
#     count = 1
#     unzip_to_path = root_path.joinpath("archives").joinpath(name)
#     while unzip_to_path.exists():
#         unzip_to_path = root_path.joinpath("archives").joinpath(name + "_" + str(count))
#         count += 1
#     os.mkdir(unzip_to_path)
#     try:
#         with gzip.open(file, "rb") as f_in:
#             with open(unzip_to_path.joinpath(name), "wb") as f_out:
#                 shutil.copyfileobj(f_in, f_out)
#         os.remove(file)
#     except:
#         os.rmdir(unzip_to_path)


def sort_files(dirname, root_path):  # rootdir is True is we are in root_path falder
    rootdir = dirname == root_path
    files_and_folders = os.listdir(dirname)
    folders = []
    files = []
    for file in files_and_folders:
        file_path = dirname.joinpath(file)
        try:
            os.rename(file_path, normalize(file_path))
            file_path = normalize(file_path)
        except PermissionError:
            print(f"Permission denied. '{file_path}' is currently in use")
            exit()
        if os.path.isdir(file_path):
            folders.append(normalize(file_path))
        if os.path.isfile(file_path):
            files.append(normalize(file_path))
    for folder in folders:
        current_folder = dirname.joinpath(folder)
        if os.path.basename(folder) not in set(known_extensions.values()) or not rootdir:
            sort_files(current_folder, root_path)
            try:
                os.rmdir(current_folder)
            except OSError:
                pass
    for file in files:
        path, name = os.path.split(file)
        name, ext = os.path.splitext(name)
        if ext[1:].upper() in known_extensions.keys():
            extention_found.add(ext[1:].upper())
            if known_extensions[ext[1:].upper()] == "archives":
                unzip(file, root_path, name)
            else:
                counter = 0
                while True:
                    try:
                        if counter == 0:
                            os.rename(file, root_path.joinpath(known_extensions[ext[1:].upper()]).
                                      joinpath(name + ext))
                            file_logs[known_extensions[ext[1:].upper()]].append(str(file)[1+len(str(root_path)):])
                        else:
                            os.rename(file, root_path.joinpath(known_extensions[ext[1:].upper()]).
                                      joinpath(name + f"_{counter}" + ext))
                            file_logs[known_extensions[ext[1:].upper()]].append(str(file)[1+len(str(root_path)):] +
                                                " (renamed to) "+name+f"_{counter}"+ext+" (due to the name repetition)")
                        break
                    except FileExistsError:
                        counter += 1
        else:
            unknown_extentions.add(ext[1:].upper())
    return 0


def normalize(path_to_file):
    newname = []
    path, file = os.path.split(path_to_file)
    file, ext = os.path.splitext(file)
    file = translate(file)
    for i in file:
        if i.isalpha() or i.isdigit() or i == ".":
            newname.append(i)
        else:
            newname.append("_")
    return Path(path).joinpath("".join(newname)+ext)


def main():
    try:  # check if folder exists
        root_folder_path = Path(sys.argv[1])
        root_folder_path = Path(os.path.abspath(root_folder_path))
    except IndexError:
        print("To sort 'myfolder' try: python main.py myfolder")
        sys.exit()
        # shutil.rmtree(r"\python_projects\GoIT\goit_task6\Trashfolder - Copy")
        # shutil.copytree(r"\python_projects\GoIT\goit_task6\Trashfolder",
        #                 r"\python_projects\GoIT\goit_task6\Trashfolder - Copy") # for test purposes
        # root_folder_path = Path(r"\python_projects\GoIT\goit_task6\Trashfolder - Copy")

    if not os.path.isdir(root_folder_path):
        print(f"'{root_folder_path}' is not a folder.")
        sys.exit()

    if not os.listdir(root_folder_path):  # check if folder not empty
        print("Folder is empty.")
        sys.exit()

    print(f"Sorting '{root_folder_path}'")

    for type_of_files in set(known_extensions.values()):  # create folders like "images" if they do not exist
        try:
            os.mkdir(root_folder_path.joinpath(type_of_files))
        except OSError:
            pass

    sort_files(root_folder_path, root_folder_path)
    with open(root_folder_path.joinpath("logs.txt"), "w") as logs:
        print(f"Extentions found: {', '.join(extention_found)}", file=logs)
        print(f"Unknown extensions: {', '.join(unknown_extentions)}", file=logs)
        print("Files sorted:", file=logs)
        for files in file_logs.keys():
            print(f"\t{files}: ", file=logs)
            for i in file_logs[files]:
                print("\t\t"+i, file=logs)

    print(f"See logs in '{root_folder_path.joinpath('logs.txt')}'")
    #print
    #print(os.listdir(folder_path))


if __name__ == "__main__":
    main()