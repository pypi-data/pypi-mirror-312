import argparse
from .downloader import download_from_github

def main():
    parser = argparse.ArgumentParser(
        description="Download files and folders from GitHub repositories"
    )
    parser.add_argument(
        "url",
        nargs="?",  # Make the URL optional
        help="GitHub URL to download (e.g., https://github.com/user/repo/tree/branch/path)"
    )
    parser.add_argument(
        "-o", "--output",
        default="./downloaded_files",
        help="Output directory (default: ./downloaded_files)"
    )
    
    args = parser.parse_args()
    
    # If no URL provided, show usage examples and prompt for input
    if not args.url:
        print("\nUsage examples:")
        print("  ghcd https://github.com/user/repo/blob/master/file.pdf")
        print("  ghcd https://github.com/user/repo/tree/master/docs")
        print("  ghcd https://github.com/user/repo")
        print("  ghcd -o ./custom/path https://github.com/user/repo/tree/master\n")
        
        args.url = input("Enter the GitHub URL to download: ").strip()
        
        if not args.url:
            parser.print_help()
            return 1
    
    try:
        download_from_github(args.url, args.output)
        return 0
    except Exception as e:
        print(f"Error: {e}")
        return 1

if __name__ == "__main__":
    main() 