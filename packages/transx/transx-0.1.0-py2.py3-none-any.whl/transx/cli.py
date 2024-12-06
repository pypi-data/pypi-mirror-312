"""Command-line interface for transx.
"""
import os
import sys
import argparse
from transx.formats.pot import PotExtractor
from transx.formats.mo import compile_po_file
from transx.constants import (
    DEFAULT_LOCALES_DIR,
    DEFAULT_MESSAGES_DOMAIN,
    MO_FILE_EXTENSION,
    POT_FILE_EXTENSION
)

def create_parser():
    """Create command line argument parser."""
    parser = argparse.ArgumentParser(
        description="TransX - Translation Management Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # extract command
    extract_parser = subparsers.add_parser(
        "extract",
        help="Extract translatable messages from source files to POT file"
    )
    extract_parser.add_argument(
        "source_path",
        help="Source file or directory to extract messages from"
    )
    extract_parser.add_argument(
        "-o", "--output",
        default=os.path.join(DEFAULT_LOCALES_DIR, DEFAULT_MESSAGES_DOMAIN + POT_FILE_EXTENSION),
        help="Output path for POT file (default: %s/%s%s)" % (
            DEFAULT_LOCALES_DIR, DEFAULT_MESSAGES_DOMAIN, POT_FILE_EXTENSION)
    )
    extract_parser.add_argument(
        "-p", "--project",
        default="Untitled",
        help="Project name (default: Untitled)"
    )
    extract_parser.add_argument(
        "-v", "--version",
        default="1.0",
        help="Project version (default: 1.0)"
    )
    extract_parser.add_argument(
        "-c", "--copyright",
        default="",
        help="Copyright holder"
    )
    extract_parser.add_argument(
        "-b", "--bugs-address",
        default="",
        help="Bug report email address"
    )
    extract_parser.add_argument(
        "-l", "--languages",
        help="Comma-separated list of languages to generate (default: en,zh_CN,ja_JP,ko_KR)"
    )
    extract_parser.add_argument(
        "-d", "--output-dir",
        default=DEFAULT_LOCALES_DIR,
        help="Output directory for language files (default: %s)" % DEFAULT_LOCALES_DIR
    )
    
    # update command
    update_parser = subparsers.add_parser(
        "update",
        help="Update or create PO files for specified languages"
    )
    update_parser.add_argument(
        "pot_file",
        help="Path to the POT file"
    )
    update_parser.add_argument(
        "-l", "--languages",
        help="Comma-separated list of languages to update (default: en,zh_CN,ja_JP,ko_KR)"
    )
    update_parser.add_argument(
        "-o", "--output-dir",
        default=DEFAULT_LOCALES_DIR,
        help="Output directory for PO files (default: %s)" % DEFAULT_LOCALES_DIR
    )
    
    # compile command
    compile_parser = subparsers.add_parser(
        "compile",
        help="Compile PO files to MO files"
    )
    compile_parser.add_argument(
        "po_files",
        nargs="+",
        help="PO files to compile"
    )
    
    return parser

def extract_command(args):
    """Execute extract command."""
    if not os.path.exists(args.source_path):
        print("Error: Path does not exist: %s" % args.source_path, file=sys.stderr)
        return 1
        
    # Ensure output directory exists
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    
    # Create POT extractor
    extractor = PotExtractor(args.output)
    
    # If source_path is a directory, recursively scan all Python files
    if os.path.isdir(args.source_path):
        for root, _, files in os.walk(args.source_path):
            for file in files:
                if file.endswith(".py"):
                    file_path = os.path.join(root, file)
                    print("Scanning %s for translatable messages..." % file_path)
                    extractor.scan_file(file_path)
    else:
        print("Scanning %s for translatable messages..." % args.source_path)
        extractor.scan_file(args.source_path)
    
    # Save POT file
    extractor.save_pot(
        project=args.project,
        version=args.version,
        copyright_holder=args.copyright,
        bugs_address=args.bugs_address
    )
    
    # Generate language files
    languages = args.languages.split(",") if args.languages else ["en", "zh_CN", "ja_JP", "ko_KR"]
    locales_dir = os.path.abspath(args.output_dir)
    extractor.generate_language_files(languages, locales_dir)
    print("POT file created and language files updated: %s" % args.output)
    return 0

def update_command(args):
    """Execute update command."""
    if not os.path.exists(args.pot_file):
        print("Error: POT file not found: %s" % args.pot_file, file=sys.stderr)
        return 1
    
    # Create POT extractor and load
    extractor = PotExtractor(args.pot_file)
    extractor.messages.load(args.pot_file)
    
    # Generate language files
    languages = args.languages.split(",") if args.languages else ["en", "zh_CN", "ja_JP", "ko_KR"]
    locales_dir = os.path.abspath(args.output_dir)
    extractor.generate_language_files(languages, locales_dir)
    print("Language files updated.")
    return 0

def compile_command(args):
    """Execute compile command."""
    success = True
    for po_file in args.po_files:
        if not os.path.exists(po_file):
            print("Error: PO file not found: %s" % po_file, file=sys.stderr)
            success = False
            continue
            
        # Build MO file path (in the same directory as PO file)
        mo_file = os.path.splitext(po_file)[0] + MO_FILE_EXTENSION
        print("Compiling %s to %s" % (po_file, mo_file))
        
        try:
            compile_po_file(po_file, mo_file)
        except Exception as e:
            print("Error compiling %s: %s" % (po_file, e), file=sys.stderr)
            success = False
    
    return 0 if success else 1

def main():
    """Main entry function."""
    parser = create_parser()
    args = parser.parse_args()
    
    if args.command == "extract":
        return extract_command(args)
    elif args.command == "update":
        return update_command(args)
    elif args.command == "compile":
        return compile_command(args)
    else:
        parser.print_help()
        return 1

if __name__ == "__main__":
    sys.exit(main())
