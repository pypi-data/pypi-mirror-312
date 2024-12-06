import queue
import threading
from concurrent.futures import ThreadPoolExecutor
from typing import Optional, Callable, Tuple

from .manager import TaskManagerBase
from .typedefs import Lock, Event, Queue


class TaskManagerWithThreadPoolExecutor(TaskManagerBase):
    def __init__(
        self,
        max_workers: Optional[int] = None,
        thread_name_prefix: str = "",
        initializer: Optional[Callable] = None,
        initargs: Tuple = (),
        *,
        global_input_queue: bool = False,
        global_output_queue: bool = False,
        global_cancel_event: bool = False,
        global_input_queue_lock: bool = False,
        global_output_queue_lock: bool = False,
        global_input_queue_size: Optional[int] = None,
        global_output_queue_size: Optional[int] = None,
    ):
        self._executor: ThreadPoolExecutor = ThreadPoolExecutor(
            max_workers=max_workers,
            thread_name_prefix=thread_name_prefix,
            initializer=initializer,
            initargs=initargs,
        )
        super().__init__(
            self._executor,
            global_input_queue=global_input_queue,
            global_output_queue=global_output_queue,
            global_cancel_event=global_cancel_event,
            global_input_queue_lock=global_input_queue_lock,
            global_output_queue_lock=global_output_queue_lock,
            global_input_queue_size=global_input_queue_size,
            global_output_queue_size=global_output_queue_size,
        )

    def create_queue(self, size: Optional[int] = None) -> Queue:
        if not size:
            return queue.Queue()
        return queue.Queue(maxsize=size)

    def create_event(self) -> Event:
        return threading.Event()

    def create_lock(self) -> Lock:
        return threading.Lock()

    def __exit__(self, exc_type, exc_val, exc_tb):
        super().__exit__(exc_type, exc_val, exc_tb)

    def shutdown(self):
        self._executor.shutdown()
