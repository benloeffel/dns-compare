# DNS Comparison Tool

This Python script compares DNS records between two nameservers and highlights the differences.

## Features

- Compares DNS records for a domain and its subdomains.
- Supports various DNS record types (A, MX, CNAME, TXT, NS).
- Outputs results in a neatly formatted, color-coded table.
- Exports comparison results to a CSV file with a timestamped filename saved in the `logs` directory.

## Prerequisites

- Python 3.6+
- `pip` package installer

## Installation

1. Clone the repository or download the script.
2. Navigate to the project directory.
3. Set up a virtual environment:

    ```sh
    python3 -m venv venv
    source venv/bin/activate  # On Windows use: venv\Scripts\activate
    ```

4. Install the required packages:

    ```sh
    pip install pandas termcolor tabulate
    ```

## Usage

1. Activate the virtual environment:

    ```sh
    source venv/bin/activate  # On Windows use: venv\Scripts\activate
    ```

2. Run the script:

    ```sh
    python dns_compare.py
    ```

3. Follow the prompts:

    ```
    Enter the domain to check: example.com
    Enter subdomains to check (comma-separated, e.g., 'www,mail'): www,api
    Enter the current nameserver: ns1.currentprovider.com
    Enter the new nameserver: ns1.newprovider.com
    ```

4. View the comparison results in the terminal.

5. Check the `logs` directory for the exported CSV file with the comparison results.

## Example

```sh
python dns_compare.py

Enter the domain to check: example.com
Enter subdomains to check (comma-separated, e.g., 'www,mail'): www,api
Enter the current nameserver: ns1.currentprovider.com
Enter the new nameserver: ns1.newprovider.com

Comparing DNS records for example.com and its subdomains between ns1.currentprovider.com and ns1.newprovider.com...

+---------------+-------------+-------------------+-------------------+-----------+
| Subdomain     | Record Type | Current Records   | New Records       | Status    |
+===============+=============+===================+===================+===========+
| example.com   | A           | 192.0.2.1         | 192.0.2.1         | Identical |
+---------------+-------------+-------------------+-------------------+-----------+
| www.example.com | A         | 192.0.2.2         | 198.51.100.1      | Different |
+---------------+-------------+-------------------+-------------------+-----------+
| api.example.com | A         | 192.0.2.3         | 192.0.2.3         | Identical |
+---------------+-------------+-------------------+-------------------+-----------+

Comparison results exported to logs/dns_comparison_28-06-2024-150101.csv