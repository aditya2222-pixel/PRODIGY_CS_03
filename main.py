import hashlib
import random
import string
import urllib.request
import tkinter as tk
from tkinter import messagebox, ttk


class PasswordCheckerGUI:

    def __init__(self, root):
        self.root = root
        self.root.title("Password Complexity & Breach Checker")
        self.root.geometry("500x530")
        self.root.resizable(False, False)

        self.hibp_api_url = "https://api.pwnedpasswords.com/range/"
        self.show_password = False  # Track password visibility state
        self._build_ui()

    def _build_ui(self):
        # 1. Password Input Section
        input_frame = tk.Frame(self.root, pady=10)
        input_frame.pack(padx=20, fill=tk.X)

        tk.Label(
            input_frame,
            text="Enter Password:",
            font=("Arial", 10, "bold"),
        ).pack(anchor=tk.W)

        # Container for entry and toggle button
        entry_container = tk.Frame(input_frame)
        entry_container.pack(fill=tk.X, pady=5)

        self.entry_pass = tk.Entry(
            entry_container, show="*", font=("Arial", 11)
        )
        self.entry_pass.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.entry_pass.bind("<KeyRelease>", self.evaluate_strength)

        # Eye Toggle Button
        self.btn_eye = tk.Button(
            entry_container,
            text="👁",
            font=("Arial", 10),
            width=3,
            command=self.toggle_password_visibility,
            relief=tk.FLAT,
            cursor="hand2",
        )
        self.btn_eye.pack(side=tk.RIGHT, padx=(5, 0))

        # 2. Overall Strength Banner
        self.lbl_strength = tk.Label(
            self.root,
            text="Strength: WEAK",
            font=("Arial", 12, "bold"),
            fg="red",
        )
        self.lbl_strength.pack(pady=5)

        # 3. Complexity Criteria Checklist
        criteria_frame = tk.LabelFrame(
            self.root, text="Complexity Criteria", font=("Arial", 10, "bold")
        )
        criteria_frame.pack(padx=20, pady=5, fill=tk.X)

        self.var_len = tk.BooleanVar()
        self.var_upper = tk.BooleanVar()
        self.var_lower = tk.BooleanVar()
        self.var_num = tk.BooleanVar()
        self.var_spec = tk.BooleanVar()

        tk.Checkbutton(
            criteria_frame,
            text="At least 8 characters",
            variable=self.var_len,
            state="disabled",
        ).pack(anchor=tk.W, padx=10, pady=2)
        tk.Checkbutton(
            criteria_frame,
            text="Uppercase letter (A-Z)",
            variable=self.var_upper,
            state="disabled",
        ).pack(anchor=tk.W, padx=10, pady=2)
        tk.Checkbutton(
            criteria_frame,
            text="Lowercase letter (a-z)",
            variable=self.var_lower,
            state="disabled",
        ).pack(anchor=tk.W, padx=10, pady=2)
        tk.Checkbutton(
            criteria_frame,
            text="Number (0-9)",
            variable=self.var_num,
            state="disabled",
        ).pack(anchor=tk.W, padx=10, pady=2)
        tk.Checkbutton(
            criteria_frame,
            text="Special character (!@#$%^&*)",
            variable=self.var_spec,
            state="disabled",
        ).pack(anchor=tk.W, padx=10, pady=2)

        # 4. HIBP Status Display
        self.lbl_hibp = tk.Label(
            self.root,
            text="HIBP: Not checked yet",
            font=("Arial", 10, "italic"),
            fg="gray",
        )
        self.lbl_hibp.pack(pady=10)

        # 5. Control Buttons
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=5)

        tk.Button(
            btn_frame,
            text="Check Password",
            command=self.check_breach,
            bg="#2196F3",
            fg="white",
            font=("Arial", 9, "bold"),
            width=18,
        ).pack(side=tk.LEFT, padx=5)
        tk.Button(
            btn_frame,
            text="Generate Password",
            command=self.generate_password,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 9, "bold"),
            width=18,
        ).pack(side=tk.LEFT, padx=5)

        # 6. Suggested Password Field
        sug_frame = tk.Frame(self.root, pady=10)
        sug_frame.pack(padx=20, fill=tk.X)

        tk.Label(
            sug_frame, text="Suggested Password:", font=("Arial", 10)
        ).pack(anchor=tk.W)
        self.entry_sug = tk.Entry(
            sug_frame, font=("Consolas", 11), width=45, fg="blue"
        )
        self.entry_sug.pack(fill=tk.X, pady=5)

    def toggle_password_visibility(self):
        self.show_password = not self.show_password
        if self.show_password:
            self.entry_pass.config(show="")
            self.btn_eye.config(text="🙈")  # Switch icon when visible
        else:
            self.entry_pass.config(show="*")
            self.btn_eye.config(text="👁")  # Switch icon when hidden

    def evaluate_strength(self, event=None):
        password = self.entry_pass.get()

        # Check conditions
        has_len = len(password) >= 8
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_num = any(c.isdigit() for c in password)
        has_spec = any(c in string.punctuation for c in password)

        # Update Checkbox UI
        self.var_len.set(has_len)
        self.var_upper.set(has_upper)
        self.var_lower.set(has_lower)
        self.var_num.set(has_num)
        self.var_spec.set(has_spec)

        # Overall rating calculation
        score = sum([has_len, has_upper, has_lower, has_num, has_spec])

        if score <= 2:
            self.lbl_strength.config(text="Strength: WEAK", fg="red")
        elif score <= 4:
            self.lbl_strength.config(text="Strength: MODERATE", fg="#FF8C00")
        else:
            self.lbl_strength.config(text="Strength: STRONG", fg="green")

    def check_breach(self):
        password = self.entry_pass.get()
        if not password:
            messagebox.showwarning("Warning", "Please enter a password first!")
            return

        self.lbl_hibp.config(text="HIBP: Querying API...", fg="black")
        self.root.update_idletasks()

        # Step 1: Local SHA-1 hashing
        sha1_hash = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()
        prefix, suffix = sha1_hash[:5], sha1_hash[5:]

        # Step 2: k-Anonymity API Lookup
        try:
            url = f"{self.hibp_api_url}{prefix}"
            req = urllib.request.Request(
                url, headers={"User-Agent": "PasswordCheckerApp/1.0"}
            )

            with urllib.request.urlopen(req) as response:
                if response.status == 200:
                    hashes = response.read().decode("utf-8").splitlines()

                    found = False
                    for line in hashes:
                        h_suffix, _ = line.split(":")
                        if h_suffix == suffix:
                            found = True
                            break

                    if found:
                        self.lbl_hibp.config(
                            text="HIBP: WARNING! Match found in known data breach!",
                            fg="red",
                        )
                    else:
                        self.lbl_hibp.config(
                            text="HIBP: Safe! No breach match found.", fg="green"
                        )
                else:
                    self.lbl_hibp.config(
                        text="HIBP: Network error or API failure.", fg="red"
                    )

        except Exception:
            self.lbl_hibp.config(
                text="HIBP: Network error or API failure.", fg="red"
            )

    def generate_password(self):
        chars = string.ascii_letters + string.digits + "!@#$%^&*()"
        secure_prng = random.SystemRandom()
        new_pass = "".join(secure_prng.choice(chars) for _ in range(16))

        self.entry_sug.delete(0, tk.END)
        self.entry_sug.insert(0, new_pass)


if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordCheckerGUI(root)
    root.mainloop()