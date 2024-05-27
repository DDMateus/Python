import sys  # Access command-line arguments
import os  # Provide OS functionality
import zlib  # Git compresses everything using zlib
import hashlib  # Git SHA hash

class GitRepository:
    """
    Git repository
    """
    def __init__(self, work_tree: str):
        self.work_tree = work_tree
        self.git_dir = os.path.join(self.work_tree, ".git")
        self.objects_dir = os.path.join(self.git_dir, "objects")
        self.refs_dir = os.path.join(self.git_dir, "refs")
    
    def git_init(self):
        """
        Initialize a new git repository
        """
        try:
            if not os.path.exists(self.git_dir):
                os.mkdir(self.git_dir)
                os.mkdir(self.objects_dir)
                os.mkdir(self.refs_dir)
                
                # Contains the a reference pointing to the check-out commit
                with open(os.path.join(self.git_dir, "HEAD"), "w") as file:
                    file.write("ref: refs/heads/main\n")
                print(f"Initialized empty Git repository in {self.git_dir}")
            else:
                print("Git repository already initialized")
        except OSError as e:
            print(f"Error: {e}")
            
class BlobObject:
    """
    Represents a blob object
    """
    def __init__(self, object_dir: str, sha1: str):
        self.sha1 = sha1
        self.object_dir = object_dir
    
    def read_blob(self):
        """
        Read the content of the blob object
        """
        blob_path = os.path.join(self.object_dir, self.sha1[:2], self.sha1[2:])
        try:
            with open(blob_path, "rb") as file:
                content = b""
                while True:
                    # Read file in chunks to avoid loading the entire content into memory 
                    chunk = file.read(4096)
                    # No more data to read
                    if not chunk:
                        break
                    content += chunk
                header, content = (zlib.decompress(content).decode()).split("\0", maxsplit=1)
                return content
        except (FileNotFoundError, zlib.error, OSError) as e:
            print(f"Error: {e}")
            return None

class HashObject:
    """
    Creates a blob object and optionally write it to .git/objects
    """
    def __init__(self, object_dir: str, content: str, write_to_obj=False):
        self.content = content
        self.object_dir = object_dir
        self.write_to_obj = write_to_obj
        
    def hash_object(self):
        try:
            with open(self.content, "rb") as f:
                file_content = b""
                while True:
                    chunk = f.read(4096)
                    if not chunk:
                        break
                    file_content += chunk
            
            # Format blob object header
            header = f"blob {(len(file_content))}\0".encode()
            # Concatenate header + contente
            blob_object = header + file_content
            
            # Compute SHA-1 hash
            object_hash = hashlib.sha1(blob_object).hexdigest()
            
            if self.write_to_obj:
                # Compress with zlib
                compressed_content = zlib.compress(blob_object)
                # Path to the object inside .git/objects
                file_path = os.path.join(self.object_dir, object_hash[:2], object_hash[2:])
                # Check if directory exists to avoid error creating file inside non-existing directory
                os.makedirs(os.path.join(self.object_dir, object_hash[:2]), exist_ok=True)
                with open(file_path, "wb") as f:
                    f.write(compressed_content)
            return object_hash
        except (FileNotFoundError, OSError, zlib.error) as e:
            print(f"Error: {e}")
            return None

class TreeObject:
    """
    Represent a tree like object
    """
    def __init__(self, object_dir: str, sha1: str, options=False):
        self.object_dir = object_dir
        self.sha1 = sha1
        self.options = options
        
    def ls_tree(self):
        tree_path = os.path.join(self.object_dir, self.sha1[:2], self.sha1[2:])
        try:
            with open(tree_path, "rb") as f:
                content = b""
                while True:
                    chunk = f.read(4096)
                    if not chunk:
                        break
                    content += chunk
            header, entries = (zlib.decompress(content).decode("ISO-8859-1")).split("\0", maxsplit=1)
            while entries:
                mode_name, entries = entries.split("\0", maxsplit=1)
                hash, entries = entries[:20], entries[20:]
                mode, name = mode_name.split(" ")
                if self.options:
                    print(name) 
                else:
                    print(mode)
                    print(name)
                    print(hash)
        except (FileNotFoundError, OSError, zlib.error) as e:
            print(f"Error: {e}")

