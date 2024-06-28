import subprocess
import os
import pandas as pd
from termcolor import colored
from tabulate import tabulate
from datetime import datetime

def run_dig(server, domain, record_type):
    """
    Run the dig command to fetch DNS records from a specific server.

    Args:
        server (str): The nameserver to query.
        domain (str): The domain to query.
        record_type (str): The type of DNS record to query.

    Returns:
        list: A list of DNS records or an empty list if the command failed.
    """
    try:
        # Ensure the server, domain, and record_type arguments are not None
        if server is None or domain is None or record_type is None:
            raise ValueError("Server, domain, and record_type must not be None")

        # Run the dig command and capture the output
        result = subprocess.run(
            ["dig", f"@{server}", domain, record_type, "+short"],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )

        # If the command failed, return an empty list
        if result.returncode != 0:
            return []

        # Return the output as a list of records
        return result.stdout.strip().split("\n")
    except Exception as e:
        # If an error occurred, print the error message and return an empty list
        print(f"Error running dig: {e}")
        return []

def compare_records(domain, subdomains, current_ns, new_ns, record_types):
    """
    Compare DNS records between the current and new nameservers.

    Args:
        domain (str): The main domain.
        subdomains (list): A list of subdomains.
        current_ns (str): The current nameserver.
        new_ns (str): The new nameserver.
        record_types (list): A list of DNS record types.

    Returns:
        list: A list of dictionaries containing the comparison results.
    """
    # Initialize the comparison data list
    comparison_data = []

    # Check if the domain, current_ns, and new_ns are not None
    if not domain or not current_ns or not new_ns:
        raise ValueError("Domain, current_ns, and new_ns must not be None")

    # Include the main domain in the list of subdomains
    all_domains = [domain] + subdomains

    # Iterate over each subdomain and record type
    for subdomain in all_domains:
        # Construct the full domain name
        full_domain = f"{subdomain}.{domain}" if subdomain != domain else domain
        for record_type in record_types:
            # Fetch records from both nameservers
            try:
                current_records = run_dig(current_ns, full_domain, record_type)
                new_records = run_dig(new_ns, full_domain, record_type)
            except Exception as e:
                print(f"Error fetching records: {e}")
                continue

            # Ensure both lists have the same length
            max_len = max(len(current_records), len(new_records))
            current_records += [""] * (max_len - len(current_records))
            new_records += [""] * (max_len - len(new_records))

            # Compare records and store the result
            for cur, new in zip(current_records, new_records):
                status = cur == new
                comparison_data.append({
                    "Subdomain": full_domain,  # Subdomain
                    "Record Type": record_type,  # Record type
                    "Current Records": cur,  # Current records
                    "New Records": new,  # New records
                    "Status": "Identical" if status else "Different"  # Status
                })

    return comparison_data

def display_comparison_table(comparison_data):
    """
    Display the comparison results in a color-coded table.

    Args:
        comparison_data (list): A list of dictionaries containing the comparison results.
    """
    # Prepare table data with color-coded status
    table_data = []
    headers = ["Subdomain", "Record Type", "Current Records", "New Records", "Status"]

    # Iterate over each row in comparison data
    for row in comparison_data:
        # Check if the required fields exist in the row dictionary
        if not all(key in row for key in ["Subdomain", "Record Type", "Current Records", "New Records", "Status"]):
            raise ValueError("Comparison data row is missing required fields")

        # Determine the color based on the status
        color = "green" if row["Status"] == "Identical" else "red"

        # Append a row to the table data with colored fields
        table_data.append([
            row["Subdomain"],
            row["Record Type"],
            colored(row.get("Current Records", ""), color),
            colored(row.get("New Records", ""), color),
            colored(row.get("Status", ""), color)
        ])

    # Print the table
    # The tablefmt="grid" argument specifies a grid-like table format
    print(tabulate(table_data, headers, tablefmt="grid"))

def export_to_csv(comparison_data):
    """
    Export the comparison results to a CSV file with a timestamp.

    Args:
        comparison_data (list): A list of dictionaries containing the comparison results.
    """
    try:
        # Ensure the logs directory exists
        os.makedirs("logs", exist_ok=True)
        
        # Convert the comparison data to a DataFrame
        df = pd.DataFrame(comparison_data)
        
        # Generate a timestamp for the filename
        timestamp = datetime.now().strftime("%d-%m-%Y-%H%M%S")
        
        # Construct the filename with the timestamp
        filename = f"logs/dns_comparison_{timestamp}.csv"
        
        # Write the DataFrame to the CSV file
        df.to_csv(filename, index=False)
        
        # Print a message indicating the exported file location
        print(f"\nComparison results exported to {filename}")
    except Exception as e:
        # If an error occurred, print the error message
        print(f"\nError exporting to CSV: {e}")

def main():
    """
    Main function to prompt user input and compare DNS records.
    """
    # Prompt user for domain and subdomains to check
    domain = input("Enter the domain to check: ")
    if not domain:
        raise ValueError("Domain must not be empty")

    subdomains_input = input("Enter subdomains to check (comma-separated, e.g., 'www,mail'): ")
    subdomains = subdomains_input.split(",") if subdomains_input else []
    
    # Prompt user for current and new nameservers
    current_ns = input("Enter the current nameserver: ")
    if not current_ns:
        raise ValueError("Current nameserver must not be empty")

    new_ns = input("Enter the new nameserver: ")
    if not new_ns:
        raise ValueError("New nameserver must not be empty")
    
    # Define the DNS record types to check
    record_types = ["A", "MX", "CNAME", "TXT", "NS"]

    # Print information about the comparison being performed
    print(f"\nComparing DNS records for {domain} and its subdomains between {current_ns} and {new_ns}...\n")

    # Compare DNS records and obtain the comparison data
    comparison_data = compare_records(domain, subdomains, current_ns, new_ns, record_types)
    
    # Display the comparison results in a formatted table
    display_comparison_table(comparison_data)
    
    # Export the comparison results to a CSV file
    export_to_csv(comparison_data)

if __name__ == "__main__":
    main()