#!/usr/bin/env python3
import os
import stat
import pwd
import grp
import magic
import argparse
import sys
import subprocess
from datetime import datetime
from io import StringIO

def write_to_clipboard(data):
    """
    Attempt to write data to system clipboard.
    Supports Windows, macOS, and various Linux clipboard managers.
    Returns True if successful, False otherwise.
    """
    if sys.platform == 'win32':
        try:
            # Windows
            process = subprocess.Popen(['clip'], stdin=subprocess.PIPE, shell=True)
            process.communicate(data.encode('utf-8'))
            return True
        except (subprocess.SubprocessError, OSError):
            return False

    # Try each clipboard program in order
    clipboard_programs = [
        ['pbcopy'],  # macOS
        ['xclip', '-selection', 'clipboard'],  # Linux with xclip
        ['xsel', '--clipboard', '--input'],  # Linux with xsel
        ['wl-copy'],  # Wayland
        ['termux-clipboard-set']  # Termux on Android
    ]

    for program in clipboard_programs:
        try:
            process = subprocess.Popen(program, stdin=subprocess.PIPE)
            process.communicate(data.encode('utf-8'))
            if process.returncode == 0:
                return True
        except (FileNotFoundError, subprocess.SubprocessError):
            continue

    return False

def get_file_details(path):
    """Get detailed file information similar to ls -la"""
    stats = os.stat(path)
    # Get file mode (permissions)
    mode = stat.filemode(stats.st_mode)
    # Get owner and group names
    try:
        owner = pwd.getpwuid(stats.st_uid).pw_name
    except KeyError:
        owner = str(stats.st_uid)
    try:
        group = grp.getgrgid(stats.st_gid).gr_name
    except KeyError:
        group = str(stats.st_gid)
    # Get file size
    size = stats.st_size
    # Get modification time
    mtime = datetime.fromtimestamp(stats.st_mtime).strftime('%b %d %H:%M')
    return f"{mode} {stats.st_nlink} {owner} {group} {size:8d} {mtime} {os.path.basename(path)}"

def is_binary(file_path):
    """
    Use python-magic to check if a file is binary
    """
    try:
        mime = magic.from_file(file_path, mime=True)
        return not mime.startswith('text/')
    except Exception as e:
        print(f"Error checking file type with python-magic: {e}")
        return True

def process_directory(directory, ignore_dirs, output_file=None, clipboard_buffer=None):
    """Process a directory and its subdirectories"""
    # Skip directories that match any pattern in ignore_dirs
    base_dir = os.path.basename(directory)
    if any(pattern in base_dir for pattern in ignore_dirs):
        return

    # Prepare output function
    def write_output(*args, **kwargs):
        message = ' '.join(str(arg) for arg in args)
        if output_file:
            print(message, file=output_file, **kwargs)
        if clipboard_buffer is not None:
            print(message, file=clipboard_buffer, **kwargs)
        print(message, **kwargs)

    # First, get all entries and sort them
    try:
        entries = sorted(os.listdir(directory))
    except PermissionError:
        write_output(f"Permission denied: {directory}")
        return

    # Print directory header
    write_output(f"\nDirectory: {directory}")
    write_output("total", len(entries))

    # Process all entries
    for entry in entries:
        # Skip directories that match any pattern in ignore_dirs
        if any(pattern in entry for pattern in ignore_dirs):
            continue

        full_path = os.path.join(directory, entry)

        # Print ls -la style information
        try:
            write_output(get_file_details(full_path))
            # If it's a regular file and not binary, print its contents
            if os.path.isfile(full_path) and not is_binary(full_path):
                write_output("\n==> File contents of:", entry, "<==")
                try:
                    with open(full_path, 'r', encoding='utf-8') as f:
                        write_output(f.read())
                    write_output("=" * 40)
                except Exception as e:
                    write_output(f"Error reading file: {e}")

            # If it's a directory, recursively process it
            if os.path.isdir(full_path):
                process_directory(full_path, ignore_dirs, output_file, clipboard_buffer)
        except Exception as e:
            write_output(f"Error processing {entry}: {e}")

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description='List directory contents with detailed information and file contents.'
    )
    parser.add_argument(
        'directory',
        help='Directory to process'
    )
    parser.add_argument(
        '-o', '--output',
        help='Output file to write results to (in addition to stdout)',
        type=argparse.FileType('w'),
        default=None
    )
    parser.add_argument(
        '-x', '--exclude',
        help='Patterns to exclude from directory processing',
        nargs='+',
        default=['.git']  # Default to excluding .git directories
    )
    parser.add_argument(
        '-c', '--clipboard',
        help='Copy output to clipboard',
        action='store_true'
    )

    return parser.parse_args()

def main():
    args = parse_arguments()

    if not os.path.isdir(args.directory):
        print(f"Error: {args.directory} is not a directory")
        sys.exit(1)

    # Get and print the absolute path
    abs_path = os.path.abspath(args.directory)
    header = f"Processing directory: {abs_path}\n"

    # Set up clipboard buffer if needed
    clipboard_buffer = StringIO() if args.clipboard else None

    print(header)
    if args.output:
        print(header, file=args.output)
    if clipboard_buffer:
        print(header, file=clipboard_buffer)

    try:
        process_directory(abs_path, ignore_dirs=args.exclude,
                        output_file=args.output, clipboard_buffer=clipboard_buffer)

        # Copy to clipboard if requested
        if args.clipboard:
            clipboard_content = clipboard_buffer.getvalue()
            if not write_to_clipboard(clipboard_content):
                print("Warning: Failed to copy to clipboard. Make sure pbcopy (macOS) or xclip (Linux) is installed.",
                      file=sys.stderr)
    finally:
        if args.output:
            args.output.close()
        if clipboard_buffer:
            clipboard_buffer.close()

if __name__ == "__main__":
    main()
