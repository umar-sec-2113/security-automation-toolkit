import hashlib
import os
import datetime


def show_menu():
    print("=" * 65)
    print("SECURITY TOOLKIT")
    print("=" * 65)
    print("1. Calculate File Hash")
    print("2. Check File Integrity")
    print("3. File Information")
    print("4. Security Report")
    print("5. Exit")


def calculate_sha256(filepath):
    with open(filepath, "rb") as file:
        data = file.read()

    hash_object = hashlib.sha256()
    hash_object.update(data)

    return hash_object.hexdigest()


def calculate_hash():
    filepath = input("Enter your file name or path: ")

    try:
        final_hash = calculate_sha256(filepath)

        print(f"SHA-256: {final_hash}")

        hash_file = filepath + ".hash"

        with open(hash_file, "w") as file:
            file.write(final_hash)

        print(f"Hash saved to: {hash_file}")

    except FileNotFoundError:
        print("File is missing!")


def check_integrity():
    filepath = input("Enter your file name or path: ")
    hash_file = filepath + ".hash"

    try:
        with open(hash_file, "r") as file:
            saved_hash = file.read().strip()

        current_hash = calculate_sha256(filepath)

        if current_hash == saved_hash:
            print("File is Unchanged")
        else:
            print("WARNING: File has been modified.")

    except FileNotFoundError:
        print("File or hash file is missing!")


def get_file_information(filepath):
    return {
        "Name": os.path.basename(filepath),
        "Extension": os.path.splitext(filepath)[1],
        "Size": f"{os.path.getsize(filepath)} bytes",
        "Full path": os.path.abspath(filepath),
        "Readable": os.access(filepath, os.R_OK),
        "Writable": os.access(filepath, os.W_OK),
        "Executable": os.access(filepath, os.X_OK)
    }


def file_information():
    filepath = input("Enter your file name or path: ")

    if not os.path.isfile(filepath):
        print("Warning: File is missing!")
        return

    information = get_file_information(filepath)

    for key, value in information.items():
        print(f"{key}: {value}")


def sec_report():
    filepath = input("Enter your file name or path: ")

    if not os.path.isfile(filepath):
        print("Warning: File is missing!")
        return

    try:
        final_hash = calculate_sha256(filepath)
    except OSError:
        print("Unable to read the file.")
        return

    information = get_file_information(filepath)

    hash_file = filepath + ".hash"

    if os.path.isfile(hash_file):
        with open(hash_file, "r") as file:
            saved_hash = file.read().strip()

        if final_hash == saved_hash:
            integrity_status = "File is Unchanged"
        else:
            integrity_status = "WARNING: File has been modified."
    else:
        integrity_status = "No saved hash found. Run option 1 first."

    generated_time = datetime.datetime.now()

    report = ""
    report += "=" * 45 + "\n"
    report += "          SECURITY REPORT\n"
    report += "=" * 45 + "\n"
    report += f"Generated on: {generated_time}\n\n"

    for key, value in information.items():
        report += f"{key}: {value}\n"

    report += f"\nSHA-256 Hash: {final_hash}\n"
    report += f"\nIntegrity Status: {integrity_status}\n"
    report += "=" * 45 + "\n"

    print(report)

    report_name = "security_report_" + os.path.splitext(
        os.path.basename(filepath)
    )[0] + ".txt"

    with open(report_name, "w") as file:
        file.write(report)

    print(f"Report saved to: {report_name}")


def main():
    while True:
        show_menu()

        choice = input("Enter an option: ")

        if choice == "1":
            calculate_hash()

        elif choice == "2":
            check_integrity()

        elif choice == "3":
            file_information()

        elif choice == "4":
            sec_report()

        elif choice == "5":
            print("Exiting Security Toolkit...")
            break

        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()
