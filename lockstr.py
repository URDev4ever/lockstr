#!/usr/bin/env python3
"""
lockstr - File encryption/decryption tool using Fernet cryptography
"""

import os
import sys
import argparse
import tempfile
from pathlib import Path
from typing import List, Optional, Tuple, Dict

from cryptography.fernet import Fernet, InvalidToken
import pyperclip
from getpass import getpass


BANNER = r"""
   __            __        __
  / /  ___  ____/ /__ ___ / /_____
 / /__/ _ \/ __/  '_/(_-</ __/ __/
/____/\___/\__/_/\_\/___/\__/_/
    By URDev | v2.1
"""

# Magic header to identify lockstr-encrypted files
MAGIC_HEADER = b"LOCKSTR1\x00"
MAGIC_LENGTH = len(MAGIC_HEADER)


class CryptoError(Exception):
    """Custom exception for cryptographic operations"""
    pass


class KeyManager:
    """Handles Fernet key generation and validation"""
    
    @staticmethod
    def generate_key() -> bytes:
        """Generate a new Fernet key and copy to clipboard"""
        key = Fernet.generate_key()
        try:
            pyperclip.copy(key.decode())
        except pyperclip.PyperclipException as e:
            print(f"⚠️  Could not copy to clipboard: {e}")
            raise CryptoError("Failed to copy key to clipboard")
        return key
    
    @staticmethod
    def get_key_from_user() -> bytes:
        """Get key from user input securely"""
        while True:
            key_input = getpass("Enter key: ")
            if not key_input:
                print("Key cannot be empty")
                continue
            
            try:
                key = key_input.encode()
                Fernet(key)  # Validate key format
                return key
            except ValueError as e:
                print(f"Invalid key format: {e}")
                print("Please try again or press Ctrl+C to cancel")


class FileProcessor:
    """Handles file encryption/decryption operations"""
    
    def __init__(self, key: bytes):
        self.cipher = Fernet(key)
    
    def process_file(self, file_path: Path, encrypt: bool = True) -> Tuple[bool, str]:
        """
        Process a single file (encrypt or decrypt)
        Returns (success, error_message)
        """
        try:
            with open(file_path, 'rb') as f:
                data = f.read()
            
            if encrypt:
                # Check if already encrypted with lockstr
                if data.startswith(MAGIC_HEADER):
                    return False, "File is already encrypted with lockstr"
                
                encrypted_data = self.cipher.encrypt(data)
                processed_data = MAGIC_HEADER + encrypted_data
                
            else:
                # Check if file has lockstr header
                if not data.startswith(MAGIC_HEADER):
                    return False, "File is not encrypted with lockstr (missing magic header)"
                
                # Remove header and decrypt
                encrypted_payload = data[MAGIC_LENGTH:]
                processed_data = self.cipher.decrypt(encrypted_payload)
            
            # Write to temporary file first
            with tempfile.NamedTemporaryFile(
                mode='wb',
                dir=file_path.parent,
                delete=False
            ) as tmp:
                tmp.write(processed_data)
                tmp_path = Path(tmp.name)
            
            # Atomic replacement
            os.replace(tmp_path, file_path)
            return True, ""
            
        except InvalidToken as e:
            return False, f"Cryptographic error (wrong key or corrupted data): {e}"
        except PermissionError as e:
            return False, f"Permission denied: {e}"
        except MemoryError as e:
            return False, f"File too large for memory: {e}"
        except Exception as e:
            return False, f"Unexpected error: {e}"


