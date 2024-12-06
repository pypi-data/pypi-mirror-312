from PyTaskHelper.string_utils import snake_to_camel, camel_to_snake

def test_snake_to_camel():
    assert snake_to_camel('hello_world') == 'HelloWorld'

def test_camel_to_snake():
    assert camel_to_snake('HelloWorld') == 'hello_world'
