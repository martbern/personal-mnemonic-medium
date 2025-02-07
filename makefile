info:
	@echo "\nThis project uses invoke. \nInstall it using "pip install invoke"\nRun invoke --list to see available commands.\n\n"

image:
	uv run pyright memium
	docker build . -t ghcr.io/martinbernstorff/memium:latest -f Dockerfile