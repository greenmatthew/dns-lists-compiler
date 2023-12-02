# Makefile for building and cleaning the program

# Variables
name = compile_dns_lists
main_script = main.py
source = src/
output = bin/
build = build/
specs = build/specs/

# Targets
all: build

build:
	@# Create the output directory if it doesn't exist
	@mkdir -p $(output)
	@mkdir -p $(build)
	@mkdir -p $(specs)

	@# Compile to executable using PyInstaller
	@pyinstaller --onefile $(source)$(main_script) --distpath=$(output) --workpath=$(build) --specpath=$(specs) --name=$(name)

clean-all:
	@# Remove the build, specs, and output directories
	@rm -rf $(build) $(specs) $(output)
	@echo "Cleaned build, specs, and output directories."

clean:
	@# Remove the build and specs directories
	@rm -rf $(build) $(specs)
	@echo "Cleaned build and specs directories."

run: build
	@# Run the generated executable
	@./$(output)$(name)

.PHONY: all build clean-all clean run
