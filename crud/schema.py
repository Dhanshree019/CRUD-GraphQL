import graphene
from graphene_django import DjangoObjectType
from .models import Book

class BookType(DjangoObjectType):
    class Meta:
        model = Book


class Query(graphene.ObjectType):
    all_books = graphene.List(BookType)
    book_by_id = graphene.Field(BookType, id=graphene.Int())

    def resolve_all_books(self, info, **kwargs):
        return Book.objects.all()
    
    def resolve_book_by_id(self,info, id, **kwargs):
        return Book.objects.get(pk=id)
    
class CreateBook(graphene.Mutation):
    class Arguments:
        title = graphene.String(required = True)
        author = graphene.String(required = True)
        published_date = graphene.Date(required = True)
    
    book = graphene.Field(BookType)

    def mutate(self,info,title,author,published_date):
        book = Book.objects.create(
            title=title,
            author=author,
            published_date=published_date
        )

        return CreateBook(book)
    
class UpdateBook(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        title = graphene.String()
        author = graphene.String()
        published_date = graphene.Date()

    book = graphene.Field(BookType)

    def mutate(self,info,id,title=None,author=None,published_date=None):
        book = Book.objects.get(pk=id)

        if title:
            book.title = title
        
        if author:
            book.author = author

        if published_date:
            book.published_date = published_date

        book.save()
        return UpdateBook(book=book)

class DeleteBook(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
    
    success = graphene.Boolean()

    def mutate(self,info,id):
        try:
            book = Book.objects.get(pk=id)
            book.delete()
            return DeleteBook(success=True)
        except Book.DoesNotExist:
            return DeleteBook(success = False)



class Mutation(graphene.ObjectType):
    create_book = CreateBook.Field()
    update_book = UpdateBook.Field()
    delete_book = DeleteBook.Field()
    

schema = graphene.Schema(query=Query, mutation=Mutation)