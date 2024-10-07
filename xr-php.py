import argparse
import subprocess
import os
import re


def main():
    parser = argparse.ArgumentParser(
        description="PHP version manager by FFXHORA, Slebew!"
    )

    # Hide the default -h option
    parser.add_argument("--no-help", action="store_true", help=argparse.SUPPRESS)
    parser.add_argument("-v", action="store_true", help="Check current PHP version")

    # Create a subparser for the 'use' command
    subparsers = parser.add_subparsers(dest="command")
    use_parser = subparsers.add_parser("use", help="Switch to a specified PHP version")
    use_parser.add_argument("version", type=str, help="The PHP version to use")

    # Parse the arguments
    args = parser.parse_args()

    # Handle different commands
    if args.v:
        check_php_version()
    elif args.command == "use":
        use_php_version(args.version)
        check_php_version()
    else:
        defaultOutput()


def defaultOutput():
    print("PHP version manager by FFXHORA, Slebew!")
    print("\nCall command like this:")
    print("xr-php <command>")
    print("\nAvailable commands:")
    print("-v : Check current PHP version")
    print("use <version> : Switch to a specified PHP version")


def check_php_version():
    php_path = "C:/xampp/php/php.exe"
    if os.path.exists(php_path):
        try:
            # Execute PHP command to get the version
            result = subprocess.run([php_path, "-v"], capture_output=True, text=True)
            version = extract_php_version(result.stdout)
            print(f"Current PHP Version: {version}")
        except Exception as e:
            print(f"Error checking PHP version: {e}")
    else:
        print(
            f"PHP executable not found at {php_path}. Please check your XAMPP installation."
        )


def extract_php_version(output):
    # Extract the version number from the output string
    match = re.search(r"PHP (\d+\.\d+\.\d+)", output)
    return match.group(1) if match else "Unknown version"


def end_task(process_path):
    """End a task by its executable path."""
    try:
        taskkill_command = f"taskkill /F /IM {os.path.basename(process_path)}"
        subprocess.run(taskkill_command, shell=True, capture_output=True, text=True)
        print(f"Ended task: {os.path.basename(process_path)}")
    except Exception as e:
        print(f"Error ending task {process_path}: {e}")


def use_php_version(version):
    unaliased_version = ""
    if version == "8":
        unaliased_version = "8.2.4"
    elif version == "7.4" or version == "7-4" or version == "74":
        unaliased_version = "7.4.33"
    elif version == "7.3" or version == "7-3" or version == "73":
        unaliased_version = "7.3.33"
    elif version == "5":
        unaliased_version = "5.3.8"
    else:
        print(f"We can't find the version that you looking for")
        print(f"\nAvaiable versions : ")
        print(f"• 8 (for 8.2.4)")
        print(f"• 7.4 (for 7.4.33)")
        print(f"• 7.3 (for 7.3.33)")
        print(f"• 5 (for 5.3.8)")
        print("")
        return None

    # Get the current PHP version
    current_php_version = check_php_version_and_get_current()

    if unaliased_version == current_php_version:
        print(f"you are now using php {unaliased_version}")

    # End tasks for Apache, MySQL, and PostgreSQL
    end_task("C:/xampp/xampp-control.exe")
    end_task("C:/xampp/apache/bin/httpd.exe")
    end_task("C:/Program Files/PostgreSQL/15/bin/postgres.exe")
    end_task("C:/xampp/mysql/bin/mysqld.exe")
    end_task("C:/Program Files/PostgreSQL/15/bin/pg_ctl.exe")

    # Rename folder C:\xampp to C:\xampp-<current_version>
    xampp_path = "C:/xampp"
    if os.path.exists(xampp_path):
        try:
            new_xampp_path = f"{xampp_path}-{current_php_version}"
            os.rename(xampp_path, new_xampp_path)
            print(f"Renamed {xampp_path} to {new_xampp_path}")
        except Exception as e:
            print(f"Failed to rename folder, {e}")

        # Rename folder C:\xampp-<version> to C:\xampp
        old_xampp_version_path = f"{xampp_path}-{unaliased_version}"
        if os.path.exists(old_xampp_version_path):
            try:
                os.rename(old_xampp_version_path, xampp_path)
                print(
                    f"Switched to PHP version {unaliased_version}. Renamed {old_xampp_version_path} to {xampp_path}"
                )
            except Exception as e:
                print(f"Failed to rename folder, {e}")
                os.rename(new_xampp_path, xampp_path)
        else:
            print(f"Version folder {old_xampp_version_path} does not exist.")
    else:
        print(f"XAMPP directory does not exist at {xampp_path}.")


def check_php_version_and_get_current():
    php_path = "C:/xampp/php/php.exe"
    if os.path.exists(php_path):
        try:
            # Execute PHP command to get the version
            result = subprocess.run([php_path, "-v"], capture_output=True, text=True)
            return extract_php_version(result.stdout)
        except Exception as e:
            print(f"Error checking PHP version: {e}")
    return "Unknown version"


if __name__ == "__main__":
    main()
