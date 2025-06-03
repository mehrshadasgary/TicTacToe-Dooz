import tkinter as tk
from tkinter import messagebox
import random
import math

class ModernTicTacToe:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("دوز مدرن - Tic Tac Toe")
        self.root.geometry("600x700")
        self.root.configure(bg='#1a1a2e')
        self.root.resizable(False, False)
        
        # رنگ‌های مدرن
        self.colors = {
            'bg': '#1a1a2e',
            'secondary': '#16213e',
            'accent': '#0f3460',
            'primary': '#e94560',
            'success': '#2ecc71',
            'text': '#ffffff',
            'text_secondary': '#bdc3c7'
        }
        
        # متغیرهای بازی
        self.board = ['' for _ in range(9)]
        self.current_player = 'X'
        self.game_mode = 'human'  # 'human' یا 'ai'
        self.game_over = False
        self.scores = {'X': 0, 'O': 0, 'Draw': 0}
        
        self.setup_ui()
        
    def setup_ui(self):
        # هدر اصلی
        header_frame = tk.Frame(self.root, bg=self.colors['bg'])
        header_frame.pack(pady=20)
        
        title_label = tk.Label(
            header_frame,
            text="🎮 دوز مدرن 🎮",
            font=("Arial", 24, "bold"),
            fg=self.colors['primary'],
            bg=self.colors['bg']
        )
        title_label.pack()
        
        # نمایش امتیازات
        self.score_frame = tk.Frame(self.root, bg=self.colors['bg'])
        self.score_frame.pack(pady=10)
        
        self.score_label = tk.Label(
            self.score_frame,
            text=f"X: {self.scores['X']} | O: {self.scores['O']} | مساوی: {self.scores['Draw']}",
            font=("Arial", 12),
            fg=self.colors['text_secondary'],
            bg=self.colors['bg']
        )
        self.score_label.pack()
        
        # نمایش نوبت بازیکن
        self.turn_label = tk.Label(
            self.root,
            text=f"نوبت: بازیکن {self.current_player}",
            font=("Arial", 14, "bold"),
            fg=self.colors['success'],
            bg=self.colors['bg']
        )
        self.turn_label.pack(pady=10)
        
        # صفحه بازی
        self.game_frame = tk.Frame(self.root, bg=self.colors['bg'])
        self.game_frame.pack(pady=20)
        
        self.buttons = []
        for i in range(9):
            btn = tk.Button(
                self.game_frame,
                text="",
                font=("Arial", 28, "bold"),
                width=4,
                height=2,
                bg=self.colors['secondary'],
                fg=self.colors['text'],
                activebackground=self.colors['accent'],
                activeforeground=self.colors['text'],
                relief='flat',
                bd=2,
                cursor='hand2',
                command=lambda idx=i: self.make_move(idx)
            )
            btn.grid(row=i//3, column=i%3, padx=3, pady=3)
            self.buttons.append(btn)
            
        # دکمه‌های کنترل
        control_frame = tk.Frame(self.root, bg=self.colors['bg'])
        control_frame.pack(pady=20)
        
        # دکمه شروع جدید
        new_game_btn = tk.Button(
            control_frame,
            text="🔄 بازی جدید",
            font=("Arial", 12, "bold"),
            bg=self.colors['primary'],
            fg=self.colors['text'],
            activebackground='#c0392b',
            relief='flat',
            padx=20,
            pady=10,
            cursor='hand2',
            command=self.new_game
        )
        new_game_btn.pack(side=tk.LEFT, padx=10)
        
        # دکمه تغییر حالت
        mode_btn = tk.Button(
            control_frame,
            text="🤖 بازی با کامپیوتر",
            font=("Arial", 12, "bold"),
            bg=self.colors['success'],
            fg=self.colors['text'],
            activebackground='#27ae60',
            relief='flat',
            padx=20,
            pady=10,
            cursor='hand2',
            command=self.toggle_mode
        )
        mode_btn.pack(side=tk.LEFT, padx=10)
        self.mode_btn = mode_btn
        
        # دکمه ری‌ست امتیازات
        reset_btn = tk.Button(
            control_frame,
            text="📊 ری‌ست امتیازات",
            font=("Arial", 12, "bold"),
            bg=self.colors['accent'],
            fg=self.colors['text'],
            activebackground='#2c3e50',
            relief='flat',
            padx=20,
            pady=10,
            cursor='hand2',
            command=self.reset_scores
        )
        reset_btn.pack(side=tk.LEFT, padx=10)
        
    def make_move(self, index):
        if self.board[index] == '' and not self.game_over:
            self.board[index] = self.current_player
            self.buttons[index].config(
                text=self.current_player,
                fg=self.colors['primary'] if self.current_player == 'X' else self.colors['success'],
                state='disabled'
            )
            
            # انیمیشن کلیک
            self.animate_button(self.buttons[index])
            
            if self.check_winner():
                self.end_game(self.current_player)
            elif self.is_board_full():
                self.end_game('Draw')
            else:
                self.current_player = 'O' if self.current_player == 'X' else 'X'
                self.update_turn_display()
                
                # اگر حالت AI فعال است و نوبت کامپیوتر است
                if self.game_mode == 'ai' and self.current_player == 'O' and not self.game_over:
                    self.root.after(500, self.ai_move)
    
    def ai_move(self):
        """حرکت هوشمند کامپیوتر با الگوریتم Minimax"""
        best_move = self.get_best_move()
        if best_move is not None:
            self.make_move(best_move)
    
    def get_best_move(self):
        """پیدا کردن بهترین حرکت با الگوریتم Minimax"""
        best_score = -math.inf
        best_move = None
        
        for i in range(9):
            if self.board[i] == '':
                self.board[i] = 'O'
                score = self.minimax(self.board, 0, False)
                self.board[i] = ''
                
                if score > best_score:
                    best_score = score
                    best_move = i
        
        return best_move
    
    def minimax(self, board, depth, is_maximizing):
        """الگوریتم Minimax"""
        winner = self.check_winner_for_board(board)
        
        if winner == 'O':
            return 1
        elif winner == 'X':
            return -1
        elif self.is_board_full_for_board(board):
            return 0
        
        if is_maximizing:
            best_score = -math.inf
            for i in range(9):
                if board[i] == '':
                    board[i] = 'O'
                    score = self.minimax(board, depth + 1, False)
                    board[i] = ''
                    best_score = max(score, best_score)
            return best_score
        else:
            best_score = math.inf
            for i in range(9):
                if board[i] == '':
                    board[i] = 'X'
                    score = self.minimax(board, depth + 1, True)
                    board[i] = ''
                    best_score = min(score, best_score)
            return best_score
    
    def check_winner_for_board(self, board):
        """بررسی برنده برای یک تخته خاص"""
        winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # ردیف‌ها
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # ستون‌ها
            [0, 4, 8], [2, 4, 6]              # قطرها
        ]
        
        for combo in winning_combinations:
            if board[combo[0]] == board[combo[1]] == board[combo[2]] != '':
                return board[combo[0]]
        return None
    
    def is_board_full_for_board(self, board):
        """بررسی پر بودن تخته برای یک تخته خاص"""
        return '' not in board
    
    def animate_button(self, button):
        """انیمیشن ساده برای دکمه"""
        original_bg = button.cget('bg')
        button.config(bg=self.colors['primary'])
        self.root.after(100, lambda: button.config(bg=original_bg))
    
    def check_winner(self):
        """بررسی وجود برنده"""
        winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # ردیف‌ها
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # ستون‌ها
            [0, 4, 8], [2, 4, 6]              # قطرها
        ]
        
        for combo in winning_combinations:
            if self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]] != '':
                # رنگ‌آمیزی خانه‌های برنده
                for idx in combo:
                    self.buttons[idx].config(bg=self.colors['success'])
                return True
        return False
    
    def is_board_full(self):
        """بررسی پر بودن تخته"""
        return '' not in self.board
    
    def end_game(self, winner):
        """پایان بازی"""
        self.game_over = True
        self.scores[winner] += 1
        self.update_score_display()
        
        if winner == 'Draw':
            message = "🤝 بازی مساوی شد!"
            title = "مساوی"
        else:
            if self.game_mode == 'ai' and winner == 'O':
                message = f"🤖 کامپیوتر برنده شد!"
            else:
                message = f"🎉 بازیکن {winner} برنده شد!"
            title = "برنده"
        
        messagebox.showinfo(title, message)
        
        # غیرفعال کردن تمام دکمه‌ها
        for btn in self.buttons:
            btn.config(state='disabled')
    
    def new_game(self):
        """شروع بازی جدید"""
        self.board = ['' for _ in range(9)]
        self.current_player = 'X'
        self.game_over = False
        
        for btn in self.buttons:
            btn.config(
                text="",
                state='normal',
                bg=self.colors['secondary'],
                fg=self.colors['text']
            )
        
        self.update_turn_display()
    
    def toggle_mode(self):
        """تغییر حالت بازی"""
        if self.game_mode == 'human':
            self.game_mode = 'ai'
            self.mode_btn.config(text="👥 بازی دو نفره")
        else:
            self.game_mode = 'human'
            self.mode_btn.config(text="🤖 بازی با کامپیوتر")
        
        self.new_game()
    
    def reset_scores(self):
        """ری‌ست کردن امتیازات"""
        self.scores = {'X': 0, 'O': 0, 'Draw': 0}
        self.update_score_display()
        messagebox.showinfo("ری‌ست", "امتیازات ری‌ست شدند!")
    
    def update_turn_display(self):
        """به‌روزرسانی نمایش نوبت"""
        if self.game_mode == 'ai':
            if self.current_player == 'X':
                text = "نوبت: شما (X)"
            else:
                text = "نوبت: کامپیوتر (O)"
        else:
            text = f"نوبت: بازیکن {self.current_player}"
        
        self.turn_label.config(text=text)
    
    def update_score_display(self):
        """به‌روزرسانی نمایش امتیازات"""
        self.score_label.config(
            text=f"X: {self.scores['X']} | O: {self.scores['O']} | مساوی: {self.scores['Draw']}"
        )
    
    def run(self):
        """اجرای بازی"""
        self.root.mainloop()

# اجرای بازی
if __name__ == "__main__":
    game = ModernTicTacToe()
    game.run()