import time, os

class FileHandler:
    @classmethod
    def readText(self, filename):
        with open(filename, "r") as file:
            return file.read()

    @classmethod
    def writeText(self, filename, content):
        try:
            with open(filename, "x") as file:
                file.write(content)
        except FileExistsError:
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            new_filename = f"{os.path.splitext(filename)[0]}_{timestamp}{os.path.splitext(filename)[1]}"
            with open(new_filename, "x") as file:
                file.write(content)
            print(f"The file '{new_filename}' was created successfully.")
        else:
            print(f"The file '{filename}' was created successfully.")

    @classmethod
    def writeFullTranscript(self, filename, full_transcript):
        try:
            with open(filename, "x") as file:
                for line in full_transcript:
                    file.write(line["role"] + ": " + line["content"] + "\n")
        except FileExistsError:
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            new_filename = f"{os.path.splitext(filename)[0]}_{timestamp}{os.path.splitext(filename)[1]}"
            with open(new_filename, "x") as file:
                for line in full_transcript:
                    file.write(line["role"] + ": " + line["content"] + "\n")
            print(f"The file '{new_filename}' was created successfully.")
        else:
            print(f"The file '{filename}' was created successfully.")