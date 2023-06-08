def generate_markdown_table(headers, data):
    # Generate the table header
    table = "| " + " | ".join(headers) + " |\n"

    # Generate the table separator
    separator = "| " + " | ".join(["---" for _ in headers]) + " |\n"

    # Generate the table rows
    rows = ""
    for row in data:
        row_str = "| " + " | ".join(str(cell) for cell in row) + " |\n"
        rows += row_str

    # Combine the header, separator, and rows
    markdown_table = table + separator + rows

    return markdown_table


# if __name__ == '__main__':
#     headers = ["Name", "Age", "Email"]
#     data = [
#         ["Alice", 25, "alice@example.com"],
#         ["Bob", 30, "bob@example.com"],
#         ["Charlie", 35, "charlie@example.com"]
#     ]
#
#     markdown_table = generate_markdown_table(headers, data)
#     print(markdown_table)
