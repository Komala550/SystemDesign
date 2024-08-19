class SimpleTextEditor:
    def __init__(self):
        self.text = ""
        self.history = []

    def add_text(self, new_text):
        self.history.append(self.text)
        self.text += new_text

    def delete_text(self, num_chars):
        self.history.append(self.text)
        self.text = self.text[:-num_chars]

    def undo(self):
        if self.history:
            self.text = self.history.pop()

    def __str__(self):
        return self.text

# Example usage
editor = SimpleTextEditor()
editor.add_text("Hello, ")
editor.add_text("world!")
print(editor)  # Output: Hello, world!
editor.delete_text(6)
print(editor)  # Output: Hello,
editor.undo()
print(editor)  # Output: Hello, world!
