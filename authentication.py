import matplotlib.pyplot as plt
from matplotlib.widgets import TextBox, Button


class LoginScreen:

    # Demonstration credentials only
    DEMO_USERNAME = "demo"
    DEMO_PASSWORD = "market123"

    def __init__(self):

        self.authenticated = False

        # Create login window
        self.fig, self.ax = plt.subplots(figsize=(8, 5))
        self.fig.canvas.manager.set_window_title(
            "Stock Market Monitor - Login"
        )

        self.fig.patch.set_facecolor("#20252B")
        self.ax.set_facecolor("#20252B")
        self.ax.axis("off")

        # Heading
        self.fig.text(
            0.5, 0.85,
            "STOCK MARKET MONITOR",
            ha="center",
            fontsize=20,
            weight="bold",
            color="#70E0EB"
        )

        self.fig.text(
            0.5, 0.77,
            "Please log in to continue",
            ha="center",
            fontsize=11,
            color="white"
        )

        # Username input
        ax_username = self.fig.add_axes(
            [0.30, 0.57, 0.40, 0.08]
        )

        self.username_box = TextBox(
            ax_username,
            "Username: ",
            initial=""
        )

        # Password input
        ax_password = self.fig.add_axes(
            [0.30, 0.42, 0.40, 0.08]
        )

        self.password_box = TextBox(
            ax_password,
            "Password: ",
            initial=""
        )

        # Login button
        ax_button = self.fig.add_axes(
            [0.40, 0.25, 0.20, 0.09]
        )

        self.login_button = Button(
            ax_button,
            "LOGIN",
            color="#43C6D9",
            hovercolor="#70E0EB"
        )

        self.login_button.on_clicked(
            self.authenticate
        )

        # Status message
        self.status = self.fig.text(
            0.5, 0.15,
            "",
            ha="center",
            fontsize=11,
            color="#FF8BAA"
        )

    def authenticate(self, event):

        username = self.username_box.text.strip()
        password = self.password_box.text

        if (
            username == self.DEMO_USERNAME
            and password == self.DEMO_PASSWORD
        ):

            self.authenticated = True

            self.status.set_text("Login successful!")

            self.status.set_color("#A9E6B4")

            self.fig.canvas.draw_idle()

            plt.close(self.fig)

        else:

            self.status.set_text(
                "Invalid username or password. Try again."
            )

            self.fig.canvas.draw_idle()

    def show(self):

        plt.show()

        return self.authenticated


# Test the login screen independently
if __name__ == "__main__":

    login = LoginScreen()

    if login.show():
        print("Access granted!")
    else:
        print("Login cancelled.")