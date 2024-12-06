# MDFT - Markdown File Trees

Package for generating file trees in Markdown

## Example

The following file tree is automatically generated based on the contents of the specified path.

<!-- mdft src include_files,link -->
- [mdft/](src/mdft)
	- [converter/](src/mdft/converter)
		- [converter.py](src/mdft/converter/converter.py)
		- [\_\_init\_\_.py](src/mdft/converter/__init__.py)
	- [util/](src/mdft/util)
		- [options.py](src/mdft/util/options.py)
		- [command.py](src/mdft/util/command.py)
		- [blueprint.py](src/mdft/util/blueprint.py)
		- [line.py](src/mdft/util/line.py)
		- [\_\_init\_\_.py](src/mdft/util/__init__.py)
	- [file/](src/mdft/file)
		- [\_\_init\_\_.py](src/mdft/file/__init__.py)
		- [file.py](src/mdft/file/file.py)
	- [\_\_init\_\_.py](src/mdft/__init__.py)
	- [scanner/](src/mdft/scanner)
		- [file\_scanner.py](src/mdft/scanner/file_scanner.py)
		- [\_\_init\_\_.py](src/mdft/scanner/__init__.py)
		- [file\_filter.py](src/mdft/scanner/file_filter.py)
	- [\_\_main\_\_.py](src/mdft/__main__.py)
	- [injector/](src/mdft/injector)
		- [\_\_init\_\_.py](src/mdft/injector/__init__.py)
		- [injector.py](src/mdft/injector/injector.py)
