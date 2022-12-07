import os
import sys
import PyPDF2
from PyPDF2 import PdfReader, PdfWriter
import re


def print_usage():  # print usage if invalid option is provided
    print(
        ''' Usage: pdfmerger.py pdf_file1 pdf_file2 [option]
        Without any pdf_file provided all PDFs in directory will be used.
        Without any option provided, given ( or all ) PDFs will be only merged.

        Options:
        -e,     encrypt saved PDF file with given password
        -d,     decrypt PDF file with provided password

        Help option:
        -h,--help   display this message''')


def all_files(saved_name):  # merge all files in directory
    merger = PyPDF2.PdfFileMerger()
    for file in os.listdir(os.curdir):
        if file.endswith(".pdf"):  # search current directory for pdf files
            merger.append(file)  # add all pages to merger
    merger.write(f"{saved_name}.pdf")  # save merged file as given name
    print(f"File was saved as {saved_name}.pdf")
    merger.close()


def certain_files(saved_name):  # merge only provided files in directory
    merger = PyPDF2.PdfFileMerger()
    for file in sys.argv[1:]:
        if file.endswith(".pdf"):  # search through arguments provided for pdf files
            merger.append(file)  # add all pages to merger
    merger.write(f"{saved_name}.pdf")  # save merged file as given name
    print(f"File was saved as {saved_name}.pdf")
    merger.close()


def encrypt(saved_name, password):  # encrypt with password provided and save the file
    reader = PdfReader(f"{saved_name}.pdf")
    writer = PdfWriter()
    for page in reader.pages:  # add all pages to writer
        writer.add_page(page)
    writer.encrypt(f"{password}")  # add password to file
    with open(f"{saved_name}.pdf", "wb") as f:  # save new PDF to a file
        writer.write(f)
    print(f"File {saved_name}.pdf was successfully encrypted!")


def decrypt_with_files_provided(file):  # decrypt only provided files in directory
    reader = PdfReader(file)
    writer = PdfWriter()
    if reader.is_encrypted:  # check if file is encrypted
        print(f"File {file} is encrypted!")
        old_pass = input(f"Enter password used to encrypt {file}: ")  # ask for password to decrypt file
        reader.decrypt(old_pass)  # decrypt
        for page in reader.pages:  # add all pages to writer
            writer.add_page(page)
        with open(f"{file}", "wb") as f:  # save new PDF to file
            writer.write(f)


def decrypt_all_files():  # decrypt all files in directory
    directory_list = os.listdir()  # default -> current directory
    for file in directory_list:
        if file.endswith(".pdf"):  # search current directory for pdf files
            reader = PdfReader(file)
            writer = PdfWriter()
            if reader.is_encrypted:  # check if file is encrypted
                print(f"File {file} is encrypted!")
                old_pass = input(f"Enter password used to encrypt {file}: ")  # ask for password to decrypt file
                reader.decrypt(old_pass)  # decrypt
                for page in reader.pages:  # add all pages to writer
                    writer.add_page(page)
                with open(f"{file}", "wb") as f:  # save new PDF to file
                    writer.write(f)


def main():
    args = sys.argv[1:]
    if "-h" in args or re.findall("-[^hed]", str(args)):  # help or RegEx for invalid option
        print_usage()

    elif "-e" in args:  # ENCRYPTING
        saved_name = input("Enter name you want to save PDF as: ")  # ask for name to save as
        password = input("Enter password you want to encrypt with: ")  # ask for password
        for file in args:
            if file.endswith(".pdf"):  # search through arguments provided for PDF files
                decrypt_with_files_provided(file)  # check if all provided PDF files are decrypted
                certain_files(saved_name)  # merge files provided
                encrypt(saved_name, password)  # encrypt with given password
                exit(0)  # exit script
        # if there is none PDF file provided
        decrypt_all_files()  # check if all PDF files in current directory are decrypted
        all_files(saved_name)  # merge all files
        encrypt(saved_name, password)  # encrypt with given password

    elif "-d" in args:  # DECRYPTING
        for file in args:
            if file.endswith(".pdf"):  # search through arguments provided for PDF files
                decrypt_with_files_provided(file)  # check if all provided PDF files are decrypted
                print("Successfully decrypted!")  # print confirmation
                exit(0)  # exit script
        decrypt_all_files()  # decrypt all PDF files in current directory
        print("Successfully decrypted!")  # print confirmation

    else:  # if none of -h -e or -d option is provided only merge PDF files
        saved_name = input("Enter name you want to save PDF as: ")  # ask for name to save as
        if len(args) < 1:  # there are no PDF files provided
            all_files(saved_name)  # merge all files in directory

        else:  # there are PDF files provided
            certain_files(saved_name)  # merge only PDF files provided


if __name__ == '__main__':
    main()
