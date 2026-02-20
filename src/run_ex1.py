from PyQt6.QtWidgets import QApplication
from PackageSources.Model import Cortex_Model_NeoNMM
from PackageSources.Computation.Loading import LoadSimul
from PackageSources.Computation.Filter import signalfilter_EEG
from PackageSources.Display.EEG_Viewer import EEG_Viewer
from PackageSources.Display.Spectrogram import Spectrogram_Viewer
import sys

def main():
    # 1) Model
    Model = Cortex_Model_NeoNMM.Cortex(Nb_NMM=1)

    # 2) Load saved simulation file (exists in src/SaveFiles)
    SaveFile_Name = r"SaveFiles/1NMM_alpha.txt"
    Model, List_Stim, List_ParamEvol = LoadSimul(FilePath=SaveFile_Name, Model=Model)

    # 3) Run simulation
    Fs = 1024
    T = 10
    LFPs, tp, Pulses, PSPs, ESs = Model.Compute_Time(
        T, Fs, Stim=List_Stim, List_ParamEvol=List_ParamEvol, Pre_Post=False
    )

    # 4) Optional filter for nicer plot
    LFPs = signalfilter_EEG(LFPs, Fs, ftype="bandpass", order=3, lowcut=1, highcut=80)

    # 5) Viewers (needs GUI)
    app = QApplication(sys.argv)

    ex0 = EEG_Viewer()
    ex0.setWindowTitle("LFPs")
    ex0.update(LFPs, Model.popColor, Model.popName, tp)
    ex0.showMaximized()

    ex3 = Spectrogram_Viewer()
    ex3.setWindowTitle("Spectrogram_Viewer")
    ex3.update(LFPs=LFPs, Names=Model.popName, Fs=Fs, plot1D2D=False, cut=1, Fmax=50, Fseg=0.5, Colors=Model.popColor)
    ex3.showMaximized()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
