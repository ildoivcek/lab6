Develop a class for working with a file. The class must contain basic methods such as reading from a file and writing to a file, as well as the ability to append data to a file (while preserving the existing file contents). The file path and name must be passed through the class constructor.
When creating an instance of the class, it is necessary to check whether the file exists. If the file does not exist, an appropriate exception must be raised. During reading from or writing to the file, if the file is corrupted or writing is impossible, a corresponding exception must be raised. Custom exceptions must be created for this purpose.
Additionally, develop a decorator for logging file creation, read, and write operations. Create a parameterized decorator logged that takes an exception and a mode as arguments. The mode can be "console" or "file". When an exception occurs in a decorated method, it is logged using the logging module. In console mode, logging is output to the console; in file mode, logging is written to a file.
Custom exceptions for clear separation of file-related problems:
File not found (FileNotFound).
File corrupted (problems with access to or reading the file) (FileCorrupted).

Type of file for logging events: text.

Type of file for reading/writing: CSV.


