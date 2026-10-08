import secrets
import string
import tkinter as tk
from tkinter import ttk, messagebox


class PasswordGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Secure Password Generator")
        self.root.geometry("650x520")
        self.root.resizable(False, False)
        self.root.configure(bg="#f4f6f8")

        self.create_variables()
        self.create_interface()

    def create_variables(self):
        self.length_variable = tk.StringVar(value="12")
        self.password_variable = tk.StringVar()
        self.status_variable = tk.StringVar(
            value="Select your options and generate a password."
        )

        self.uppercase_variable = tk.BooleanVar(value=True)
        self.lowercase_variable = tk.BooleanVar(value=True)
        self.numbers_variable = tk.BooleanVar(value=True)
        self.symbols_variable = tk.BooleanVar(value=True)

    def create_interface(self):
        main_frame = ttk.Frame(self.root, padding=25)
        main_frame.pack(fill="both", expand=True)

        self.create_header(main_frame)
        self.create_password_display(main_frame)
        self.create_length_section(main_frame)
        self.create_options_section(main_frame)
        self.create_buttons(main_frame)
        self.create_status_section(main_frame)

    def create_header(self, parent):
        title_label = ttk.Label(
            parent,
            text="PASSWORD GENERATOR",
            font=("Arial", 24, "bold")
        )
        title_label.pack(pady=(0, 5))

        subtitle_label = ttk.Label(
            parent,
            text="Create strong and secure random passwords",
            font=("Arial", 11)
        )
        subtitle_label.pack(pady=(0, 20))

    def create_password_display(self, parent):
        display_frame = ttk.LabelFrame(
            parent,
            text="Generated Password",
            padding=12
        )
        display_frame.pack(fill="x", pady=8)

        self.password_entry = ttk.Entry(
            display_frame,
            textvariable=self.password_variable,
            font=("Consolas", 15),
            justify="center",
            state="readonly"
        )
        self.password_entry.pack(fill="x")

    def create_length_section(self, parent):
        length_frame = ttk.LabelFrame(
            parent,
            text="Password Length",
            padding=12
        )
        length_frame.pack(fill="x", pady=8)

        ttk.Label(
            length_frame,
            text="Enter length:"
        ).pack(side="left", padx=(0, 10))

        self.length_entry = ttk.Entry(
            length_frame,
            textvariable=self.length_variable,
            width=10
        )
        self.length_entry.pack(side="left")

        ttk.Label(
            length_frame,
            text="Recommended length: 12 or more characters"
        ).pack(side="left", padx=15)

    def create_options_section(self, parent):
        options_frame = ttk.LabelFrame(
            parent,
            text="Character Options",
            padding=12
        )
        options_frame.pack(fill="x", pady=8)

        ttk.Checkbutton(
            options_frame,
            text="Uppercase letters: A-Z",
            variable=self.uppercase_variable
        ).grid(row=0, column=0, sticky="w", padx=10, pady=5)

        ttk.Checkbutton(
            options_frame,
            text="Lowercase letters: a-z",
            variable=self.lowercase_variable
        ).grid(row=0, column=1, sticky="w", padx=10, pady=5)

        ttk.Checkbutton(
            options_frame,
            text="Numbers: 0-9",
            variable=self.numbers_variable
        ).grid(row=1, column=0, sticky="w", padx=10, pady=5)

        ttk.Checkbutton(
            options_frame,
            text="Special symbols: !@#$%",
            variable=self.symbols_variable
        ).grid(row=1, column=1, sticky="w", padx=10, pady=5)

    def create_buttons(self, parent):
        button_frame = ttk.Frame(parent)
        button_frame.pack(pady=18)

        ttk.Button(
            button_frame,
            text="Generate Password",
            command=self.generate_password
        ).pack(side="left", padx=5)

        ttk.Button(
            button_frame,
            text="Copy Password",
            command=self.copy_password
        ).pack(side="left", padx=5)

        ttk.Button(
            button_frame,
            text="Clear",
            command=self.clear_password
        ).pack(side="left", padx=5)

    def create_status_section(self, parent):
        status_label = ttk.Label(
            parent,
            textvariable=self.status_variable,
            font=("Arial", 10)
        )
        status_label.pack(pady=8)

    def get_selected_character_groups(self):
        character_groups = []

        if self.uppercase_variable.get():
            character_groups.append(string.ascii_uppercase)

        if self.lowercase_variable.get():
            character_groups.append(string.ascii_lowercase)

        if self.numbers_variable.get():
            character_groups.append(string.digits)

        if self.symbols_variable.get():
            character_groups.append("!@#$%^&*()-_=+[]{};:,.?/")

        return character_groups

    def validate_input(self, length, character_groups):
        if not length.isdigit():
            messagebox.showerror(
                "Invalid Length",
                "Please enter a valid whole number."
            )
            return False

        length = int(length)

        if length < 4:
            messagebox.showerror(
                "Invalid Length",
                "Password length must be at least 4 characters."
            )
            return False

        if length > 128:
            messagebox.showerror(
                "Invalid Length",
                "Password length cannot be greater than 128 characters."
            )
            return False

        if not character_groups:
            messagebox.showerror(
                "No Character Type Selected",
                "Select at least one character type."
            )
            return False

        if length < len(character_groups):
            messagebox.showerror(
                "Length Too Short",
                "Password length must be at least equal to the number "
                "of selected character types."
            )
            return False

        return True

    def generate_password(self):
        length_text = self.length_variable.get().strip()
        character_groups = self.get_selected_character_groups()

        if not self.validate_input(length_text, character_groups):
            return

        length = int(length_text)

        password_characters = []

        # Add at least one character from every selected group.
        for group in character_groups:
            password_characters.append(secrets.choice(group))

        # Create one combined pool for the remaining characters.
        character_pool = "".join(character_groups)

        remaining_length = length - len(password_characters)

        for _ in range(remaining_length):
            password_characters.append(
                secrets.choice(character_pool)
            )

        # Securely shuffle the final password characters.
        secrets.SystemRandom().shuffle(password_characters)

        password = "".join(password_characters)

        self.password_variable.set(password)
        self.status_variable.set(
            f"Password generated successfully. Strength: "
            f"{self.calculate_strength(password)}"
        )

    def calculate_strength(self, password):
        score = 0

        if len(password) >= 8:
            score += 1

        if len(password) >= 12:
            score += 1

        if any(character.isupper() for character in password):
            score += 1

        if any(character.islower() for character in password):
            score += 1

        if any(character.isdigit() for character in password):
            score += 1

        if any(not character.isalnum() for character in password):
            score += 1

        if score <= 2:
            return "Weak"
        elif score <= 4:
            return "Medium"
        else:
            return "Strong"

    def copy_password(self):
        password = self.password_variable.get()

        if not password:
            messagebox.showwarning(
                "No Password",
                "Generate a password before copying it."
            )
            return

        self.root.clipboard_clear()
        self.root.clipboard_append(password)
        self.root.update()

        self.status_variable.set(
            "Password copied to the clipboard."
        )

    def clear_password(self):
        self.password_variable.set("")
        self.status_variable.set(
            "Select your options and generate a password."
        )


def main():
    root = tk.Tk()
    PasswordGeneratorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()