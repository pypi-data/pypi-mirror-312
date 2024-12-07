import fitz  # PyMuPDF


def extract_text_by_sections(pdf_path):
    # Open the PDF file
    document = fitz.open(pdf_path)

    # A list to hold the sections
    sections = []
    current_section = []
    current_font_size = None
    current_font_style = None

    # Loop through each page in the PDF
    for page_num in range(len(document)):
        page = document.load_page(page_num)  # Get the page
        blocks = page.get_text("dict")["blocks"]  # Extract text as blocks (with font info)

        for block in blocks:
            if block['type'] == 0:  # This is a text block (ignore images, etc.)
                for line in block["lines"]:
                    for span in line["spans"]:
                        text = span["text"]
                        font_size = span["size"]
                        font_style = span["font"]

                        # If the font size or style changes, save the current section
                        if current_font_size is not None and (
                                font_size != current_font_size or font_style != current_font_style):
                            sections.append("".join(current_section))
                            current_section = []  # Start a new section

                        # Add the text to the current section
                        current_section.append(text)

                        # Update the current font properties
                        current_font_size = font_size
                        current_font_style = font_style

        # Append the last section after the loop
        if current_section:
            sections.append("".join(current_section))

    # Close the document
    document.close()

    return sections


# Path to the PDF file
pdf_path = r"C:\Users\lucas\Desktop\BDD_Helico\Owners Manuel Fama Kiss.pdf"

# Extract the sections from the PDF
sections = extract_text_by_sections(pdf_path)

# Print the extracted sections
for i, section in enumerate(sections):
    print(f"Section {i + 1}:\n{section[:500]}...\n")  # Print the first 500 characters of each section

# import functions_DatasetGeneration
#
# # Load the document
# txt_path = r"C:\Users\lucas\Desktop\BDD_Helico\Owners Manuel Fama Kiss.txt"
# document = functions_DatasetGeneration.load_txt_file(txt_path)
#
# from chonkie import SemanticChunker
#
# from chonkie import SemanticChunker
# from chonkie.embeddings import BaseEmbeddings
#
# model_name = r"C:\Users\lucas\aait_store\Models\NLP\all-mpnet-base-v2"
# model = model_name
# chunker = SemanticChunker(
#     embedding_model=model,  # Default model
#     similarity_threshold=0.3,  # Similarity threshold (0-1)
#     chunk_size=1024,  # Maximum tokens per chunk
#     initial_sentences=5  # Initial sentences per chunk
# )
#
# chunks = chunker.chunk(document)
# chunks1=[]
# for chunk in chunks:
#     chunks1.append(chunk.text)
#
# for c in chunks1:
#     print("\n\nCHUNK------:", c)
#
