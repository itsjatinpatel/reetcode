"""
https://leetcode.com/problems/design-in-memory-file-system/

Design a data structure that simulates an in-memory file system.

Implement the FileSystem class:

FileSystem() Initializes the object of the system.

List<String> ls(String path)
If path is a file path, returns a list that only contains this file's name.
If path is a directory path, returns the list of file and directory names in this directory.
The answer should in lexicographic order.

void mkdir(String path) Makes a new directory according to the given path. The given directory path does not exist. If the middle directories in the path do not exist, you should create them as well.

void addContentToFile(String filePath, String content)
If filePath does not exist, creates that file containing given content.
If filePath already exists, appends the given content to original content.

String readContentFromFile(String filePath) Returns the content in the file at filePath.


Example 1:


Input
["FileSystem", "ls", "mkdir", "addContentToFile", "ls", "readContentFromFile"]
[[], ["/"], ["/a/b/c"], ["/a/b/c/d", "hello"], ["/"], ["/a/b/c/d"]]
Output
[null, [], null, null, ["a"], "hello"]

Explanation
FileSystem fileSystem = new FileSystem();
fileSystem.ls("/");                         // return []
fileSystem.mkdir("/a/b/c");
fileSystem.addContentToFile("/a/b/c/d", "hello");
fileSystem.ls("/");                         // return ["a"]
fileSystem.readContentFromFile("/a/b/c/d"); // return "hello"


Constraints:

1 <= path.length, filePath.length <= 100
path and filePath are absolute paths which begin with '/' and do not end with '/' except that the path is just "/".
You can assume that all directory names and file names only contain lowercase letters, and the same names will not exist in the same directory.
You can assume that all operations will be passed valid parameters, and users will not attempt to retrieve file content or list a directory or file that does not exist.
You can assume that the parent directory for the file in addContentToFile will exist.
1 <= content.length <= 50
At most 300 calls will be made to ls, mkdir, addContentToFile, and readContentFromFile.
"""

from abc import ABC


class Inode(ABC):
    def __init__(self, inode_id: int):
        self.inode_id = inode_id


class File(Inode):
    def __init__(self, inode_id: int):
        super().__init__(inode_id)
        self.content = bytearray()


class Directory(Inode):
    def __init__(self, inode_id: int):
        super().__init__(inode_id)
        self.entries = {}


class FileSystem:
    def __init__(self):
        self._next_inode_id = 0
        self._root = Directory(self._allocate_inode())

    def ls(self, path: str) -> list[str]:
        inode = self._resolve(path)

        if isinstance(inode, Directory):
            return sorted(inode.entries.keys())
        return [self._basename(path)]

    def mkdir(self, path: str) -> None:
        self._resolve(path, True)

    def addContentToFile(self, filePath: str, content: str) -> None:
        inode = self._resolve(self._parent_path(filePath), True)
        file_name = self._basename(filePath)

        assert isinstance(inode, Directory)

        if file_name not in inode.entries:
            inode.entries[file_name] = File(self._allocate_inode())

        file_inode = inode.entries[file_name]
        file_inode.content.extend(content.encode())

    def readContentFromFile(self, filePath: str) -> str:
        inode = self._resolve(filePath)

        assert isinstance(inode, File)
        return inode.content.decode()

    def _allocate_inode(self) -> int:
        inode_id = self._next_inode_id
        self._next_inode_id += 1
        return inode_id

    def _resolve(self, path: str, create_dirs: bool = False) -> Inode:
        inode = self._root
        for name in self._split(path):
            if name not in inode.entries and create_dirs:
                inode.entries[name] = Directory(self._allocate_inode())
            inode = inode.entries[name]
        return inode

    def _split(self, path: str) -> list[str]:
        return [p for p in path.split("/") if p]

    def _parent_path(self, path: str) -> str:
        return "/".join(path.split("/")[:-1])

    def _basename(self, path: str) -> str:
        return path.split("/")[-1]
