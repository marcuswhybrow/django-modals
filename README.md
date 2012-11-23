Django Modals
=============

Do you want modal forms? Love abstraction? Make things easy with django-modals!

I really love [Twitter's bootstrap][bootstrap], and use [modals][modals] all the time to display forms. Manually adding forms to a view is a giant pain. You've got to override `get_context_data()` and slip in your form, and then do the same with `post()` to grap the result.

That all sounds easy enough the first time. But then you add another form to the same view, and you find yourself distinuishing between forms by the submit button name, or a hidden field. **It's time to abstract!**

Django Modal's `ModalMixin` tidies up that messy code, and allows you to neatly define subclasses of `Modal`, instances of which are included in the template context. A `Modal` subclass defines a template to use for rendering the modal in HTML, only handles data from a specific modal form, and defines methods for valid and invalid form data handling:

```
class MyThingModal(Modal):
    form_class = MyThingForm
    template_name = 'app/my_thing_modal.html'

    def valid(self, form):
        form.save()
        # Do other work here

    def invalid(self, form):
        # Take other action
```

I'm figuring out the best approach, and it's not functional yet. But I think this is a useful abstraction to make.


[bootstrap]: http://twitter.github.com/bootstrap/
[modals]: http://twitter.github.com/bootstrap/javascript.html#modals