"""
Author: Jess Williams
Email: jessgwiii@gmail.com
Description: Provides common utilities used in other Inuxnet Projects
"""
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet
from getpass import getpass
import base64
import os
import sys
import re
import argparse
import traceback


# Exit Codes
A_OK = 0
INVALIDKEYFILE = 1
INVALIDOUTPUTPATH = 2
INVALIDARGUMENTS = 3
INVALIDPASSPHRASE = 4
UNEXPECTEDERROR = 5


class DecryptError(IOError):
    pass


class EncryptError(IOError):
    pass


def validate_argument(argument: object, arg_types: type, arg_name: str = "argument", nullable: bool = False,
                      message: str = "Parameter {arg_name} '{argument}' must be of type {' or '.join([ f'{x}' for x "
                                     "in arg_types ])}.") -> object:
    """
    Validates argument, raises TypeError or returns argument
    :param argument: <class 'any'>
        - This can be any type that needs to match
    :param arg_types: <class 'list'> or <class 'tuple'> or <class 'type'>
        - A list/tuple of <class 'type'> to match
    :param arg_name: <class 'str'>
        - The name of the argument being passed in. Defaults to "argument"
    :param nullable: <class 'bool'>
        - If None is allowed as an input parameter
    :param message: <class 'str'>
        - Custom error message, defaults to:
          f"Parameter {arg_name} '{argument}' must be of type {' or '.join([ f'{x}' for x in arg_types ])}"
    :return: <class 'object'>
        - returns the argument object
    """
    if not isinstance(arg_types, list) and not isinstance(arg_types, tuple):
        if isinstance(arg_types, type):
            arg_types = [arg_types]
        else:
            raise TypeError(f"Parameter arg_types '{arg_types}' must be of type {list} or {tuple}")
    elif len(arg_types) == 0:
        raise ValueError(
            f"Parameter arg_types cannot be empty must have at least one value. len(arg_types)={len(arg_types)}")
    if not isinstance(message, str):
        raise TypeError(f"Parameter message '{message}' must be of type {str}")
    matches = 0
    for arg_type in arg_types:
        if not isinstance(arg_type, type):
            raise TypeError(f"arg_types=['{arg_type}',...] must be of type {type}")
        if isinstance(argument, arg_type) or (argument is None and nullable):
            matches += 1
    if matches == 0:
        cmd = f'f"{message}"'
        msg = eval(cmd)
        raise TypeError(msg)
    return argument


def is_empty_string(arg: str, arg_name: str, nullable: bool = False) -> str:
    """
    Validates arguments and ensures no empty string if not nullable
    :param arg: <class 'str'>
        - Since it is validating an empty string, must be a string
    :param arg_name: <class 'str'>
        - The argument name, defaults to 'argument'
    :param nullable: <class 'bool'>
        - If None is allowed as an input parameter
    :return: <class 'str'>
        - Returns the string passed in.
    """
    validate_argument(arg, str, arg_name, nullable)
    if not nullable and arg.strip() == '':
        raise ValueError(f"{arg_name} '{arg}' must have a valid value, cannot be empty.")

    return arg


def validate_filepath(filepath: str):
    """
    Validates file path.
    :param filepath: <class 'str'>
        - The filepath to validate
    """
    validate_argument(filepath, str, "filepath")
    # Check if File exists
    if not os.path.isfile(filepath):
        raise ValueError(f"{filepath} is invalid. Either invalid path or permissions.")


def derive_key(passphrase: str, salt: bytes) -> bytes:
    """
    Derives a key from passphrase and salt.
    :param passphrase: <class 'str'>
        - The passphrase to derive key from.
    :param salt: <class 'bytes'>
        - The salt to spice the key.
    :return: <class 'bytes'>
    """
    validate_argument(passphrase, str, "passphrase")
    validate_argument(salt, bytes, "salt")
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(passphrase.encode()))
    return key


def encrypt(data: bytes, passphrase: str, salt: bytes = None) -> bytes:
    """
    Encrypts a list of bytes, returns encrypted bytes
    :param data: <class 'bytes'>
        - The unencrypted bytes.
    :param passphrase: <class 'str'>
        - The passphrase to encrypt with.
    :param salt: <class 'bytes'>
        - Season the encryption, defaults to None and generates random salt
    :return: <class 'bytes'>
        - Encrypted bytes
    """
    validate_argument(data, bytes, "data")
    validate_argument(passphrase, str, "passphrase")
    validate_argument(salt, bytes, "salt", True)

    if salt is None:
        # Generate a random salt
        salt = os.urandom(16)

    # Derive the key from the passphrase
    key = derive_key(passphrase, salt)

    # Create a Fernet object
    fernet = Fernet(key)

    try:
        # Encrypt the file data
        encrypted_data = fernet.encrypt(data)
        return salt + encrypted_data
    except Exception as e:
        raise EncryptError(f"Unable to encrypt data. {e}")


