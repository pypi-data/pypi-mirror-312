import threading
import time
from concurrent.futures import ThreadPoolExecutor
from queue import Empty, Full, Queue

from cnvrgv2.cli.utils.progress_bar_utils import init_progress_bar_for_cli
from cnvrgv2.data.clients.storage_client_factory import storage_client_factory
from cnvrgv2.data.cvc.error_messages import CVC_MALFUNCTION_IN_FILES_COLLECTOR
from cnvrgv2.data.cvc.errors import CvcMalfunctioningFilesCollector
from cnvrgv2.errors import CnvrgRetryError


class CvcRemoteFilesHandler:
    def __init__(
        self,
        store,
        total_files,
        total_files_size=None,
        num_workers=40,
        queue_size=5000,
        progress_bar_enabled=False,
        progress_bar_message=""
    ):
        """
        Multithreaded remote file handler base class
        @param store: The store object
        @param total_files: Total number of files to download
        @param num_workers: Number of threads to handle files
        @param queue_size: Max number of file meta to put in queue
        @param progress_bar_enabled: Boolean indicating whenever or not to print a progress bar. In use of the cli
        """
        # Init the storage client
        self.store = store
        self.storage_client = storage_client_factory(refresh_function=self.store.storage_meta_refresh_function())
        self.progress_bar_enabled = progress_bar_enabled
        self.progress_bar = None

        # Init progress bar messages
        self.progress_bar_message = progress_bar_message

        self.queue_size = queue_size
        self.progress_queue = Queue(self.queue_size)  # Files deleted / downloaded
        self.handle_queue = Queue(self.queue_size)  # Files need to be deleted / downloaded

        # Create a thread event in order to exit download when needed
        self.task_active = threading.Event()
        self.task_active.set()

        # Create a thread-safe lock
        self.progress_lock = threading.Lock()

        # Create collector thread which fetches file chunks from the server
        self.file_index = 0
        self.collector_thread = threading.Thread(target=self.file_collector)

        # Create progress thread which tracks the upload progress
        self.errors = None
        self.total_files = total_files
        self.total_files_size = total_files_size
        self.handled_files = 0
        self.handle_threads = []
        self.progress_thread = threading.Thread(target=self.task_progress)

        # Init threads
        self.collector_thread.start()
        self.progress_thread.start()

        # Create downloader threads to parallelize s3 file download
        for i in range(num_workers):
            t = threading.Thread(target=self.file_handler)
            t.start()
            self.handle_threads.append(t)

    @property
    def in_progress(self):
        """
        Property used to check if the upload is still in progress
        @return: Boolean
        """
        return self.task_active.is_set()

    def task_progress(self):
        """
        Handles the upload progress and confirming file uploads to the server
        @return: None
        """

        while self.handled_files < self.total_files and self.task_active.is_set():

            try:
                self.progress_queue.get_nowait()

                with self.progress_lock:
                    self.handled_files += 1

            except Empty:
                time.sleep(0.5)

        self.clear()

    def clear(self):
        """
        Clear the threads used to download files
        @return: none
        """
        # Clear download threads
        self.task_active.clear()
        if self.collector_thread:
            self.collector_thread.join()
        for t in self.handle_threads:
            t.join()

        if self.progress_bar_enabled and self.progress_bar:
            self.progress_bar.finish()

    def file_collector(self):
        """
        The function that handles collecting files metadata from the server
        @return: None
        """
        next_chunk = 0
        with ThreadPoolExecutor() as executor:
            while (
                self.total_files > 0 and
                self.file_index < self.total_files and
                self.task_active.is_set()
            ):
                # Attempt to retrieve file chunk from the server
                try:
                    files_to_process = self._collector_function(chunk_number=next_chunk)
                    self.file_index = self.file_index + len(files_to_process)

                    if self.progress_bar_enabled and not self.progress_bar:
                        self.progress_bar = init_progress_bar_for_cli(self.progress_bar_message, self.total_files_size)

                    # Parallelize the add to handle queue part,
                    # to prevent stalling the next call of _file_collector_function
                    executor.submit(self._add_chunk_to_handle_queue, files_to_process)

                    next_chunk += 1

                    # Before next loop, verify that if we got an empty result, it was the last.
                    # If it wasn't the last it point to a miscalculation between the total_files and the real number of
                    # file at the db, or a corrupted representation of file_chunks in the db
                    # (there is an empty chunk before the latest chunk)
                    if files_to_process == 0 and self.file_index < self.total_files:
                        raise CvcMalfunctioningFilesCollector(CVC_MALFUNCTION_IN_FILES_COLLECTOR)

                except Exception as e:
                    # Keep the errors on a variable, and retrieve them back on the main thread
                    self.errors = e
                    if self.progress_bar_enabled:
                        print("Could not process files {}".format(self.file_index))
                        print(e)
                    self.task_active.clear()
                    return

    def _add_chunk_to_handle_queue(self, chunk):
        """
        Attempt to put the new files in the upload queue, non-blocking in case we want to stop the upload
        @param chunk: list. Files to add to the handle_queue
        @return: None
        """
        # non-blocking in case we want to break iterator loop
        for cvc_file in chunk:
            while self.task_active.is_set():
                try:
                    self.handle_queue.put_nowait(cvc_file)
                    break
                except Full:
                    time.sleep(0.5)

    def file_handler(self):
        """
        Function to handle single file
        @return: None
        """
        # Run as long as we have files to download
        while self.task_active.is_set():
            try:
                # Get file non-blocking way, otherwise thread will hang forever
                file = self.handle_queue.get_nowait()
                self._handle_file_function(file, progress_bar=self.progress_bar)

            except Empty:
                time.sleep(0.5)
            except CnvrgRetryError:
                # If we could not download the file we still count it as processed
                with self.progress_lock:
                    self.handled_files += 1
            except Exception as e:
                # Should not be possible to enter here, safeguard against deadlock
                print("An unhandled exception in downloader thread has occurred:")
                print(e)
                with self.progress_lock:
                    self.handled_files += 1

    def _collector_function(self, chunk_number=None) -> dict:
        """
        Base function to collect files metadata from server
        @param chunk_number: int. The sequence of the chunk to fetch
        @return: Should return array of cvc file objects
        """
        pass

    def _handle_file_function(self, file, progress_bar=None):
        """
        Base function to handle single file
        @param local_path: File location locally
        @param kwargs: Needs to be fullpath / object_path depends on the class using this base
        @return: None
        """
        pass
