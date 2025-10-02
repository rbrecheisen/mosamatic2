import os
import shutil
import tempfile
from totalsegmentator.python_api import totalsegmentator
from mosamatic2.core.tasks.task import Task
from mosamatic2.core.managers.logmanager import LogManager

LOG = LogManager()
TOTAL_SEGMENTATOR_OUTPUT_DIR = os.path.join(tempfile.gettempdir(), 'total_segmentator_output')


class TotalSegmentatorTask(Task):
    INPUTS = ['scans']
    PARAMS = ['tasks']

    def __init__(self, inputs, params, output, overwrite):
        super(TotalSegmentatorTask, self).__init__(inputs, params, output, overwrite)
        LOG.info(f'Using temporary output directory: {TOTAL_SEGMENTATOR_OUTPUT_DIR}')

    def load_scan_dirs(self):
        scan_dirs = []
        for d in os.listdir(self.input('scans')):
            scan_dir = os.path.join(self.input('scans'), d)
            if os.path.isdir(scan_dir):
                scan_dirs.append(scan_dir)
        return scan_dirs
    
    def extract_masks(self, scan_dir):
        os.makedirs(TOTAL_SEGMENTATOR_OUTPUT_DIR, exist_ok=True)
        tasks = self.param('tasks').split(",") if self.param('tasks') else []
        for task in tasks:
            LOG.info(f'Running task {task}...')
            totalsegmentator(input=scan_dir, output=TOTAL_SEGMENTATOR_OUTPUT_DIR, task=task)

    def run(self):
        scan_dirs = self.load_scan_dirs()
        nr_steps = len(scan_dirs)
        for step in range(nr_steps):
            scan_dir = scan_dirs[step]
            try:
                self.extract_masks(scan_dir)
            except Exception as e:
                LOG.error(f'{scan_dir}: Could not extract masks [{str(e)}]. Skipping scan...')
            self.set_progress(step, nr_steps)
            LOG.info(f'Copying temporary output to final output directory...')
            for f in os.listdir(TOTAL_SEGMENTATOR_OUTPUT_DIR):
                if f.endswith('.nii') or f.endswith('.nii.gz'):
                    f_path = os.path.join(TOTAL_SEGMENTATOR_OUTPUT_DIR, f)
                    shutil.move(f_path, self.output())
                    LOG.info(f'Copied {f}')
