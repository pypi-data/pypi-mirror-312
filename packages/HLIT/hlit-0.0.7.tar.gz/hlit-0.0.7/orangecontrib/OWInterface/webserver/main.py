import asyncio
import os
import time
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any, Dict, List

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse

from fileQueue import FileQueue
from utils import (generate_unique_output_folder, hash_file_content, make_list,
                   zip_folder)


@asynccontextmanager
async def lifespan(app: FastAPI):
    os.makedirs(save_directory, exist_ok=True)
    os.makedirs(output_directory, exist_ok=True)
    asyncio.create_task(process_files_queue())
    yield

app = FastAPI(lifespan=lifespan)
# CORS Settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # List of origins that are allowed, '*' means allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # List of HTTP methods that are allowed, '*' means allow all methods
    allow_headers=["*"],  # List of headers that are allowed, '*' means allow all headers
)

# Constants
MAX_PROCESSING_QUEUE_LENGTH: int = 1
TIMEOUT_LIMIT: int = 120  # seconds

# Path settingsmatch_number
save_directory: Path = Path(__file__).parent / "received_files"
output_directory: Path = Path(__file__).parent / "sent_files"

print("save_directory: ", save_directory)
print("output_directory: ", output_directory)

waiting_queue: FileQueue = FileQueue(save_directory / "waiting_queue.json")
in_process_queue: FileQueue = FileQueue(save_directory / "in_process_queue.json")

def make_tuple_list(text_inputs: List[str]) -> List[tuple[str, str]]:
    assert len(text_inputs) % 2 == 0, "The number of text inputs must be even."
    print("text_inputs: ", text_inputs)
    print("return: ", [(text_inputs[i], text_inputs[i+1]) for i in range(0, len(text_inputs), 2)])
    return [(text_inputs[i], text_inputs[i+1]) for i in range(0, len(text_inputs), 2)]

# Main API Endpoints
@app.post("/upload-files/")
async def upload_files(
    file_ids: List[str], 
    workflow_id: str,
    opening_methods: List[str], 
    expected_nb_outputs: int, 
    files: List[UploadFile] = File(...),
    text_inputs: List[str] = []
) -> JSONResponse:
    """
    Upload multiple files to the server for processing through a Orange workflow. 
      
    Args:   
        - file_ids (List[str]): List of unique file IDs corresponding to the files.
          The IDs should match the ones configured in the Orange workflow.   
        - workflow_id (str): Unique ID of the workflow.
          The ID should match the one configured in the Orange workflow.   
        - opening_methods (List[str]): List of opening methods for the files.
          Choose from 'image_file', 'multiple_file', or 'file'.    
        - expected_nb_outputs (int): Expected number of output files (depending on your workflow).
        - files (List[UploadFile]): List of files to be uploaded.  
        - text_inputs (List[str]): List of text inputs for the workflow. Must be in the format [input_id1, value1, input_id2, value2].

    Returns:   
        JSONResponse: Response message with the unique ID of the processing task."""
    text_inputs = make_list(text_inputs)
    opening_methods = make_list(opening_methods)
    print(file_ids, opening_methods)
    if len(files) != len(file_ids) or len(files) != len(opening_methods):
        raise HTTPException(status_code=400, detail="Number of files, file IDs, and opening methods must match.")

    file_entries: List[Dict[str, Any]] = []
    for file, file_id, opening_method in zip(files, file_ids, opening_methods):
        if opening_method not in ["image_file", "multiple_file", "file"]:
            raise HTTPException(status_code=400, detail="Invalid opening method provided. Choose from 'image_file', 'multiple_file', or 'file'.")
        
        content: bytes = await file.read()
        file_hash: str = hash_file_content(content)
        input_filename: str = str(save_directory / str(file.filename))
        
        # Save the file locally
        with open(input_filename, 'wb') as f:
            f.write(content)

        file_entries.append({
            'input_filename': input_filename,
            'file_id': file_id,
            'file_hash': file_hash,
            'opening_method': opening_method,
        })

    unique_id, output_folder = generate_unique_output_folder(output_directory)

    waiting_queue.add({
        'unique_id': unique_id,
        'workflow_id': workflow_id,
        'file_entries': file_entries,
        'output_folder': str(output_folder),
        'expected_nb_outputs': expected_nb_outputs,
        'text_inputs': text_inputs
    })

    return JSONResponse(content={"message": "Files queued for processing", "unique_id": unique_id})

