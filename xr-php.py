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
        process_name = os.path.basename(process_path)
        taskkill_command = f"taskkill /F /IM {process_name}"
        result = subprocess.run(taskkill_command, shell=True, capture_output=True, text=True)
        
        # Only print if the process was actually killed (not if it wasn't running)
        if result.returncode == 0:
            print(f"Stopped: {process_name}")
        # Don't print error if process wasn't running (common case)
        
    except Exception as e:
        # Only print if there's an actual error, not if process wasn't running
        pass


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
        print(f"You are already using PHP {unaliased_version}")
        return

    # Rename folder C:\xampp to C:\xampp-<current_version>
    xampp_path = "C:/xampp"
    if not os.path.exists(xampp_path):
        print(f"XAMPP directory does not exist at {xampp_path}.")
        return

    # End tasks for Apache, MySQL, PostgreSQL, Fork, and FileZilla
    print("Stopping XAMPP services...")
    end_task("C:/xampp/xampp-control.exe")
    end_task("C:/xampp/apache/bin/httpd.exe")
    end_task("C:/xampp/mysql/bin/mysqld.exe")
    end_task("C:/xampp/FileZillaFTP/FileZillaServer.exe")
    end_task("C:/Users/fadly/AppData/Local/Fork/current/Fork.exe")

    # Wait a bit for processes to fully terminate
    import time
    time.sleep(2)

    new_xampp_path = f"{xampp_path}-{current_php_version}"
    old_xampp_version_path = f"{xampp_path}-{unaliased_version}"

    # Check if target version folder exists
    if not os.path.exists(old_xampp_version_path):
        print(f"Version folder {old_xampp_version_path} does not exist.")
        return

    # Check if backup folder already exists and remove it if necessary
    if os.path.exists(new_xampp_path):
        print(f"Backup folder {new_xampp_path} already exists, removing it...")
        try:
            import shutil
            shutil.rmtree(new_xampp_path)
        except Exception as e:
            print(f"Failed to remove existing backup folder: {e}")
            return

    # Step 1: Rename current xampp to backup
    try:
        os.rename(xampp_path, new_xampp_path)
        print(f"Backed up current XAMPP: {xampp_path} -> {new_xampp_path}")
    except Exception as e:
        print(f"Failed to backup current XAMPP folder: {e}")
        return

    # Step 2: Rename target version to xampp
    try:
        os.rename(old_xampp_version_path, xampp_path)
        print(f"Switched to PHP version {unaliased_version}: {old_xampp_version_path} -> {xampp_path}")
    except Exception as e:
        print(f"Failed to switch to new version: {e}")
        # Rollback: restore original xampp folder
        try:
            os.rename(new_xampp_path, xampp_path)
            print("Rollback successful: restored original XAMPP folder")
        except Exception as rollback_error:
            print(f"CRITICAL: Rollback failed! {rollback_error}")
            print("Please manually rename folders to restore XAMPP")
        return

    # Start tasks for Apache, MySQL, PostgreSQL, Fork, and FileZilla
    print("Starting XAMPP control panel...")
    try:
        subprocess.Popen(["C:/xampp/xampp-control.exe"])
        subprocess.Popen(["C:/Users/fadly/AppData/Local/Fork/current/Fork.exe"])
    except Exception as e:
        print(f"Failed to start applications: {e}")


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