class WriteTree():
    """
    Recursively creates tree and blob objects for the directory structure.
    """
    def __init__(self, object_dir: str):
        self.object_dir = object_dir
                
    def write_tree(self, path: str): 
        """
        Create tree object and write it to .git/objects
        """
        try:
            tree_entries = {}
            for entry in os.listdir(path):
                # Skip entries starting with "."
                if entry.startswith("."):
                    continue
                full_path = os.path.join(path, entry)
                if os.path.isdir(full_path):
                    # Recursively create tree object for subdirectory
                    sha1_hash = self.write_tree(full_path)
                    name = entry
                    mode = "40000"
                # Create blob object for file
                elif os.path.isfile(full_path):
                    sha1_hash = self.write_blob(full_path)
                    mode = "100644"
                    name = entry
                    
                tree_entries[name] = f"{mode} {name}".encode() + b"\0" + bytes.fromhex(sha1_hash)
                
            content = b"".join(tree_entries[key] for key in sorted(tree_entries.keys()))
            
            size = len(content)
            header_tree = f"tree {size}".encode()
            tree_content = header_tree + b"\0" + content
            
            tree_sha1 = hashlib.sha1(tree_content).hexdigest()
            compressed = zlib.compress(tree_content)
            
            folder, file = tree_sha1[:2], tree_sha1[2:]
            
            os.makedirs(os.path.join(self.object_dir, folder), exist_ok=True)
            with open(os.path.join(self.object_dir, folder, file), "wb") as f:
                f.write(compressed)
                
            return tree_sha1
        except (FileNotFoundError, OSError, zlib.error) as e:
            print(f"Error: {e}")
            return None
        
    def write_blob(self, file: str): 
        """
        Create blob object and write it to .git/objects
        """
        try:
            with open(file, "rb") as f:
                file_content = b""
                while True:
                    chunk = f.read(4096)
                    if not chunk:
                        break
                    file_content += chunk
            
            # Format blob object header
            header = f"blob {(len(file_content))}\0".encode()
            # Concatenate header + contente
            blob_object = header + file_content
            
            # Compute SHA-1 hash
            object_hash = hashlib.sha1(blob_object).hexdigest()
            # Compress with zlib
            compressed_content = zlib.compress(blob_object)
            # Path to the object inside .git/objects
            file_path = os.path.join(self.object_dir, object_hash[:2], object_hash[2:])
            # Check if directory exists to avoid error creating file inside non-existing directory
            os.makedirs(os.path.join(self.object_dir, object_hash[:2]), exist_ok=True)
            with open(file_path, "wb") as f:
                f.write(compressed_content)
            return object_hash
        except (FileNotFoundError, OSError, zlib.error) as e:
            print(f"Error: {e}")
            return None
        
class CommitObject:
    """
    Create a commit object and write it in the ".git/objects" directory
    """
    def __init__(self, object_dir: str, tree_hash: str, commit_message: str, commit_hash=False):
        self.object_dir = object_dir
        self.tree_hash = tree_hash
        self.commit_hash = commit_hash
        self.commit_message = commit_message
        
    def commit_tree(self, parent_hash=None):
        try:
            # Format commit
            content = f"tree {self.tree_hash})\n"
            # Option "-p" - parent commit objects
            if self.commit_hash:
                content +=  f"parent {parent_hash}\n"
            # Hardcoded any valid name/email author/committer fields
            content += f"author Antonio Costa <antonio@gmail.com> 1714599041 -0600\n"
            content += f"comitter Antonio Costa <antonio@gmail.com> 1714599041 -0600\n"
            content += f"\n{self.commit_message}\n"
            
            # Commit object
            content = f"commit {len(content)}\0{content}"
            
            # SHA1-hash
            content = content.encode()
            sha1 = hashlib.sha1(content).hexdigest()
            
            # Compress data
            compressed_data = zlib.compress(content)
            
            # Write to ".git/objects" 
            folder, file = sha1[:2], sha1[2:]
            os.makedirs(os.path.join(self.object_dir, folder), exist_ok=True)
            with open(os.path.join(self.object_dir, folder, file), "wb") as file:
                file.write(compressed_data)
            
            return sha1
        except (OSError, zlib.error) as e:
            print(f"Error: {e}")
            return None
