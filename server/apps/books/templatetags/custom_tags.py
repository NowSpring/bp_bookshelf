from django import template

register = template.Library()

@register.filter
def unique_booklists(personal_books):

  if personal_books is None:

    return []

  unique = []
  seen = set()

  for pb in personal_books:

    identifier = (pb.booklist.title, pb.booklist.owner.username)

    if identifier not in seen:

      unique.append(pb)
      seen.add(identifier)

  return unique