@app.post("/upload-files-via-path/")
async def upload_files_via_path(
    filepaths: List[str], 
    file_ids: List[str], 
    opening_methods: List[str],
    workflow_id: str, 
    expected_nb_outputs: int,
    text_inputs: List[tuple[str, str]] = []
) -> JSONResponse:
    """
    Upload multiple files to the server for processing through a Orange workflow.

    Args:   
        - filepaths (List[str]): List of file paths to be uploaded.   
        - file_ids (List[str]): List of unique file IDs corresponding to the files.
          The IDs should match the ones configured in the Orange workflow.  
        - opening_methods (List[str]): List of opening methods for the files.
          Choose from 'image_file', 'multiple_file', or 'file'.   
        - workflow_id (str): Unique ID of the workflow.
          The ID should match the one configured in the Orange workflow.   
        - expected_nb_outputs (int): Expected number of output files (depending on your workflow).

    Returns:   
        JSONResponse: Response message with the unique ID of the processing task."""
    file_ids = make_list(file_ids)
    opening_methods = make_list(opening_methods)
    filepaths = make_list(filepaths)
    if len(filepaths) != len(file_ids) or len(file_ids) != len(opening_methods):
        raise HTTPException(status_code=400, detail="Number of file paths, file IDs, and opening methods must match.")

    file_entries: List[Dict[str, Any]] = []
    for filepath, file_id, opening_method in zip(filepaths, file_ids, opening_methods):
        if opening_method not in ["image_file", "multiple_file", "file"]:
            raise HTTPException(status_code=400, detail="Invalid opening method provided.")
        
        file_path: Path = Path(filepath)
        if not file_path.exists():
            raise HTTPException(status_code=404, detail=f"File not found: {filepath}")

        with file_path.open('rb') as f:
            content: bytes = f.read()

        file_hash: str = hash_file_content(content)
        file_entries.append({
            'input_filename': str(file_path),
            'file_id': file_id,
            'file_hash': file_hash,
            'opening_method': opening_method
        })

    unique_id, output_folder = generate_unique_output_folder(output_directory)

    waiting_queue.add({
        'unique_id': unique_id,
        'workflow_id': workflow_id,
        'file_entries': file_entries,
        'output_folder': str(output_folder),
        'expected_nb_outputs': expected_nb_outputs,
        'text_inputs': text_inputs
    })

    return JSONResponse(content={"message": "Files queued for processing", "unique_id": unique_id})

@app.get("/retrieve-outputs/{unique_id}", response_model=None)
async def retrieve_outputs(unique_id: str, file_id: str = ""):
    """
    Retrieve the output files for a given unique ID. By default, a zip of all files will be returned.
    If a specific output filename is provided, only that file will be returned.   
    **IMPORTANT** : If the processing is not complete, the method will return a 404 error. You have to keep calling this method until the processing is complete.

    Args:     
        - unique_id (str): Unique ID of the processing task.  
        - file_id (str): Optional file ID to retrieve a specific file. If not provided, a zip of all files will be returned. 

    Returns:  
        FileResponse | JSONResponse: Response with the output file(s) for download.
    """
    output_folder = output_directory / unique_id
    
    # Check if the processing is complete by checking the presence of the "done" file
    if (output_folder / "done").exists():
        all_files = list(output_folder.glob('*'))
        
        # Remove 'done' and 'output.zip' files from the list
        for file in [output_folder / "done", output_folder / "output.zip"]:
            if file.exists():
                all_files.remove(file)

        # If a specific file_id is provided, search for it in the output folder
        if file_id:
            for file in all_files:
                if file_id in file.name:
                    return FileResponse(str(file), media_type='application/octet-stream', filename=file.name)
            return JSONResponse(content={"message": f"File with ID {file_id} not found."}, status_code=404)

        # If no specific file_id is specified, handle the retrieval of multiple or single files
        if len(all_files) == 1:
            # Return the single file if only one file is present
            output_file = all_files[0]
            return FileResponse(str(output_file), media_type='application/octet-stream', filename=output_file.name)
        elif len(all_files) > 1:
            # Create a zip of all the output files for download
            output_zip: Path = output_folder / "output.zip"
            zip_folder(output_folder, output_zip)
            return FileResponse(str(output_zip), media_type='application/zip', filename=f"output.zip")
        else:
            return JSONResponse(content={"message": "No files found in the output folder."}, status_code=404)

    elif output_folder.exists():
        return JSONResponse(content={"message": "Processing is not complete."}, status_code=404)
    else:
        return JSONResponse(content={"message": "Unique ID not found."}, status_code=404)

@app.get("/ping")
async def ping() -> JSONResponse:
    return JSONResponse(content={"message": "pong"})



# Background Processing Task
async def process_files_queue() -> None:
    """
    Background task to process files from the waiting queue.
    This task will check the waiting queue for new files and move them to the in-process queue.
    It will then wait for the expected number of output files to be generated by the workflow.
    """

    while True:
        if not waiting_queue.queue or len(in_process_queue.queue) >= MAX_PROCESSING_QUEUE_LENGTH:
            await asyncio.sleep(1)
            continue

        workflow_entry= waiting_queue.queue[0] # element en attente
        waiting_queue.remove(workflow_entry)
        in_process_queue.add(workflow_entry) # element en process
        expected_nb_outputs: int = workflow_entry['expected_nb_outputs']
        output_folder: Path = Path(workflow_entry['output_folder'])
        
        # Wait for the expected number of output files to be generated by the workflow
        start_time: float = time.time()
        output_folder: Path = Path(workflow_entry['output_folder'])
        while time.time() - start_time < TIMEOUT_LIMIT:
            if len(list(output_folder.glob('*'))) == expected_nb_outputs:
                break
            elif len(list(output_folder.glob('*'))) > expected_nb_outputs:
                raise Exception("Too many files found in the output folder. Error.")
            await asyncio.sleep(1)
        
        in_process_queue.remove(workflow_entry)
        (output_folder / "done").touch()


