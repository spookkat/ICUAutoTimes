import argparse
import vitaldb as vdb
import os

def vital_to_csv_file(file_path, out_file_path, track_names=[]):
    load_tracks = track_names
    if len(track_names) == 0:
        load_tracks = None
    vdb_data = vdb.vital_recs(file_path, track_names=load_tracks, return_timestamp=True, return_datetime=False, return_pandas=True)
    vdb_data = vdb_data.fillna(method='ffill', axis=0).fillna(method='bfill', axis=0)
    vdb_data = vdb_data.rename(columns={'Time': 'date'})
    vdb_data.to_csv(out_file_path, index=False)

def vital_to_csv_folder(folder_path, out_folder_path, track_names=[]):
    file_list = os.listdir(folder_path)
    os.makedirs(out_folder_path, exist_ok=True)
    for filename in file_list:
        out_file_name = f"{filename.split('.')[0]}.csv"
        vital_to_csv_file(os.path.join(folder_path, filename), os.path.join(out_folder_path, out_file_name), track_names)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Dataset Conversion")
    parser.add_argument('--data_folder_path', type=str, default='data/', help='dataset folder path')
    parser.add_argument('--data_output_path', type=str, default='out_data/', help='dataset folder path')
    args = parser.parse_args()

    data_folder_path = args.data_folder_path
    data_output_path = args.data_output_path

    vital_track_names = [
        'SNUADC/ART',
        'SNUADC/ECG_II',
        'SNUADC/ECG_V5',
        'SNUADC/PLETH',
        'Primus/CO2',
        'BIS/EEG1_WAV',
        'BIS/EEG2_WAV'
    ]

    vital_to_csv_folder(data_folder_path, data_output_path, vital_track_names)