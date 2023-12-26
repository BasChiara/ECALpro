#include "./ICfunctions.h"

using namespace ROOT;

std::map<TString, float> Lumi_w_2022 = {
        {"354780",0.081},
        {"356580",0.048},
        {"357059",0.038},
        {"357440",0.017},
        {"357704",0.816},
};
std::map<TString, float> Lumi_w_2022BE = {       
        {"354780", 0.1919},
        {"356580", 0.1125},
        {"357059", 0.0895},
        {"357440", 0.0404},
        {"357704", 0.5657},
};
std::map<TString, float> Lumi_w_2022FG = {
        {"354780",0.},
        {"356580",0.},
        {"357059",0.},
        {"357440",0.},
        {"357704",1.},
};

void makeICmap_ZeeEp( TString inputFile_Zee = "ic354780.csv",
                      TString since_run = "354780",
                      TString ICsource = "hnsEtascale",
                      TString out_path = "./",
                      TString eosDir = "/eos/user/c/cbasile/www/CalibPi0_Run3/AlCaP0_2022BE_TestCalib_iter8to10/iter_2/2DMaps/ICmaps/"
)
{
    ROOT::EnableImplicitMT();
    gStyle->SetPalette(55, 0);  // 55:raibow palette ; 57: kBird (blue to yellow) ; 107 kVisibleSpectrum ; 77 kDarkRainBow                          
    gStyle->SetNumberContours(101); // default is 20

    // Zee intercalibration method
    TString intercalib_method = "Zee_"+ICsource+"_"+since_run;

    // make a TTree with thw itercalibration coefficients 
    RDataFrame IC_df_pre = ROOT::RDF::MakeCsvDataFrame(inputFile_Zee);
    std::cout << " created RDataFrame with number of entries : " << *(IC_df_pre.Count()) << std::endl;
    auto IC_df = IC_df_pre.Define("coeff_Lw22_", Form("coeff_*%f", Lumi_w_2022[since_run]))
                        .Define("coeff_LwBE_", Form("coeff_*%f", Lumi_w_2022BE[since_run]))
                        .Define("coeff_LwFG_", Form("coeff_*%f", Lumi_w_2022FG[since_run]));

    IC_df.Filter("iz_ == 0")
            .Snapshot("calibMap_"+intercalib_method+"_EB", out_path+"calibMap_"+intercalib_method+"_EB.root" );
    IC_df.Filter("fabs(iz_) == 1")
            .Snapshot("calibMap_"+intercalib_method+"_EE", out_path+"calibMap_"+intercalib_method+"_EE.root");
    
    // draw and save the IC-maps for EB and EE
    // BARREL
    int nBins_eta = 171, nBins_phi = 360;
    double eta_low = -85.5, eta_high = 85.5, phi_low = 0.5, phi_high = 360.5, IC_low = 0.1, IC_high = 2.;
    auto EB_map = IC_df.Filter("iz_ == 0")
                        .Profile2D({"EB_ICs_" + intercalib_method, " EB map " + intercalib_method, nBins_phi, phi_low, phi_high, nBins_eta, eta_low, eta_high, IC_low, IC_high}, "iphi_", "ieta_", "coeff_");
    IC_low = IC_df.Filter("iz_ == 0").Min("coeff_").GetValue(); 
    IC_high = IC_df.Filter("iz_ == 0").Max("coeff_").GetValue(); 
    std::cout << " IC max " << IC_high << std::endl;
    EB_map->GetZaxis()->SetRangeUser(std::max(0.4, IC_low),std::min(1.6, IC_high));
    auto EB_map_Lw22 = IC_df.Filter("iz_ == 0")
                        .Profile2D({"EB_ICs_" + intercalib_method + "_22", " EB map Lumi-weight 2022 " + intercalib_method, nBins_phi, phi_low, phi_high, nBins_eta, eta_low, eta_high, IC_low, IC_high}, "iphi_", "ieta_", "coeff_Lw22_");
    auto EB_map_LwBE = IC_df.Filter("iz_ == 0")
                        .Profile2D({"EB_ICs_" + intercalib_method + "_22BE", " EB map Lumi-weight 2022(BE) " + intercalib_method, nBins_phi, phi_low, phi_high, nBins_eta, eta_low, eta_high, IC_low, IC_high}, "iphi_", "ieta_", "coeff_LwBE_");
    auto EB_map_LwFG = IC_df.Filter("iz_ == 0")
                        .Profile2D({"EB_ICs_" + intercalib_method + "_22FG", " EB map Lumi-weight 2022(FG) " + intercalib_method, nBins_phi, phi_low, phi_high, nBins_eta, eta_low, eta_high, IC_low, IC_high}, "iphi_", "ieta_", "coeff_LwFG_");
    
    
    // ENDACP
    auto EEp_map = IC_df.Filter("iz_ == 1")
                        .Profile2D({"EEp_ICs_" + intercalib_method, " EE+ map " + intercalib_method, 100, 0.5, 100.5, 100, 0.5, 100.5, 0., 2.}, "iphi_", "ieta_", "coeff_");
    auto EEp_map_Lw22 = IC_df.Filter("iz_ == 1")
                        .Profile2D({"EEp_ICs_" + intercalib_method  + "_22", " EE+ map Lumi-weight 2022 " + intercalib_method, 100, 0.5, 100.5, 100, 0.5, 100.5, 0., 2.}, "iphi_", "ieta_", "coeff_Lw22_");
    auto EEp_map_LwBE = IC_df.Filter("iz_ == 1")
                        .Profile2D({"EEp_ICs_" + intercalib_method  + "_22BE", " EE+ map Lumi-weight 2022(BE) " + intercalib_method, 100, 0.5, 100.5, 100, 0.5, 100.5, 0., 2.}, "iphi_", "ieta_", "coeff_LwBE_");
    auto EEp_map_LwFG = IC_df.Filter("iz_ == 1")
                        .Profile2D({"EEp_ICs_" + intercalib_method  + "_22FG", " EE+ map Lumi-weight 2022(FG) " + intercalib_method, 100, 0.5, 100.5, 100, 0.5, 100.5, 0., 2.}, "iphi_", "ieta_", "coeff_LwFG_");
    
    auto EEm_map = IC_df.Filter("iz_ == -1")
                        .Profile2D({"EEm_ICs_" + intercalib_method, " EE- map " + intercalib_method, 100, 0.5, 100.5, 100, 0.5, 100.5, 0., 2.}, "iphi_", "ieta_", "coeff_");
    auto EEm_map_Lw22 = IC_df.Filter("iz_ == -1")
                        .Profile2D({"EEm_ICs_" + intercalib_method  + "_22", " EE- map Lumi-weight 2022 " + intercalib_method, 100, 0.5, 100.5, 100, 0.5, 100.5, 0., 2.}, "iphi_", "ieta_", "coeff_Lw22_");
    auto EEm_map_LwBE = IC_df.Filter("iz_ == -1")
                        .Profile2D({"EEm_ICs_" + intercalib_method  + "_22BE", " EE- map Lumi-weight 2022(BE) " + intercalib_method, 100, 0.5, 100.5, 100, 0.5, 100.5, 0., 2.}, "iphi_", "ieta_", "coeff_LwBE_");
    auto EEm_map_LwFG = IC_df.Filter("iz_ == -1")
                        .Profile2D({"EEm_ICs_" + intercalib_method  + "_22FG", " EE- map Lumi-weight 2022(FG) " + intercalib_method, 100, 0.5, 100.5, 100, 0.5, 100.5, 0., 2.}, "iphi_", "ieta_", "coeff_LwFG_");
    


    Int_t xsizeCanvas = 1200;
    Int_t ysizeCanvas = 1.0 * xsizeCanvas * 171. / 360. + 0.1 *xsizeCanvas;

    auto c1 = new TCanvas("c1", "profile ICs for " + intercalib_method, xsizeCanvas, ysizeCanvas);
    gStyle->SetOptStat(0);
    EB_map->DrawClone("colz");
    c1->SaveAs(eosDir+ "EBmap_"+intercalib_method+".png");
    c1->SaveAs(eosDir+ "EBmap_"+intercalib_method+".pdf");
    ysizeCanvas = xsizeCanvas;
    auto c2 = new TCanvas("c2", "profile ICs for " + intercalib_method, xsizeCanvas, ysizeCanvas);
    EEp_map->DrawClone("colz");
    c2->SaveAs(eosDir+ "EEp_map"+intercalib_method+".png");
    c2->SaveAs(eosDir+ "EEp_map"+intercalib_method+".pdf");
    EEm_map->DrawClone("colz");
    c2->SaveAs(eosDir+ "EEm_map"+intercalib_method+".png");
    c2->SaveAs(eosDir+ "EEm_map"+intercalib_method+".pdf");

    TFile* outMap = TFile::Open(out_path+"h_calibMap_"+intercalib_method+".root", "RECREATE");
    if (!outMap->IsOpen()){
        cout << "Error opening file \"" << outMap << "\".\nApplication will be terminated." << endl;
         exit(EXIT_FAILURE);
    }
    EB_map->Write();
    EB_map_Lw22->Write();
    EB_map_LwBE->Write();
    EB_map_LwFG->Write();
    EEp_map->Write();
    EEp_map_Lw22->Write();
    EEp_map_LwBE->Write();
    EEp_map_LwFG->Write();
    EEm_map->Write();
    EEm_map_Lw22->Write();
    EEm_map_LwBE->Write();
    EEm_map_LwFG->Write();
    outMap->Close();
   

}//makeICmap_ZeeEp
