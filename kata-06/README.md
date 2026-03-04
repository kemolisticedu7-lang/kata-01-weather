## Git Bisect Report

### Bug Description
A bug was intentionally introduced by removing the call to `ensure_output_dir()` in `main()`.  
This caused the program to fail when attempting to write output files because the output directory was not created.

### Known Good / Bad Commits

Good commit:
8f2a130 - Kata 6: Process-based parallelism using ProcessPoolExecutor

Bad commit:
7e563ad - Introduce bug: skip output dir creation

### Bisect Commands Used

git bisect start  
git bisect bad 7e563ad  
git bisect good 8f2a130  

### Result

Git bisect identified commit **7e563ad** as the first bad commit that introduced the bug.

The bug occurred because the function `ensure_output_dir()` was removed, which prevented the program from creating the required output directory before writing files.