class DirectoryWalker:
    """Handles recursive directory traversal"""
    
    @staticmethod
    def get_files(path: Path, include_hidden: bool = False) -> List[Path]:
        """
        Get all files from a path (recursive if directory)
        """
        files = []
        
        if path.is_file():
            files.append(path)
        elif path.is_dir():
            for item in path.rglob('*'):
                if item.is_file() and not item.is_symlink():
                    # Skip hidden files unless requested
                    if not include_hidden and item.name.startswith('.'):
                        continue
                    files.append(item)
        
        return files
    
    @staticmethod
    def validate_files(files: List[Path]) -> Tuple[bool, List[str]]:
        """Validate file access permissions"""
        errors = []
        
        for file_path in files:
            if not file_path.exists():
                errors.append(f"File not found: {file_path}")
            elif not os.access(file_path, os.R_OK):
                errors.append(f"Cannot read: {file_path}")
            elif not os.access(file_path, os.W_OK):
                errors.append(f"Cannot write: {file_path}")
        
        return len(errors) == 0, errors
    
    @staticmethod
    def display_file_tree(files: List[Path], base_path: Path) -> None:
        """Display files in a tree-like structure"""
        from collections import defaultdict
        
        # Organize files by directory
        dir_structure = defaultdict(list)
        
        for file_path in files:
            relative_path = file_path.relative_to(base_path)
            parent = str(relative_path.parent)
            if parent == ".":
                parent = ""
            dir_structure[parent].append(relative_path.name)
        
        # Sort and display
        sorted_dirs = sorted(dir_structure.keys())
        
        print("\n📁 File structure to be processed:")
        print("-" * 40)
        
        for i, directory in enumerate(sorted_dirs):
            if directory:
                print(f"📂 {directory}/")
            else:
                print("📂 . (current directory)")
            
            files_in_dir = sorted(dir_structure[directory])
            for file_name in files_in_dir:
                prefix = "  └── " if directory else "├── "
                print(f"  {prefix}{file_name}")
            
            if i < len(sorted_dirs) - 1:
                print("")
        
        print("-" * 40)


