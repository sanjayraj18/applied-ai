

class ToolError(Exception):
    """Recoverable. Step 2 catches this and hands the text back to the model."""

class LoopError(Exception):
    """Not recoverable by the model. The run must stop and a human must look."""

class CapExceeded(LoopError):
    """A budget ran out. The run stops; the caller decides whether to escalate."""