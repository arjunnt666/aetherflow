from aetherflow.core.types import Message, MessageRole, Artifact, TaskStatus


def test_message_creation():
    msg = Message(role=MessageRole.USER, content="Hello")
    assert msg.role == MessageRole.USER
    assert msg.content == "Hello"
    assert msg.id is not None


def test_artifact():
    art = Artifact(name="report", type="text", content="Hello world")
    assert art.name == "report"
