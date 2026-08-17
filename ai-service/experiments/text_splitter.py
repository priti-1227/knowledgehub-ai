from langchain_text_splitters import RecursiveCharacterTextSplitter


text = """
Work From Home Policy

Employees are allowed to work from home up to three days per week.
Employees must obtain approval from their reporting manager before
working remotely.

Employees working from home must remain available during normal
working hours. They must attend all required meetings and maintain
regular communication with their team.

The company may require employees to work from the office when
business requirements demand it.

Leave Policy

Employees receive casual leave, sick leave, and earned leave according
to the company's leave policy. Leave requests must be submitted through
the employee portal and approved by the reporting manager.
"""


# Create the text splitter
splitter = RecursiveCharacterTextSplitter(
    chunk_size=300,
    chunk_overlap=50,
)

# Split the document
chunks = splitter.split_text(text)


# Display the chunks
print("TOTAL CHUNKS:", len(chunks))

for i, chunk in enumerate(chunks):
    print("\n" + "=" * 60)
    print(f"CHUNK {i + 1}")
    print("=" * 60)
    print(chunk)
    print(f"\nCHUNK LENGTH: {len(chunk)} characters")