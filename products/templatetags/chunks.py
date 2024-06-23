from django import template

register = template.Library()

@register.filter(name='chunks')
def chunks(list_data, chunk_size):
    """
    Splits a list into chunks of the specified size.
    Yields each chunk as a list.
    """
    chunk = []
    for i, data in enumerate(list_data, start=1):
        chunk.append(data)
        if i % chunk_size == 0:
            yield chunk
            i=0
            chunk = []
    if chunk:
        yield chunk

