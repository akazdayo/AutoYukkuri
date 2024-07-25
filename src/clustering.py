from speechbrain.inference.speaker import SpeakerRecognition
from pprint import pprint
from pydub import AudioSegment
import glob
import os
import whisper
import sys


class SpeakerClustering:
    def __init__(self) -> None:
        self.verification = SpeakerRecognition.from_hparams(
            source="speechbrain/spkrec-ecapa-voxceleb",
            savedir="pretrained_models/spkrec-ecapa-voxceleb",
        )

    def triming(self, result, path) -> None:
        audio = AudioSegment.from_file(path)
        trim = None
        for i, x in enumerate(result["segments"]):
            trim = audio[int(x["start"]) * 1000 : int(x["end"]) * 1000]
            os.makedirs("./temp", exist_ok=True)
            trim.export(f"temp/{i}.wav", format="wav")

    def clustering(self, all_path):
        all_user = []
        chara_list = []
        for i in range(len(all_path)):
            appended = False
            if os.path.exists(all_path[i]) and os.path.getsize(all_path[i]) > 0:
                try:
                    for j in range(len(all_user)):
                        _, prediction = self.verification.verify_files(
                            all_user[j], all_path[i]
                        )
                        if prediction:
                            # all_user[j].append(all_path[i])
                            chara_list.append(j)
                            appended = True
                            break
                    if not appended:
                        all_user.append(all_path[i])
                        chara_list.append(len(all_user) - 1)
                except Exception as e:
                    print(
                        f"ファイル処理中にエラーが発生しました: {all_path[i]}, エラー: {e}"
                    )
                    sys.exit(1)
            else:
                print("ファイルが存在しません", str(i))
        print("終了")
        return (all_user, chara_list)

    def run_whisper(self, use_model, path):
        model = whisper.load_model(use_model)
        result = model.transcribe(
            path,  # ファイルパス
            verbose=True,
            language="ja",
        )
        return result


if __name__ == "__main__":
    filepath = "./content/voice.wav"
    speaker = SpeakerClustering()
    data = speaker.run_whisper("small", filepath)
    speaker.triming(data, filepath)
    files = glob.glob(".\\temp\\*.wav")
    # print(files)
    users = speaker.clustering(files)
    pprint(users)
