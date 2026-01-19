import sqlite3
import sys

def get_mysql_style_table(headers, data):
    # Calculate max width for each column
    col_widths = [len(h) for h in headers]
    for row in data:
        for i, value in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(value)))
    
    output = []
    
    # Create separator line
    separator = "+"
    for w in col_widths:
        separator += "-" * (w + 2) + "+"
    
    output.append(separator)
    
    # Print Headers
    header_line = "|"
    for i, h in enumerate(headers):
        header_line += f" {h:<{col_widths[i]}} |"
    output.append(header_line)
    output.append(separator)
    
    # Print Data
    for row in data:
        row_line = "|"
        for i, value in enumerate(row):
            row_line += f" {str(value):<{col_widths[i]}} |"
        output.append(row_line)
    
    output.append(separator)
    output.append(f"{len(data)} rows in set.")
    
    return "\n".join(output)

def view_users():
    try:
        conn = sqlite3.connect("college.db")
        cursor = conn.execute("SELECT * FROM users")
        
        headers = [description[0] for description in cursor.description]
        data = cursor.fetchall()
        
        table_string = get_mysql_style_table(headers, data)
        
        # Write to file
        with open("users_table_view.txt", "w", encoding="utf-8") as f:
            f.write("Database Export: users table\n")
            f.write(table_string)
            
        print(f"Successfully exported database view to: users_table_view.txt")
        print(table_string) # Also print to terminal
            
        conn.close()
    except Exception as e:
        print(f"Error reading database: {e}")

if __name__ == "__main__":
    view_users()
