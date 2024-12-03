from books.models import Author, Publisher, Book, Genre

# Create Genres
fiction = Genre.objects.create(name="Fiction")
romance = Genre.objects.create(name="Romance")
dystopian = Genre.objects.create(name="Dystopian")
science_fiction = Genre.objects.create(name="Science Fiction")
mystery = Genre.objects.create(name="Mystery")
fantasy = Genre.objects.create(name="Fantasy")
non_fiction = Genre.objects.create(name="Non-Fiction")
history = Genre.objects.create(name="History")
thriller = Genre.objects.create(name="Thriller")
horror = Genre.objects.create(name="Horror")

# Create Authors
orwell = Author.objects.create(name="George Orwell", birth_year=1903)
austen = Author.objects.create(name="Jane Austen", birth_year=1775)
asimov = Author.objects.create(name="Isaac Asimov", birth_year=1920)
christie = Author.objects.create(name="Agatha Christie", birth_year=1890)
tolkien = Author.objects.create(name="J.R.R. Tolkien", birth_year=1892)
stephen_king = Author.objects.create(name="Stephen King", birth_year=1947)
yuval_noah_harari = Author.objects.create(name="Yuval Noah Harari", birth_year=1976)
rowling = Author.objects.create(name="J.K. Rowling", birth_year=1965)
dan_brown = Author.objects.create(name="Dan Brown", birth_year=1964)
mary_shelley = Author.objects.create(name="Mary Shelley", birth_year=1797)

# Create Publishers
secker_warburg = Publisher.objects.create(name="Secker & Warburg", country="UK")
penguin = Publisher.objects.create(name="Penguin Books", country="UK")
harper_collins = Publisher.objects.create(name="HarperCollins", country="USA")
random_house = Publisher.objects.create(name="Random House", country="USA")
macmillan = Publisher.objects.create(name="Macmillan", country="USA")
bloomsbury = Publisher.objects.create(name="Bloomsbury", country="UK")
simon_schuster = Publisher.objects.create(name="Simon & Schuster", country="USA")
hachette = Publisher.objects.create(name="Hachette Livre", country="France")
scholastic = Publisher.objects.create(name="Scholastic", country="USA")
oxford = Publisher.objects.create(name="Oxford University Press", country="UK")

# Create Books and Assign Genres
book1 = Book.objects.create(title="1984", author=orwell, publisher=secker_warburg, publication_year=1949)
book1.genres.add(dystopian, fiction)

book2 = Book.objects.create(title="Pride and Prejudice", author=austen, publisher=penguin, publication_year=1813)
book2.genres.add(romance, fiction)

book3 = Book.objects.create(title="Foundation", author=asimov, publisher=harper_collins, publication_year=1951)
book3.genres.add(science_fiction, fiction)

book4 = Book.objects.create(title="Murder on the Orient Express", author=christie, publisher=random_house, publication_year=1934)
book4.genres.add(mystery, thriller)

book5 = Book.objects.create(title="The Hobbit", author=tolkien, publisher=macmillan, publication_year=1937)
book5.genres.add(fantasy, fiction)

book6 = Book.objects.create(title="It", author=stephen_king, publisher=simon_schuster, publication_year=1986)
book6.genres.add(horror, thriller)

book7 = Book.objects.create(title="Sapiens: A Brief History of Humankind", author=yuval_noah_harari, publisher=hachette, publication_year=2011)
book7.genres.add(non_fiction, history)

book8 = Book.objects.create(title="Harry Potter and the Philosopher's Stone", author=rowling, publisher=bloomsbury, publication_year=1997)
book8.genres.add(fantasy, fiction)

book9 = Book.objects.create(title="The Da Vinci Code", author=dan_brown, publisher=scholastic, publication_year=2003)
book9.genres.add(thriller, mystery)

book10 = Book.objects.create(title="Frankenstein", author=mary_shelley, publisher=oxford, publication_year=1818)
book10.genres.add(horror, fiction)
