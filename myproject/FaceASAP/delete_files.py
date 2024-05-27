import os
import shutil

def delete_all_files_in_directory(directory):
    if os.path.exists(directory):
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f'Failed to delete {file_path}. Reason: {e}')

if __name__ == "__main__":
    encodings_dir = os.path.join('media', 'encodings')
    videos_dir = os.path.join('media', 'videos')
    delete_all_files_in_directory(encodings_dir)
    delete_all_files_in_directory(videos_dir)
