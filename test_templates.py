import os

# Create the templates directory if it doesn't exist
os.makedirs("templates", exist_ok=True)

# Open and write a simple test template
with open("templates/index.html", "w") as f:
    f.write("""
<!DOCTYPE html>
<html>
<head>
    <title>Test Template</title>
</head>
<body>
    <h1>Test Template</h1>
    <p>This is a test template.</p>
</body>
</html>
    """)

print("Template created successfully at:", os.path.abspath("templates/index.html"))