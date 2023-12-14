import tkinter as tk

class DraggablePuzzlePopup:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Puzzle Pop-up")

    def create_puzzle_pieces(self, images):
        pieces = []
        for idx, img in enumerate(images):
            piece = self.PuzzlePiece(self.root, img, piece_id=idx)
            piece.place(x=(idx % 3) * 100, y=(idx // 3) * 100)  # Initial placement, arrange in a grid
            pieces.append(piece)
        return pieces

    class PuzzlePiece(tk.Label):
        def __init__(self, master, image, piece_id):
            super().__init__(master, image=image)
            self.piece_id = piece_id
            self.bind('<ButtonPress-1>', self.on_press)
            self.bind('<B1-Motion>', self.on_drag)
            self.bind('<ButtonRelease-1>', self.on_release)
            self.drag_data = {'x': 0, 'y': 0}

        def on_press(self, event):
            self.drag_data['x'] = event.x
            self.drag_data['y'] = event.y

        def on_drag(self, event):
            x = self.winfo_x() - self.drag_data['x'] + event.x
            y = self.winfo_y() - self.drag_data['y'] + event.y
            self.place(x=x, y=y)

        def on_release(self, event):
            self.drag_data = {'x': 0, 'y': 0}

    def create_puzzle_board(self):
        board = tk.Frame(self.root, width=300, height=300, bg='black', borderwidth=2, relief="solid")
        board.place(x=20, y=20)  # Adjust position as needed
        return board

    def show(self):
        popup = tk.Toplevel(self.root)
        popup.title("Draggable Puzzle")

        # Load puzzle piece images
        img_paths = [
            f"res/images/piece{i + 1}.png" for i in range(9)
        ]  # Paths for nine pieces in the format res/images/pieceX.png
        images = [tk.PhotoImage(file=path) for path in img_paths]

        # Create puzzle pieces
        puzzle_pieces = self.create_puzzle_pieces(images)

        # Create a black puzzle board
        puzzle_board = self.create_puzzle_board()

        self.root.mainloop()

