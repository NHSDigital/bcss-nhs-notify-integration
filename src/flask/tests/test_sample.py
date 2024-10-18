class TestClass:
    # Self values are shared between tests in the test class, so would be an idea to gen access tokens/jwt in different test classes
    # Also need to look into how to mock the other classes in services
    def test_one(self):
        x = "this"
        assert "h" in x, f"h is in fact not in {x}"

    def test_two(self):
        x = "hello"
        assert hasattr(x, "check"), f"{x} does not in fact haveattr check"
