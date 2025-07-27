import os

output_dir = "output/"  # or your custom path
print(f"Checking for files in: {os.path.abspath(output_dir)}")

if not os.path.exists(output_dir):
    print(f"Error: Directory not found: {output_dir}")
elif not os.listdir(output_dir):
    print(f"Error: Directory is empty: {output_dir}")
else:
    print("Files found:", os.listdir(output_dir))
    # Rest of your processing code