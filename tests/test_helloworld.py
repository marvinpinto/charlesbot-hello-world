import asynctest
from asynctest.mock import patch


class TestHelloWorld(asynctest.TestCase):

    def setUp(self):
        patcher1 = patch('charlesbot_hello_world.helloworld.HelloWorld.load_config')  # NOQA
        self.addCleanup(patcher1.stop)
        self.mock_load_config = patcher1.start()

        from charlesbot_hello_world.helloworld import HelloWorld
        test_plug = HelloWorld()  # NOQA

    def tearDown(self):
        pass

    @asynctest.ignore_loop
    def test_something(self):
        pass
