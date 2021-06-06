from django.db import models

# Create your models here.

#장르 모델
class Genre(models.Model):
    """Model representing a book genre."""
    name = models.CharField(max_length=200, help_text='Enter a book genre (e.g. Science Fiction)')

    def __str__(self):
        """String for representing the Model object."""
        return self.name

#책 모델
from django.urls import reverse #Used to generate URLs by reversing the URL patterns
# URL pattern 을 반환해서 url들을 만들어 낼것임

class Book(models.Model):
    """Model representing a book (but not a specific copy of a book)."""
    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    # null = true    저자는 null 상태여도 가능!
    # on_delete=models.SET_NULL    저자 정보가 삭제되었을때 저자의 값을 null로 설정!

    # Foreign Key used because book can only have one author, but authors can have multiple books
    # 일대다 키가 사용됨. 책은 하나의 저자를 갖지만 저자는 여러 책을 가질 수 있음
    # Author as a string rather than object because it hasn't been declared yet in the file.
    # 파일 내에서 아직 author 클래스가 정의되지 않았기때문에 문자열로 사용해야함!
    Summary = models.TextField(max_length=1000, help_text='Enter a brief description of the book')
    isbn = models.CharField('ISBN', max_length=13, help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')

    # ManyToManyField used because genre can contain many books. Books can cover many genres.
    # 다대다필드를 사용함. 책은 다양한 장르를 가질 수 있고, 장르 또한 다양한 책을 가질 수 있음.
    # Genre class has already been defined so we can specify the object above.
    # 장르 클래스는 이미 정의되어있으므로 객체를 구체화 할 수 있다.
    genre = models.ManyToManyField(Genre, help_text='Select a genre for this book')

    def __str__(self):
        """String for representing the Model object."""
        return self.title

    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        """
        이 책에 디테일한 정보에 접근할 수 있는 url을 return한다
        이것을 가능하게 하려면 book-detail이란 이름의 URL을 mapping하고 관련 뷰와 탬플릿 정의해야함
        """
        return reverse('book-detail', args[str(self.id)])

    def display_genre(self):
        """Create a string for the Genre. This is required to display genre in Admin."""
        return ', '.join(genre.name for genre in self.genre.all()[:3])

    display_genre.short_description = 'Genre'

# Book instance 모델
import uuid # Required for unique book instances
# Book instance : 책의 복사본, 사용가능여부, 반납예정일, 버전세부사항, 도서관 내 고유 id 등

class BookInstance(models.Model):
    """Model representing a specific copy of a book (i.e. that can be borrowed from the library)"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this particular book across whole library')
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200) # 책의 출판정보(특정 발간일을 나타내기 위함)
    due_back = models.DateField(null=True, blank=True)   # 반납 예정일

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='m',
        help_text='Book availablity',
    )

    class meta:
        ordering = ['due_back']

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.id} ({self.book.title})' # f'{}' 문자열 포맷팅 방법!!

# 저자 모델
class Author(models.Model):
    """Model representing an author."""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        """Returns the url to access a particular author instance."""
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.last_name}, {self.first_name}' # f'{}' 문자열 포맷팅 방법!

class Language(models.Model):
    """Model representing a Language (e.g. English, French, Korean, etc.)"""
    name = models.CharField(max_length=200, help_text="Enter the book's natural language (e.g. English, French, Korean, etc.)")

    def __str__(self):
        """String for representing the Model object (in Admin site etc.)"""
        return self.name
