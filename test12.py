import re
import PyPDF2
import tkinter as tk
from tkinter import scrolledtext
import webbrowser

def search_schemes(pdf_file, keyword):
    schemes = []
    with open(pdf_file, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page_number in range(len(reader.pages)):
            page = reader.pages[page_number]
            text = page.extract_text()
            # Remove unwanted text
            text = text.replace("Downloaded from InstaPDF.in", "")
            text = text.replace("Take free IBPS Clerk Mock here: https://cracku.in/banking/ibps-clerk-mocks", "")
            text = text.replace("cracku.in Take Free Mock for IBPS PO here : -prelims -mocks", "")
            # Remove URLs using regex
            text = re.sub(r'\bhttps?://\S+\b', '', text)
            if keyword.lower() in text.lower():
                schemes.append(text.strip())
    return schemes

def search():
    keyword = entry.get()
    result1 = search_schemes('instapdf.in-all-indian-government-schemes-list-463.pdf', keyword)
    result2 = search_schemes('List of all schemes of Indian government pdf.pdf', keyword)
    result = result1 + result2
    if result:
        output.delete('1.0', tk.END)
        output.insert(tk.END, "Matching Government Schemes:\n\n")
        for idx, scheme in enumerate(result, start=1):
            # Strip prefix from the scheme
            scheme = re.sub(r'^\d+\s*/\s*\d+\s*', '', scheme)
            # Strip additional prefix if present
            scheme = re.sub(r'^cracku\.in\s+Take\s+Free\s+Mock\s+for\s+IBPS\s+PO\s+here\s*:\s*[-–]*\s*prelims\s*[-–]*\s*mocks\s*', '', scheme)
            link = f"https://www.google.com/search?q={'+'.join(scheme.split())}"
            output.insert(tk.END, f"{idx}. ")
            output.insert(tk.END, f"{scheme}\n")
            output.tag_add("link", f"{output.index(tk.END)} -{len(scheme) + 1}c", f"{output.index(tk.END)}")
            output.tag_config("link", foreground="blue", underline=True)
            output.tag_bind("link", "<Button-1>", lambda e, link=link: webbrowser.open_new(link))
    else:
        output.delete('1.0', tk.END)
        output.insert(tk.END, "No matching government schemes found.")

# Create main application window
root = tk.Tk()
root.title("Government Schemes Search")

# Create input label and entry
label = tk.Label(root, text="Enter a keyword to search for government schemes:")
label.pack(pady=5)
entry = tk.Entry(root, width=50)
entry.pack(pady=5)

# Create search button
search_button = tk.Button(root, text="Search", command=search)
search_button.pack(pady=5)

# Create scrolled text widget for output
output = scrolledtext.ScrolledText(root, width=80, height=20, wrap=tk.WORD)
output.pack(pady=5)

# Run the application
root.mainloop()
