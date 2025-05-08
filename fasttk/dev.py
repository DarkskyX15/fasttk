
import os
import sys
import logging
import threading
import watchfiles
import importlib

from fasttk.tkvm import ftk

CWD = os.getcwd()

stop_event = threading.Event()
pass_event = threading.Event()
reload_event = threading.Event()

root_logger = logging.getLogger("FastTk")
logger = logging.getLogger("FastTk.DevServer")

def _watch_worker():

    logger = logging.getLogger("FastTk.WatchFiles")
    logger.info(f"Watching files at {CWD}.")

    for changes in watchfiles.watch(
        CWD, stop_event=stop_event, watch_filter=watchfiles.PythonFilter()
    ):
        for file_change in changes:
            change, file = file_change
            logger.info(f"Detect change '{change.name}' in {file}, reloading...")
            reload_event.set()
        pass_event.wait()
        logger.info("Reload complete, keep watching.")
        pass_event.clear()


    logger.info("WatchFiles thread exited.")

def _serve(
    src: str,
    cls_name: str,
    title: str,
    size: tuple[int, int],
    background: str
) -> None:
    
    logger.info(f"Loading window entrance in module {src}")
    
    sys.path.append(CWD)
    entrance = importlib.import_module(src)
    component_cls = getattr(entrance, cls_name, None)
    if not component_cls:
        raise ImportError(f"Export entry point '{cls_name}' not found in module '{src}'.")

    logger.info("Starting FastTk dev server.")

    watch_thread = threading.Thread(
        target=_watch_worker, name="fasttk.WatchFiles"
    )
    watch_thread.start()
    
    logger.info("Press Ctrl+C to stop.")

    def reload_callback() -> None:
        nonlocal entrance
        try:
            entrance = importlib.reload(entrance)
            component = getattr(entrance, cls_name, None)
            if not component:
                raise ImportError(f"Export entry point '{cls_name}' not found in module '{src}'.")
        except Exception as e:
            logger.warning("Exception while reloading, skip this reload.")
        else:
            ftk.mount_component(ftk._tk, component)

    try:
        ftk.main_window(
            component_cls, title=title, size=size, background=background
        )
        ftk._track_reload(reload_event, pass_event, reload_callback)
        ftk.mainloop()
        stop_event.set()
    except KeyboardInterrupt:
        logger.info("Stop FastTk dev server.")
        pass_event.set()
        stop_event.set()

    watch_thread.join()

def start_dev_server(
    src: str,
    cls_name: str = "export",
    title: str = "FastTk Dev Window",
    size: tuple[int, int] = (600, 400),
    background: str = "white"
) -> None:
    try:
        _serve(src, cls_name, title, size, background)
    except Exception as e:
        logger.error(
            "Exception while starting dev server:", exc_info=True
        )

def _console() -> None:
    # TODO command entry point
    print("Hello from console.")