def encrypt_file(file_path: str, passphrase: str, output_path: str):
    """
    Encrypts file
    :param file_path: <class 'str'>
        - The file path of the file to encrypt.
    :param passphrase: <class 'str'>
        - The passphrase to encrypt the file with.
    :param output_path: <class 'str'>
        - The file path of the output encrypted file.
    """
    validate_filepath(file_path)
    validate_argument(passphrase, str, "passphrase")
    validate_argument(output_path, str, "output_path")

    # Read the file content
    with open(file_path, 'rb') as file:
        file_data = file.read()

    encrypted_data = encrypt(file_data, passphrase)

    # Write the encrypted data to the output file
    try:
        with open(output_path, 'wb') as file:
            file.write(encrypted_data)
    except Exception as e:
        raise IOError(f"Unable to write {output_path}. Check permissions or disk space. {e}")


def decrypt(data: bytes, passphrase: str) -> bytes:
    """
    Decrypts bytes of data with passphrase, returns string
    :param data: <class 'bytes'>
        - Encrypted bytes
    :param passphrase:
        - Passphrase to decrypt
    :return: <class 'bytes'>
        - Decrypted data
    """
    validate_argument(data, bytes, "data")
    validate_argument(passphrase, str, "passphrase")

    try:
        # Extract the salt (first 16 bytes)
        salt = data[:16]
        encrypted_data = data[16:]

        # Derive the key from the passphrase
        key = derive_key(passphrase, salt)

        # Create a Fernet object
        fernet = Fernet(key)

        # Decrypt the file data
        decrypted_data = fernet.decrypt(encrypted_data)
        return decrypted_data
    except Exception as e:
        raise DecryptError(f"Cannot Decrypt. Invalid Passphrase or Encrypted File. {e}")


def decrypt_file(file_path: str, passphrase: str, output_path: str):
    """
    Derives a key from bytes
    :param file_path: <class 'str'>
        - The file path of the encrypted file to decrypt
    :param passphrase: <class 'str'>
        - The passphrase the file is encrypted with.
    :param output_path: <class 'str'>
        - The output file path for decrypted file.
    """
    validate_filepath(file_path)
    validate_argument(passphrase, str, "passphrase")
    validate_argument(output_path, str, "output_path")

    # Read the encrypted file content
    with open(file_path, 'rb') as file:
        file_data = file.read()

    decrypted_data = decrypt(file_data, passphrase)

    # Write the decrypted data to the output file
    try:
        with open(output_path, 'wb') as file:
            file.write(decrypted_data)
    except Exception as e:
        raise IOError(f"Unable to write {output_path}. Check permissions or disk space. {e}")


def validate_password(password: str) -> bool:
    """
    Validates password
    :param password: <class 'str'>
    :return: <class 'bool'>
    """
    validate_argument(password, str, "password")
    if len(password) < 8:
        printpasswordhelp("Invalid Length")
        return False

    if not re.search(r'[A-Z]', password):
        printpasswordhelp("No Uppercase")
        return False

    if not re.search(r'[a-z]', password):
        printpasswordhelp("No Lowercase")
        return False

    if not re.search(r'\d', password):
        printpasswordhelp("No Number")
        return False

    if not re.search(r'[~!@#$%^&*()_+`\-={}|[\]:";<>?,./]', password):
        printpasswordhelp("No Special Characters")
        return False

    if re.search(r"[ '\']", password):
        printpasswordhelp("Cannot contain spaces or apostrophes")
        return False

    return True


def printpasswordhelp(msg: str):
    """
    Prints Password requirments
    :param msg: <class 'str'>
        - The specific message
    """
    validate_argument(msg, str, "msg")
    print(f"Invalid Password ({msg}):", file=sys.stderr)
    print("  * Must contain at least one Uppercase Letter", file=sys.stderr)
    print("  * Must Contain at least 1 Lowercase Letter", file=sys.stderr)
    print("  * Must Contain at least 1 Number", file=sys.stderr)
    print("  * Must Contain at least one of the following", file=sys.stderr)
    print("    special characters ~!@#$%^&*()_-+`{}|[]\\:\";<>?,/.", file=sys.stderr)
    print("  * Must *NOT* Contain spaces or apostrophes", file=sys.stderr)
    print("  * Must be at least 8 characters in length.")


