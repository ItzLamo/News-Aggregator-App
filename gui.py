import tkinter as tk
from tkinter import ttk, messagebox
import webbrowser
from typing import List, Dict
from src.news_api import NewsAPI
from src.storage import Storage

class NewsAggregatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("News Aggregator")
        self.root.geometry("1000x600")
        
        self.news_api = NewsAPI()
        self.storage = Storage()
        
        self.setup_gui()
        
    def setup_gui(self):
        # Create main container
        self.main_container = ttk.Frame(self.root, padding="10")
        self.main_container.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Search frame
        search_frame = ttk.LabelFrame(self.main_container, text="Search News", padding="5")
        search_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=40)
        search_entry.grid(row=0, column=0, padx=5)
        
        search_button = ttk.Button(search_frame, text="Search", command=self.search_news)
        search_button.grid(row=0, column=1, padx=5)
        
        # Category frame
        category_frame = ttk.LabelFrame(self.main_container, text="Categories", padding="5")
        category_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        self.category_var = tk.StringVar()
        for i, category in enumerate(self.news_api.categories):
            rb = ttk.Radiobutton(category_frame, text=category.capitalize(),
                               variable=self.category_var, value=category)
            rb.grid(row=0, column=i, padx=5)
        
        # Articles frame
        articles_frame = ttk.LabelFrame(self.main_container, text="Articles", padding="5")
        articles_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        # Create articles list
        self.articles_list = ttk.Treeview(articles_frame, columns=("title", "source", "date"),
                                        show="headings", height=10)
        self.articles_list.heading("title", text="Title")
        self.articles_list.heading("source", text="Source")
        self.articles_list.heading("date", text="Date")
        
        self.articles_list.column("title", width=400)
        self.articles_list.column("source", width=150)
        self.articles_list.column("date", width=150)
        
        self.articles_list.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Scrollbar for articles list
        scrollbar = ttk.Scrollbar(articles_frame, orient=tk.VERTICAL, command=self.articles_list.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.articles_list.configure(yscrollcommand=scrollbar.set)
        
        # Buttons frame
        buttons_frame = ttk.Frame(self.main_container, padding="5")
        buttons_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        view_button = ttk.Button(buttons_frame, text="View Article", command=self.view_article)
        view_button.grid(row=0, column=0, padx=5)
        
        save_button = ttk.Button(buttons_frame, text="Save Article", command=self.save_article)
        save_button.grid(row=0, column=1, padx=5)
        
        saved_button = ttk.Button(buttons_frame, text="View Saved", command=self.view_saved_articles)
        saved_button.grid(row=0, column=2, padx=5)
        
        history_button = ttk.Button(buttons_frame, text="Search History", command=self.view_history)
        history_button.grid(row=0, column=3, padx=5)
        
        # Footer with credits
        footer_frame = ttk.Frame(self.main_container, padding="5")
        footer_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        footer_text = ttk.Label(
            footer_frame, 
            text="Developed by Hassan Ahmed for the Hack Club",
            font=("Helvetica", 9 ),
            foreground="#666666"
        )
        footer_text.pack(side=tk.RIGHT)
        
        # Store current articles
        self.current_articles = []
        
    def search_news(self):
        keywords = self.search_var.get()
        category = self.category_var.get()
        
        if keywords or category:
            self.current_articles = self.news_api.fetch_news(keywords, category)
            self.update_articles_list()
            if keywords:
                self.storage.save_search(keywords)
        else:
            messagebox.showwarning("Input Required", "Please enter keywords or select a category")
    
    def update_articles_list(self):
        self.articles_list.delete(*self.articles_list.get_children())
        for article in self.current_articles:
            self.articles_list.insert("", tk.END, values=(
                article['title'],
                article['source'],
                article['published_at'][:10]
            ))
    
    def view_article(self):
        selection = self.articles_list.selection()
        if selection:
            index = self.articles_list.index(selection[0])
            article = self.current_articles[index]
            webbrowser.open(article['url'])
        else:
            messagebox.showinfo("Selection Required", "Please select an article to view")
    
    def save_article(self):
        selection = self.articles_list.selection()
        if selection:
            index = self.articles_list.index(selection[0])
            article = self.current_articles[index]
            self.storage.save_article(article)
            messagebox.showinfo("Success", "Article saved successfully!")
        else:
            messagebox.showinfo("Selection Required", "Please select an article to save")
    
    def view_saved_articles(self):
        self.current_articles = self.storage.saved_articles
        self.update_articles_list()
    
    def view_history(self):
        history = self.storage.get_recent_searches()
        if history:
            history_text = "\n".join([f"{h['query']} - {h['timestamp']}" for h in history])
            messagebox.showinfo("Search History", history_text)
        else:
            messagebox.showinfo("Search History", "No search history available")