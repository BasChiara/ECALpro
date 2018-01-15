#include <memory>

#include "TFitResult.h"

#include "RooRealVar.h"
#include "RooFitResult.h"

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "CalibCode/CalibTools/interface/EcalRegionalCalibration.h"
#include "CalibCode/CalibTools/interface/EcalCalibTypes.h"


enum calibGranularity{ xtal, tt, etaring };

struct Pi0FitResult {
  RooFitResult* res;
  float S;     // signal in 3 sigma region
  float Serr;
  float B;     // bkg in 3 sigma region
  float Berr; 
  float  SoB;  // S/B
  float  SoBerr;
  float chi2;
  //float chi2red; // reduced chi2
  int dof; // after subtracting number of model parameters
  int nFitParam;  // number of parameters in the fit model
  float probchi2; // after subtracting fit parameters 
};

Float_t my2sideCrystalBall(double* x, double* par);
Float_t myLeftTailCrystalBall(double* x, double* par);

class FitEpsilonPlot : public edm::EDAnalyzer {
   public:
      enum FitMode{ Eta=0, Pt, GausPol3, GausEndpoint, Pi0EB, Pi0EE, EtaEB };
      explicit FitEpsilonPlot(const edm::ParameterSet&);
      ~FitEpsilonPlot();

      static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);


   private:
      virtual void beginJob() ;
      virtual void analyze(const edm::Event&, const edm::EventSetup&);
      virtual void endJob() ;

      virtual void beginRun(edm::Run const&, edm::EventSetup const&);
      virtual void endRun(edm::Run const&, edm::EventSetup const&);
      virtual void beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&);
      virtual void endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&);

      void loadEpsilonPlot(const std::string& filename);
      void loadEoverEtruePlot(const std::string& filename, const int whichPhoton);
      void saveCoefficients();
      void saveCoefficientsEoverEtrue(const bool isSecondGenPhoton);
      void IterativeFit(TH1F* h, TF1 & ffit); 
      void deleteEpsilonPlot(TH1F **h, int size);

      int getArrayIndexOfFoldedSMfromIetaIphi(int& ieta, int& iphi);
      int getArrayIndexOfFoldedSMfromDenseIndex(int& index);  
      Pi0FitResult FitMassPeakRooFit(TH1F* h,double xlo, double xhi, uint32_t HistoIndex, int ngaus=1, FitMode mode=Pi0EB, int niter=0, bool isNot_2010_=true);
      TFitResultPtr FitEoverEtruePeak(TH1F* h1, Bool_t isSecondGenPhoton, uint32_t HistoIndex, FitMode mode, Bool_t noDrawStatBox);

      // ----------member data ---------------------------

      EcalRegionalCalibration<EcalCalibType::Xtal> xtalCalib;
      EcalRegionalCalibration<EcalCalibType::EtaRing> etaCalib;
      EcalRegionalCalibration<EcalCalibType::TrigTower> TTCalib;
      EcalRegionalCalibrationBase *regionalCalibration_;    // use it for pi0 mass or first photon with E/overEtrue

      // for second photon with E/Etrue (MC only)
      // I create them with "regionalCalibration_g2_ = new EcalRegionalCalibration<EcalCalibType::Xtal>()" directly in the source
      /* EcalRegionalCalibration<EcalCalibType::Xtal> xtalCalib_g2; */
      /* EcalRegionalCalibration<EcalCalibType::EtaRing> etaCalib_g2; */
      /* EcalRegionalCalibration<EcalCalibType::TrigTower> TTCalib_g2; */
      EcalRegionalCalibrationBase *regionalCalibration_g2_; // use it for second gen photon with E/Etrue

      int currentIteration_;
      std::string outputDir_;
      std::string outfilename_;
      std::string calibTypeString_;
      std::string epsilonPlotFileName_;
      std::string calibMapPath_; 
      std::string Barrel_orEndcap_; 
      std::string fitFileName_;
      bool useFit_RooMinuit_;

      std::string EEoEB_; 
      bool isNot_2010_; 
      bool Are_pi0_; 
      bool StoreForTest_; 
      int inRangeFit_; 
      int finRangeFit_; 
      bool useMassInsteadOfEpsilon_;
      bool foldInSuperModule_;

      calibGranularity calibTypeNumber_;

      TH1F **epsilon_EB_h;  // epsilon distribution by region
      TH1F **epsilon_EE_h;  // epsilon distribution in EE

      // for E/Etrue with MC 
      bool isEoverEtrue_;
      TH1F **EoverEtrue_g1_EB_h;
      TH1F **EoverEtrue_g1_EE_h;
      TH1F **EoverEtrue_g2_EB_h;
      TH1F **EoverEtrue_g2_EE_h;
      std::map<int,TFitResultPtr> EBmap_fitresptr_g1;
      std::map<int,TFitResultPtr> EBmap_fitresptr_g2;
      std::map<int,TFitResultPtr> EEmap_fitresptr_g1;
      std::map<int,TFitResultPtr> EEmap_fitresptr_g2;

      TFile *inputEpsilonFile_;
      TFile *outfile_;
      TFile *outfileTEST_;

      std::vector<TH1F*> EoverEtrue_g1_EB_SM_hvec;  // 20(phi)*85(ieta) crystals in 1 SM
      std::vector<TH1F*> EoverEtrue_g2_EB_SM_hvec;  // 20(phi)*85(ieta) crystals in 1 SM

      std::map<int,float> EBmap_Signal;//#
      std::map<int,float> EBmap_Backgr;
      std::map<int,float> EBmap_Chisqu;
      std::map<int,float> EBmap_ndof;
      std::map<int,float> EBmap_mean;
      std::map<int,float> EBmap_mean_err;
      std::map<int,float> EBmap_sigma;
      std::map<int,float> EBmap_Snorm;
      std::map<int,float> EBmap_b0;
      std::map<int,float> EBmap_b1;
      std::map<int,float> EBmap_b2;
      std::map<int,float> EBmap_b3;
      std::map<int,float> EBmap_Bnorm;

      std::map<int,float> EEmap_Signal;
      std::map<int,float> EEmap_Backgr;
      std::map<int,float> EEmap_Chisqu;
      std::map<int,float> EEmap_ndof;
      std::map<int,float> EEmap_mean;
      std::map<int,float> EEmap_mean_err;
      std::map<int,float> EEmap_sigma;
      std::map<int,float> EEmap_Snorm;
      std::map<int,float> EEmap_b0;
      std::map<int,float> EEmap_b1;
      std::map<int,float> EEmap_b2;
      std::map<int,float> EEmap_b3;
      std::map<int,float> EEmap_Bnorm;





};