def get_valid_password(validate: bool = True, complexity: bool = True) -> str:
    """
    Returns a valid password
    :param validate: <class 'bool'>
        - Must enter the password twice if True, defaults to True
    :param complexity: <class 'bool'>
        - Password must be reasonably complex, defaults to True
    :return: <class 'str'>
        - The valid password entered
    """
    validate_argument(validate, bool, "validate")
    validate_argument(complexity, bool, "complexity")
    valid = False
    password = None
    while not valid:
        password = getpass("Enter your passphrase: ")

        if complexity:
            if not validate_password(password):
                continue

        if validate:
            validation = getpass("ReEnter your passphrase: ")
            if password != validation:
                printpasswordhelp("Passwords do not match!")
                continue

        valid = True

    return password


def process_coding_arguments(parser: argparse.ArgumentParser):
    """
    Processes common arguments for Encoding/Decoding entry points
    :param parser: <class 'argparse.ArgumentParser'>
        - The parser to process arguments.
    """
    validate_argument(parser, argparse.ArgumentParser, "parser")
    parser.add_argument("-p", "--passphrase", type=str,
                        help="(Optional) Passphrase to encrypt the info, if omitted will query user.")
    parser.add_argument("-k", "--keyfile", type=str,
                        help="The file that needs to be encrypted or decrypted.")
    parser.add_argument("-f", "--outfile", type=str, help="The resulting output file.")


def validate_coding_arguments(parser: argparse.ArgumentParser, args: argparse.Namespace):
    """
    Validates common arguments for Encoding/Decoding entry points
    :param parser: <class 'argparse.ArgumentParser'>
        - The parser to process arguments.
    :param args: <class 'argparse.Namespace'>
        - The parsed arguments.
    """
    validate_argument(parser, argparse.ArgumentParser, "parser")
    validate_argument(args, argparse.Namespace, "args")
    if not args.keyfile:
        parser.print_help()
        print("ERROR: Must provide an input file.", file=sys.stderr)
        sys.exit(INVALIDARGUMENTS)
    if not args.outfile:
        parser.print_help()
        print("ERROR: Must provide an output file.", file=sys.stderr)
        sys.exit(INVALIDARGUMENTS)
    if not args.passphrase:
        if args.operation == "ENCRYPT":
            args.passphrase = get_valid_password()
        else:
            args.passphrase = get_valid_password(False, False)
    else:
        if args.operation == "ENCRYPT":
            if not validate_password(args.passphrase):
                sys.exit(INVALIDPASSPHRASE)


def main_encryptfile():
    """
    Main Entry point for Encrypting a file
    """
    parser = argparse.ArgumentParser(description="Encrypts a file with passphrase.",
                                     epilog="""Examples:
  encryptfile -p 'P@ssw0rd' -k ./id_rsa -f /tmp/id_rsa.enc
  encryptfile --passphrase='P@ssw0rd' --keyfile=./id_rsa --outfile=/tmp/id_rsa.enc
  encryptfile -k ./id_rsa -f /tmp/id_rsa.enc""", formatter_class=argparse.RawTextHelpFormatter)
    process_coding_arguments(parser)
    args = parser.parse_args()
    args.operation = "ENCRYPT"
    validate_coding_arguments(parser, args)
    try:
        encrypt_file(args.keyfile, args.passphrase, args.outfile)
    except EncryptError as e:
        print(e, file=sys.stderr)
        sys.exit(INVALIDPASSPHRASE)
    except IOError as e:
        print(e, file=sys.stderr)
        if str(e).find("key") >= 0:
            sys.exit(INVALIDKEYFILE)
        else:
            sys.exit(INVALIDOUTPUTPATH)
    except Exception as e:
        traceback.print_exc()
        print(f"Unexpected error. {e}")
        sys.exit(UNEXPECTEDERROR)


def main_decryptfile():
    """
    Main Entry point for Encrypting a file
    """
    parser = argparse.ArgumentParser(description="Decrypts a file with passphrase.",
                                     epilog="""Examples:
  decryptfile -p 'P@ssw0rd' -k ./id_rsa.enc -f /tmp/id_rsa
  decryptfile --passphrase='P@ssw0rd' --keyfile=./id_rsa.enc --outfile=/tmp/id_rsa
  decryptfile -k ./id_rsa.enc -f /tmp/id_rsa""", formatter_class=argparse.RawTextHelpFormatter)
    process_coding_arguments(parser)
    args = parser.parse_args()
    args.operation = "DECRYPT"
    validate_coding_arguments(parser, args)
    try:
        decrypt_file(args.keyfile, args.passphrase, args.outfile)
    except DecryptError as e:
        print(e, file=sys.stderr)
        sys.exit(INVALIDPASSPHRASE)
    except IOError as e:
        print(e, file=sys.stderr)
        if str(e).find("key") >= 0:
            sys.exit(INVALIDKEYFILE)
        else:
            sys.exit(INVALIDOUTPUTPATH)
    except Exception as e:
        traceback.print_exc()
        print(f"Unexpected error. {e}")
        sys.exit(UNEXPECTEDERROR)


