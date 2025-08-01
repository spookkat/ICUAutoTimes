import argparse
import vitaldb as vdb
import os

def vital_to_csv_file(file_path, out_file_path, track_names=[], write_meta=False, delete_original=False):
    load_tracks = track_names
    if len(track_names) == 0:
        load_tracks = None
    vdb_data = vdb.vital_recs(file_path, track_names=load_tracks, return_timestamp=True, return_datetime=False, return_pandas=True)
    vdb_data = vdb_data.fillna(method='ffill', axis=0).fillna(method='bfill', axis=0)
    vdb_data = vdb_data.rename(columns={'Time': 'date'})
    vdb_data.to_csv(out_file_path, index=False)
    vdb_len = len(vdb_data)
    del vdb_data

    if delete_original:
        try:
            os.remove(file_path)
            #print(f"File '{file_path}' deleted successfully.")
        except FileNotFoundError:
            print(f"Error: File '{file_path}' not found.")
        except Exception as e:
            print(f"An error occurred: {e}")

    if write_meta:
        return vdb_len

def vital_to_csv_folder(folder_path, out_folder_path, track_names=[], write_meta=False, delete_original=False):
    file_list = os.listdir(folder_path)
    os.makedirs(out_folder_path, exist_ok=True)
    total_len = 0
    if write_meta:
        data_meta = open(os.path.join(out_folder_path, 'data_meta.txt'), 'w')
    for filename in file_list:
        out_file_name = f"{filename.split('.')[0]}.csv"
        vdb_len = vital_to_csv_file(os.path.join(folder_path, filename), os.path.join(out_folder_path, out_file_name), track_names, write_meta, delete_original)
        if write_meta:
            if vdb_len:
                data_meta.writelines([f"{filename.split('.')[0]} {vdb_len}\n"])
                total_len += vdb_len
    
    if write_meta:
        data_meta.writelines([f"TOTAL {total_len}"])
        data_meta.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Dataset Conversion")
    parser.add_argument('--data_folder_path', type=str, default='data/', help='dataset folder path')
    parser.add_argument('--data_output_path', type=str, default='out_data/', help='dataset folder path')
    parser.add_argument('--write_meta', action='store_true', default=False, help='Should write meta data')
    parser.add_argument('--delete_original', action='store_true', default=False, help='Should delete original after writing files')
    args = parser.parse_args()

    data_folder_path = args.data_folder_path
    data_output_path = args.data_output_path
    write_meta = args.write_meta
    delete_original = args.delete_original

    vital_track_names = [
        'SNUADC/ART',
        'SNUADC/ECG_II',
        'SNUADC/ECG_V5',
        'SNUADC/PLETH',
        'Primus/CO2',
        'BIS/EEG1_WAV',
        'BIS/EEG2_WAV'
    ]

    vital_to_csv_folder(data_folder_path, data_output_path, vital_track_names, write_meta, delete_original)