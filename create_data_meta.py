import os
import argparse
import vitaldb as vdb

def calculate_len(file_path, use_pandas=False, track_names=[], header=False):
    if not use_pandas:
        with open(file_path, 'r') as f:
            if header:
                next(f)
            data_len = sum(1 for _ in f)
        
        f.close()
    
    else:
        load_tracks = track_names
        if len(track_names) == 0:
            load_tracks = None
        vdb_data = vdb.vital_recs(file_path, track_names=load_tracks, return_timestamp=False, return_datetime=True, return_pandas=True)
        data_len = len(vdb_data)
        del vdb_data
    
    return data_len

def create_data_meta(data_path, header=False):
    files_list = sorted(os.listdir(data_path), key=lambda x: int(x.split('.')[0]))

    vital_track_names = [
            'SNUADC/ART',
            'SNUADC/ECG_II',
            'SNUADC/ECG_V5',
            'SNUADC/PLETH',
            'Primus/CO2',
            'BIS/EEG1_WAV',
            'BIS/EEG2_WAV'
    ]

    total_rows = 0

    with open(f'{data_path}/data_meta.txt', 'w') as data_meta:
        for file in files_list:
            if file != "data_meta.txt" and len(file.split('.')) > 1:
                file_len = calculate_len(os.path.join(data_path, file), use_pandas=True, track_names=vital_track_names, header=header)

                total_rows += file_len
                
                data_meta.writelines([f"{file} {file_len}\n"])

                print(f"{file} {file_len}")
            
        data_meta.writelines([f"TOTAL {total_rows}"])
        print(f"TOTAL {total_rows}")

    data_meta.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Dataset Metadata")
    parser.add_argument('--data_path', type=str, default='data/', help='dataset folder path')
    args = parser.parse_args()

    data_path = args.data_path

    create_data_meta(data_path, header=True)