def main_cryptfile():
    """
    Main Entry point for Encoding a file
    """
    parser = argparse.ArgumentParser(description="Encrypts or Decrypts a file with passphrase.",
                                     epilog="""Examples:
  cryptfile -o ENCRYPT -p 'P@ssw0rd' -k ./id_rsa -f /tmp/id_rsa.enc
  cryptfile --operation=DECRYPT --passphrase='P@ssw0rd' --keyfile=./id_rsa.enc --outfile=/tmp/id_rsa
  cryptfile -o ENCRYPT -k ./id_rsa -f /tmp/id_rsa.enc""", formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("-o", "--operation", choices=["ENCRYPT", "DECRYPT"], required=True,
                        help="Specify the operation: ENCRYPT or DECRYPT")
    process_coding_arguments(parser)
    args = parser.parse_args()
    validate_coding_arguments(parser, args)
    try:
        if args.operation == 'ENCRYPT':
            encrypt_file(args.keyfile, args.passphrase, args.outfile)
        else:
            decrypt_file(args.keyfile, args.passphrase, args.outfile)
    except (EncryptError, DecryptError) as e:
        print(e, file=sys.stderr)
        sys.exit(INVALIDPASSPHRASE)
    except IOError as e:
        print(e, file=sys.stderr)
        if str(e).find("key") >= 0:
            sys.exit(INVALIDKEYFILE)
        else:
            sys.exit(INVALIDOUTPUTPATH)
    except Exception as e:
        traceback.print_exc()
        print(f"Unexpected error. {e}")
        sys.exit(UNEXPECTEDERROR)


def main_encrypt():
    """
    Main Entry point for encrypt string
    """
    parser = argparse.ArgumentParser(description="Encrypts a string with passphrase.",
                                     epilog="""Examples:
    echo "Secret to encrypt" | encrypt -p 'P@ssw0rd'
    encrypt "Secret to encrypt"
    encrypt "Secret to encrypt" --passphrase='P@ssw0rd'""", formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("-d", "--data", type=str, help="The string data to encrypt.")
    parser.add_argument("-p", "--passphrase", type=str,
                        help="(Optional) Passphrase to encrypt the info, if omitted will query user.")
    args = parser.parse_args()
    if not sys.stdin.isatty():
        args.data = sys.stdin.read()
    else:
        if not args.data:
            parser.print_help()
            print("ERROR: Must provide input data.", file=sys.stderr)
            sys.exit(INVALIDARGUMENTS)
    if not args.passphrase:
        args.passphrase = get_valid_password()
    else:
        if not validate_password(args.passphrase):
            sys.exit(INVALIDPASSPHRASE)

    try:
        encrypted_data = encrypt(args.data.encode('utf-8'), args.passphrase)
        print(base64.b64encode(encrypted_data).decode('utf-8'), end='')
    except Exception as e:
        print(e, sys.stderr)


def main_decrypt():
    """
    Main Entry point for decrypt string
    """
    """
    Main Entry point for encrypt string
    """
    parser = argparse.ArgumentParser(description="Encrypts a string with passphrase.",
                                     epilog="""Examples:
    cat encrypted_file.txt | decrypt -p 'P@ssw0rd'
    decrypt "hd78hgdf832f7g78=="
    decrypt "hd78hgdf832f7g78==" --passphrase='P@ssw0rd'""", formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("-d", "--data", type=str, help="The string data to encrypt.")
    parser.add_argument("-p", "--passphrase", type=str,
                        help="(Optional) Passphrase to encrypt the info, if omitted will query user.")
    args = parser.parse_args()
    if not sys.stdin.isatty():
        args.data = sys.stdin.read()
    else:
        if not args.data:
            parser.print_help()
            print("ERROR: Must provide input data.", file=sys.stderr)
            sys.exit(INVALIDARGUMENTS)
    if not args.passphrase:
        args.passphrase = get_valid_password(False, False)

    original_bytes = base64.b64decode(args.data)
    try:
        decrypted_data = decrypt(original_bytes, args.passphrase)
        print(decrypted_data.decode('utf-8'), end='')
    except Exception as e:
        print(e, file=sys.stderr)


if __name__ == "__main__":
    pass
