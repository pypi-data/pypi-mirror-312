import random



class MovieQuotes:
    def __init__(self):
        # Predefined quotes database
        self.quotes = [
            {"quote": "Frankly, my dear, I don't give a damn.", "movie": "Gone with the Wind"},
            {"quote": "May the Force be with you.", "movie": "Star Wars"},
            {"quote": "I'll be back.", "movie": "The Terminator"},
            {"quote": "Here's looking at you, kid.", "movie": "Casablanca"},
            {"quote": "You can't handle the truth!", "movie": "A Few Good Men"},
            {"quote": "I'm the king of the world!", "movie": "Titanic"},
            {"quote": "Why so serious?", "movie": "The Dark Knight"},
            {"quote": "To infinity and beyond!", "movie": "Toy Story"},
            {"quote": "Say hello to my little friend!", "movie": "Scarface"},
            {"quote": "E.T. phone home.", "movie": "E.T. the Extra-Terrestrial"},
        ]

    def get_random_quote(self):
        """Fetch a random quote."""
        return random.choice(self.quotes)

    def get_quote_by_movie(self, movie_title):
        """Fetch a quote by movie title."""
        quotes = [q for q in self.quotes if q["movie"].lower() == movie_title.lower()]
        return quotes if quotes else f"No quotes found for movie: {movie_title}"

    def add_quote(self, quote, movie):
        """Add a new quote."""
        self.quotes.append({"quote": quote, "movie": movie})

    def list_quotes(self):
        """List all quotes."""
        return self.quotes
