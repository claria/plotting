
def get_base_config():
    config = {}
    config['objects'] = {}
    config['store_json'] = False
    return config

def get_config():
    rap_bins = ['yb0ys0','yb0ys1','yb0ys2','yb1ys0','yb1ys1','yb2ys0']
    configs = []
    for rap_bin in rap_bins:
        config = get_base_config()
        config['ana_modules'] = [ "Multiply", 
                                  "Normalize", 
                                  "Ratio", 
                                  "ReBinning"
                                ]
        # config["normalize"] = [("dataunf", "width")]
        config["normalize"] = [
                ('nloct14', 50000),
                ('unf_truth', 'width'),
                ('unf_measured', 'width'),
                ]
        config["multiply"] = [
                              ("nloct14", "_np"),
                              ]
        config["ratio"] = [
                           ["unf_measured", "unf_truth"],
                           ["nloct14", "unf_truth"],
                           ["unf_truth", "unf_truth"],
                          ] 

        # config["data_lims"] = [('all', { 'min' : '_{0}_xmin_'.format(rap_bin), 'max' : '_{0}_xmax_'.format(rap_bin)})]
        config["data_lims"] = []
        config["to_tgraph"] = [
                               "nloct14"] 
        config['plot_order'] = ['dataunf_stat', 'dataunf_syst', 'nloct14']


        config['objects']["_np"] = {
            "input": "~/dust/dijetana/plot/plots/np_factors_calc_{0}.root?res_np_factor".format(rap_bin)
        } 
        config['objects']["unf_truth"] = {
            "alpha": 0.5, 
            "color": "auto", 
            "edgecolor": "auto", 
            "input": "~/dust/dijetana/ana/CMSSW_7_2_3/unf_DATA_NLO.root?{0}/h_ru_truth".format(rap_bin), 
            "label": "Unf truth", 
            "linestyle": "", 
            "marker": ".", 
            "plot": True, 
            "step": True, 
            "style": "line", 
            "x_err": True, 
            "y_err": True, 
            "zorder": 1.0
        } 
        config['objects']["unf_measured"] = {
            "alpha": 0.5, 
            "color": "auto", 
            "edgecolor": "auto", 
            "input": "~/dust/dijetana/ana/CMSSW_7_2_3/unf_DATA_NLO.root?{0}/h_ru_measured".format(rap_bin), 
            "label": "Unf Measured", 
            "linestyle": "", 
            "marker": ".", 
            "plot": True, 
            "step": True, 
            "style": "line", 
            "x_err": True, 
            "y_err": True, 
            "zorder": 1.0
        } 

        config['objects']["nloct14"] = {
            "alpha": 0.5, 
            "color": "auto", 
            "edgecolor": "auto", 
            "input": "~/dust/dijetana/ana/CMSSW_7_2_3/PTAVG_YBYS_NLO.root?{0}/CT14nlo_xs".format(rap_bin), 
            "label": "NLOxNP (CT14)", 
            "linestyle": "", 
            "marker": ".", 
            "plot": True, 
            "step": True, 
            "style": "line", 
            "x_err": True, 
            "y_err": True, 
            "zorder": 1.0
        } 
        config["y_lims"] = ["0.0", "2.0"]
        # config["x_lims"] = ["_{0}_xmin_".format(rap_bin),"_{0}_xmax_".format(rap_bin)]
        config['x_lims'] = [30., 3000.]
        config["x_log"] =  True
        config["y_log"] =  False
        config["legend_loc"] = 'upper right'
        config["x_label"] = "$p_\\mathrm{T,avg}$ (GeV)"
        config["y_label"] = "Ratio to NLO$\otimes$NP (CT14)?_center_"
        config["ax_hlines"] = [
                {'y' : 1.0, 'color' : 'black', 'linewidth' : 1.0, 'linestyle' : '--'}
                ]
        config["ax_texts"] = [
                              '_{0}_?_upperleft_'.format(rap_bin), 
                              '_20fb_'] 

        config["output_path"] = 'unf_nlo_check_{0}.png'.format(rap_bin)
        configs.append(config)

    return configs

