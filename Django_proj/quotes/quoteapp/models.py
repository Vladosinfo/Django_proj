from django.db import models


class Author(models.Model):
    fullname = models.CharField(max_length=50, null=False, unique=True)
    born_date = models.CharField(max_length=30, null=False)
    born_location = models.CharField(max_length=50, null=False)
    description = models.TextField(null=False)    

    def __str__(self):
        return f"{self.fullname}"


class Tag(models.Model):
    name = models.CharField(max_length=25, null=False, unique=True)

    def __str__(self):
        return f"{self.name}"


class Quote(models.Model):
    quote = models.CharField(max_length=255, null=False)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    # author = models.ForeignKey(User,   on_delete=models.SET_NULL)
    # author = models.ManyToOneRel("author_id", "id" on_delete=models.CASCADE)
    # ManyToOneRel(field="model_key", field_name="'id'", to="'id'")    
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return f"{self.quote}"