class LockstrCLI:
    """Main CLI interface"""
    
    def __init__(self):
        self.parser = self._create_parser()
    
    def _create_parser(self) -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser(
            description=BANNER + "\nFile encryption/decryption tool using Fernet cryptography",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            add_help=False,
            epilog="""
⚠️  IMPORTANT SECURITY NOTES:
• The encryption key is NEVER displayed on screen
• Keys are only copied to clipboard during encryption
• Save your key in a secure password manager
• Without the key, encrypted files are unrecoverable
• Magic header prevents double-encryption accidents
            
📝 Examples:
  lockstr encrypt secret.txt
  lockstr decrypt secret.txt
  lockstr encrypt ./documents/ --dry-run
  lockstr encrypt ./backup/ --include-hidden --confirm
  lockstr decrypt ./encrypted/ --continue-on-error
            """
        )
        
        parser.add_argument(
            'mode',
            choices=['encrypt', 'decrypt'],
            nargs='?',
            help='Operation mode (encrypt|decrypt)'
        )
        parser.add_argument(
            'path',
            nargs='?',
            help='File or directory path'
        )
        
        # Optional flags
        parser.add_argument(
            '--include-hidden',
            action='store_true',
            help='Include hidden files (starting with .)'
        )
        parser.add_argument(
            '--continue-on-error',
            action='store_true',
            help='Continue processing other files if one fails'
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be processed without making changes'
        )
        parser.add_argument(
            '--confirm',
            action='store_true',
            help='Ask for confirmation before processing'
        )
        parser.add_argument(
            '-h', '--help',
            action='help',
            help='Show this help message and exit'
        )
        
        return parser
    
    def parse_args(self) -> argparse.Namespace:
        """Parse command line arguments"""
        if len(sys.argv) == 1:
            self.parser.print_help()
            sys.exit(0)
        
        return self.parser.parse_args()
    
    def confirm_operation(self, mode: str, file_count: int) -> bool:
        """Ask for user confirmation"""
        if file_count == 1:
            print(f"\n⚠️  You are about to {mode} 1 file.")
        else:
            print(f"\n⚠️  You are about to {mode} {file_count} files.")
        
        print("This operation is irreversible without the key.")
        
        response = input("Continue? [y/N]: ").strip().lower()
        return response in ('y', 'yes')
    
    def run(self) -> int:
        """Main execution flow"""
        args = self.parse_args()
        
        print(BANNER)
        
        if not args.mode or not args.path:
            print("Error: Mode and path required")
            print(f"Usage: {sys.argv[0]} [encrypt|decrypt] <path>")
            return 1
        
        target_path = Path(args.path)
        
        if not target_path.exists():
            print(f"Error: Path '{args.path}' does not exist")
            return 1
        
        # Get files to process
        files = DirectoryWalker.get_files(target_path, args.include_hidden)
        
        if not files:
            print(f"No valid files found at '{args.path}'")
            if not args.include_hidden:
                print("(Use --include-hidden to include hidden files)")
            return 0
        
        # Display file tree for dry-run or confirmation
        if args.dry_run:
            DirectoryWalker.display_file_tree(files, target_path)
            print(f"\n📊 Summary: {len(files)} file(s) would be processed")
            print("No changes were made (dry-run mode)")
            return 0
        
        # Validate file access
        valid, errors = DirectoryWalker.validate_files(files)
        if not valid:
            print("Access errors found:")
            for error in errors:
                print(f"  {error}")
            if not args.continue_on_error:
                return 1
        
        # Ask for confirmation if requested
        if args.confirm and not self.confirm_operation(args.mode, len(files)):
            print("Operation cancelled.")
            return 0
        
        # Get key
        try:
            if args.mode == 'encrypt':
                key = KeyManager.generate_key()
                print("\n✅ New key generated and copied to clipboard")
                print("⚠️  IMPORTANT: Save this key in a secure location!")
                print("   Without it, your files will be permanently inaccessible.")
                print("   The key is ONLY in your clipboard, not shown on screen.")
            else:  # decrypt
                key = KeyManager.get_key_from_user()
                print("✓ Key accepted")
        except CryptoError as e:
            print(f"Error: {e}")
            return 1
        
        # Process files
        processor = FileProcessor(key)
        success_count = 0
        error_count = 0
        errors_list = []
        
        print(f"\nProcessing {len(files)} file(s)...")
        print("-" * 40)
        
        for i, file_path in enumerate(files, 1):
            print(f"[{i}/{len(files)}] {file_path}", end="", flush=True)
            
            success, error_msg = processor.process_file(
                file_path,
                encrypt=(args.mode == 'encrypt')
            )
            
            if success:
                print(" ✓")
                success_count += 1
            else:
                print(" ✗")
                print(f"     Error: {error_msg}")
                error_count += 1
                errors_list.append((file_path, error_msg))
                
                if not args.continue_on_error:
                    print(f"\n❌ Aborting due to error (use --continue-on-error to continue)")
                    
                    # Report partial results
                    if success_count > 0:
                        print(f"\nPartial operation completed:")
                        print(f"  ✓ Successfully processed: {success_count} file(s)")
                        print(f"  ✗ Failed: {error_count} file(s)")
                        if args.mode == 'encrypt':
                            print(f"  ⚠️  Some files may be encrypted, others not")
                            print(f"  ⚠️  Manual intervention may be required")
                    
                    return 1
        
        # Report final results
        print(f"\n{'='*40}")
        if args.mode == 'encrypt':
            print(f"✅ ENCRYPTION COMPLETE")
            print(f"   • Files encrypted: {success_count}")
            print(f"   • Protected against double-encryption")
        else:
            print(f"✅ DECRYPTION COMPLETE")
            print(f"   • Files decrypted: {success_count}")
        
        if error_count > 0:
            print(f"   • Files failed: {error_count}")
            
            if args.continue_on_error:
                print(f"\n📋 Errors encountered (continued anyway):")
                for file_path, error_msg in errors_list[:5]:  # Show first 5 errors
                    print(f"   • {file_path}: {error_msg}")
                if len(errors_list) > 5:
                    print(f"   • ... and {len(errors_list) - 5} more")
        
        if args.mode == 'encrypt':
            print(f"\n🔑 KEY INFORMATION:")
            print(f"   • Key was copied to your clipboard")
            print(f"   • Save it in a secure password manager")
            print(f"   • Without this key, files are PERMANENTLY inaccessible")
            print(f"   • The key was NEVER displayed on screen")
        
        if error_count > 0 and not args.continue_on_error:
            return 1
        
        return 0


def main():
    """Entry point"""
    cli = LockstrCLI()
    return cli.run()


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n⏹️  Operation cancelled by user")
        sys.exit(130)
    except MemoryError:
        print("\n\n💥 Out of memory - file too large")
        print("   Consider using smaller files or streaming approach")
        sys.exit(137)
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        print("   Please report this issue")
        sys.exit(1)
