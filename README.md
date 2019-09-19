## Test assignment
Build and deploy a web application representing Dogs and Cats. 

Each dog and cat must have a name and birthday, and be linked to an Owner.

Owners should be able to access dogs and cats via an API and carry out CRUD operations on their Dog and Cat.

Owners should also be able to access dogs and cats via an admin interface.

#### Quickstart (local setup)
Assuming that you have created and activated virtual env and have Docker installed on
your machine.
```bash
cp .env.local.example .env
pip install -r requirements
inv db
inv setup
```
That's it. This will start database container, create schema and populate it with fake 
data to start working with that.

#### Implementation notes

##### Model structure
It would be possible to implement single model for pets and make a choice field for pet type.
Since in task description Dogs and Cats are written using capital letter I assume that
separate model is expected for them. In real situation I would prefer discuss
the model structure, whether to use single model or multiple models. There is no right 
answer, everything depends on further project requirements.

I used abstract model Pet as both Dog and Cat has common fields.

#### Users
I define role based permissions by overriding User's `has_perm` method. I think that 
this approach is better than configuring permissions for Groups. 


#### Admin site
Pet owner users will be able to edit only their own pets. This is achieved by overriding
choices for Pet form and querysets for Owner and pet models.
ModelAdmin classes also have `has_*_permission` function defined.


#### Tests
Tests are implemented using pytest framework and perform testing of REST endpoints

#### Frontend
To make frontend developer work easier swagger UI endpoint was added.