def main():
    # Defines paths for a new git repository
    repo = GitRepository(work_tree=os.getcwd())
    
    command = sys.argv[1]
    if command == "init":
        repo.git_init()
    elif command == "cat-file":
        if len(sys.argv) < 4:
            print("Usage: main.py cat-file <options> <sha1>")
            sys.exit(1)
            
        options = sys.argv[2]
        sha1 = sys.argv[3]
        if options == "-p":  # Display blob object contents
            blob = BlobObject(object_dir=repo.objects_dir, sha1=sha1)
            content = blob.read_blob()
            if content:
                print(content, end="")
    elif command == "hash-object":
        if len(sys.argv) < 3:
            print("Usage: main.py hash-object <options> <file>")
            sys.exit(1)
        # Check for command line arguments 
        options = sys.argv[2] if sys.argv[2] == "-w" else None
        file = sys.argv[3] if options else sys.argv[2]
        
        if options == "-w":
            # Write to objects directory
            new_object = HashObject(object_dir=repo.objects_dir, content=file, write_to_obj=True)
        else:
            new_object = HashObject(object_dir=repo.objects_dir, content=file)
        
        object_hash = new_object.hash_object()
        if object_hash:
            print(object_hash)
    elif command == "ls-tree":
        if len(sys.argv) < 3:
            print("Usage: main.py ls-tree <options> <tree_sha>")
            sys.exit(1)
            
        options = sys.argv[2] if sys.argv[2] == "--name-only" else None
        tree_sha = sys.argv[3] if options else sys.argv[2]
        
        if options == "--name-only":
            tree_object = TreeObject(object_dir=repo.objects_dir, sha1=tree_sha, options=True)
            name = tree_object.ls_tree()
            if name:
                print(name)
        else:
            tree_object = TreeObject(object_dir=repo.objects_dir, sha1=tree_sha, options=False)
            structure = tree_object.ls_tree()
            if structure:
                print(structure)
    elif command == "write-tree":
        if len(sys.argv) < 1:
            print("Usage: main.py write-tree")
            sys.exit(1)
        tree_hash = WriteTree(object_dir=repo.objects_dir)
        hash = tree_hash.write_tree(os.getcwd())
        if hash:
            print(hash)
    elif command == "commit-tree":
        if len(sys.argv) < 5:
            print("Usage: main.py commit-tree <tree_sha> -p <commit_sha> -m <message>")
            sys.exit(1)
            
        tree_sha = sys.argv[2]
        options = sys.argv[3]
        if options == "-p":
            message = sys.argv[6]
            parent_hash = sys.argv[4]
            commit_object = CommitObject(object_dir=repo.objects_dir, tree_hash=tree_sha, commit_message=message, commit_hash=True)
            sha1 = commit_object.commit_tree(parent_hash)
            if sha1:
                print(sha1)
        elif options == "-m":
            message = sys.argv[4]
            commit_object = CommitObject(object_dir=repo.objects_dir, tree_hash=tree_sha, commit_message=message, commit_hash=False)
            sha1 = commit_object.commit_tree(None)
            if sha1:
                print(sha1)
    else:
        raise RuntimeError(f"Unknown command #{command}")

if __name__ == "__main__":
    main()
