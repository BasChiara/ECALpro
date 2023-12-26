#include "./ICfunctions.h"




void makeICratio_ZeeEp(
		 const string& outDir = "/eos/user/c/cbasile/www/CalibPi0_Run3/AlCaP0_2022BE_TestCalib_iter8to10/iter_2/2DMaps/ICmaps/Zee/",
		 const string& canvasSuffix = "ratioIC",
		 const string& inputFilePi0 = "/eos/user/c/cbasile/www/CalibPi0_Run3/AlCaP0_2022BE_TestCalib_iter8to10/iter_2/2DMaps/ICmaps/calibrationMaps.root",
		 const string& inputFileZee = "ICs_ZeeEp_2022/calibMap_Zee_357704.root",
		 const string& mapNamePi0 = "calibMap_EB",
		 const string& mapNameZee = "EB_ICs_Zee_357704",
		 const Double_t mapMin = 0.0,
		 const Double_t mapMax = 2.0,
		 const Int_t is_EB0_EEp1_EEm2 = 2, 
		 const string& canvasLabel1 = "IC set 1",
		 const string& canvasLabel2 = "IC set 2"
		 ) 
{

    TH1::SetDefaultSumw2();
    TH1::StatOverflows(kTRUE);

    gStyle->SetPalette(55, 0);  // 55:raibow palette ; 57: kBird (blue to yellow) ; 107 kVisibleSpectrum ; 77 kDarkRainBow          
    gStyle->SetNumberContours(101); // default is 20 

    TFile* inFilePi0 = TFile::Open(inputFilePi0.c_str(),"READ");
    if (!inFilePi0 || !inFilePi0->IsOpen()) {
        cout << "*******************************" << endl;
        cout << "Error opening file \"" << inputFilePi0 << "\".\nApplication will be terminated." << endl;
        cout << "*******************************" << endl;
        exit(EXIT_FAILURE);
    }

  TH2F *mapEB_pi0 = NULL;
  mapEB_pi0 = (TH2F*) inFilePi0->Get(mapNamePi0.c_str());
  if (!mapEB_pi0) {
    cout << "Error: could not get EE histogram. End of programme" << endl;
    exit(EXIT_FAILURE);
  }else cout << " got pi0 IC map "  << endl;
  mapEB_pi0->SetDirectory(0);
  inFilePi0->Close();
  
  TFile* inFileZee = TFile::Open(inputFileZee.c_str(),"READ");
    if (!inFileZee || !inFileZee->IsOpen()) {
        cout << "*******************************" << endl;
        cout << "Error opening file \"" << inputFileZee << "\".\nApplication will be terminated." << endl;
        cout << "*******************************" << endl;
        exit(EXIT_FAILURE);
    }

  TH2F *mapEB_Zee = NULL;
  mapEB_Zee = (TH2F*) inFileZee->Get(mapNameZee.c_str());
  if (!mapEB_Zee) {
    cout << "Error: could not get EE histogram. End of programme" << endl;
    exit(EXIT_FAILURE);
  }else cout << " got Zee IC map "  << endl;
  mapEB_Zee->SetDirectory(0);
  inFileZee->Close();

    TH2F* IC_ratio = (TH2F*)mapEB_pi0->Clone("IC_ratio_Pi0overZee");
    IC_ratio->SetTitle("ratio IC Pi0 [folded separately on EB+ EB- and normalized in #eta-ring] w.r.t. IC Zee ");
    divideEBmap(IC_ratio, mapEB_pi0, mapEB_Zee);

    Int_t xsizeCanvas = 1200;
    Int_t ysizeCanvas = 1.0 * xsizeCanvas * 171. / 360. + 0.1 *xsizeCanvas;
    auto c1 = new TCanvas("c1", "ratio canva", xsizeCanvas, ysizeCanvas);
    gStyle->SetOptStat(0);
    IC_ratio->Draw("COLZ0");
    c1->SaveAs("/eos/user/c/cbasile/www/CalibPi0_Run3/AlCaP0_2022BE_TestCalib_iter8to10/iter_2/2DMaps/ICmaps/Zee/IC_Pi0overZee_357704.png");
}
