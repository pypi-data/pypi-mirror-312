def display_code():
    code_snippet = """
    def greet():
        print("Hello, World!")
    
    if __name__ == "__main__":
        greet()
    """
    print("Here is an example code snippet:")
    print(code_snippet)

def main():
    print("Ask 'how to make it?' to see an example.")
    question = input("Your question: ")
    if "how to make it" in question.lower():
        display_code()
    else:
        print("I don't understand the question. Try asking 'how to make it?'")
