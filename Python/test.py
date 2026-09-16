def outer_func():
    msg = 'Hello'

    def inner_func():
        msg = 'Hi'
        return msg

    inner_func()
    return msg

print(outer_func())
programming_languages = ('Rust', 'Java', 'Python', 'C++', 'Rust', 'Python', 'JavaScript', 'Python')
programming_languages.index()