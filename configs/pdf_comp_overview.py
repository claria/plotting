import util.callbacks as callbacks

def get_base_config():
    config = {}
    config['objects'] = {}
    config['store_json'] = False
    return config

def get_q2label(q2):
    q2_str = r'{:.2G}'.format(q2)
    if "E" in q2_str:
        base, exponent = q2_str.split('E')
        if base == '1':
            return r"10^{{{1}}}".format(base, int(exponent))
        else:
            return r"{0}\times 10^{{{1}}}".format(base, int(exponent))
    else:
        return q2_str



def get_config():
    configs = []
    partons = [0, 7, 8, 9]
    names = ['gluon', 'd valence quark', 'u valence quark', 'sea quarks']
    y_labels = ['$xg(x,Q^2\!)$', '$xd_{\mathrm{v}}(x,Q^2\!)$', '$xu_{\mathrm{v}}(x,Q^2\!)$', '$x\Sigma(x,Q^2\!)$',]
    q2s = [1.9, 10000]
    pdfset1 = "HFTD_HERA_V103_EIG"
    pdfset2 = "HFTD_HERACMSTDJETS_V103_EIG"

    pdf_label1 = "HERA DIS"
    pdf_label2 = "HERA DIS + CMS jets"
   
    for k, q2 in enumerate(q2s):
        config = get_base_config()
        config['ana_modules'] = ["PDFModule",'Multiply', 'Copy']
        config["plot_id"] =  []
        config["plot_order"] =  []
        config["input_pdfsets"] = []

        config['multiply'] = [
                              ('_{0}_0_totunc'.format(pdfset1), 0.2),
                              ('_{0}_0_totunc'.format(pdfset2), 0.2),
                              ('_{0}_9_totunc'.format(pdfset1), 0.2),
                              ('_{0}_9_totunc'.format(pdfset2), 0.2),
                ]

        config['copy_id'] = []
        config['combine_legend_entries'] = []

        for i, parton in enumerate(partons):

            config['copy_id'].append(("_{0}_{1}_totunc".format(pdfset1, partons[i]),"_{0}_{1}_totunc_line".format(pdfset1, partons[i])))
            config['copy_id'].append(("_{0}_{1}_totunc".format(pdfset2, partons[i]),"_{0}_{1}_totunc_line".format(pdfset2, partons[i])))

            config["plot_id"].append('_{0}_{1}_totunc'.format(pdfset1, partons[i]))
            config["plot_id"].append('_{0}_{1}_totunc_line'.format(pdfset1, partons[i]))
            config["plot_id"].append('_{0}_{1}_totunc'.format(pdfset2, partons[i]))
            config["plot_id"].append('_{0}_{1}_totunc_line'.format(pdfset2, partons[i]))
            config['plot_order'].append('_{0}_{1}_totunc'.format(pdfset1, partons[i]))
            config['plot_order'].append('_{0}_{1}_totunc'.format(pdfset2, partons[i]))
            config["combine_legend_entries"].append(("_{0}_{1}_totunc_line".format(pdfset1, partons[i]), "_{0}_{1}_totunc".format(pdfset1, partons[i])))
            config["combine_legend_entries"].append(("_{0}_{1}_totunc_line".format(pdfset2, partons[i]), "_{0}_{1}_totunc".format(pdfset2, partons[i])))
            config["input_pdfsets"].append(
                    ("{0}_{1}".format(pdfset1, partons[i]), {
                            "flavour": partons[i], 
                            "q2": q2s[k], 
                            "pdfset": pdfset1
                            }
                    ))
            config["input_pdfsets"].append(
                    ("{0}_{1}".format(pdfset2, partons[i]), {
                            "flavour": partons[i], 
                            "q2": q2s[k], 
                            "pdfset": pdfset2
                            }
                    ))

            config["objects"]["_{0}_{1}_totunc".format(pdfset1, partons[i])] = {
                "edgealpha": 1.0,
                "edgecolor": "auto",
                "style": "band",
                "rasterized": True,
                "capsize": 0, 
                "x_err": True, 
                "color": "_color0_",
                "linestyle": "",
                "label": "{0}".format(pdf_label1),
                "step": False,
                "cmap": "viridis",
                "zorder": 1.0,
                "obj": "null",
                "plot_datavals": False, 
                "marker": ".", 
                "alpha": 1.0, 
                "fill": True, 
                "y_err": True, 
                "axis": "ax"
            }
            config["objects"]["_{0}_{1}_totunc_line".format(pdfset1, partons[i])] = {
                "edgealpha": 1.0,
                "edgecolor": "auto",
                "style": "line",
                "rasterized": True,
                "capsize": 0, 
                "x_err": True, 
                "color": "black",
                "linestyle": "--",
                "linewidth": "1.0",
                "label": "{0}".format(pdf_label1),
                "step": False,
                "cmap": "viridis",
                "zorder": 1.0,
                "obj": "null",
                "plot_datavals": False, 
                "marker": ".", 
                "alpha": 1.0, 
                "fill": True, 
                "y_err": True, 
                "axis": "ax"
            }

            config["objects"]["_{0}_{1}_totunc".format(pdfset2, partons[i])] = {
                "edgealpha": 1.0,
                "edgecolor": "auto",
                "style": "band",
                "rasterized": True,
                "capsize": 0, 
                "x_err": True, 
                "color": "none", 
                "edgecolor": "_color2_", 
                "linestyle": "",
                "linewidth": "2.0",
                "label": "{0}".format(pdf_label2),
                "step": False,
                "cmap": "viridis",
                "zorder": 2.0,
                "obj": "null",
                "hatch": 'sllll', 
                "plot_datavals": False, 
                "marker": ".", 
                "alpha": 1.0, 
                "fill": True, 
                "y_err": True, 
                "axis": "ax"
            }
            config["objects"]["_{0}_{1}_totunc_line".format(pdfset2, partons[i])] = {
                "edgealpha": 1.0,
                "edgecolor": "auto",
                "style": "line",
                "rasterized": True,
                "capsize": 0, 
                "x_err": True, 
                "color": "none", 
                "color": "_color2_", 
                "linestyle": "--",
                "linewidth": "1.0",
                "label": "{0}".format(pdf_label2),
                "step": False,
                "cmap": "viridis",
                "zorder": 2.0,
                "obj": "null",
                "hatch": 'sllll', 
                "plot_datavals": False, 
                "marker": ".", 
                "alpha": 1.0, 
                "fill": False, 
                "y_err": True, 
                "axis": "ax"
            }


        config["y_lims"] = ["0.0", 1.0]
        config["x_lims"] = [1E-4, 0.9]
        config['x_axis_formatter'] = 'scientific'
        config["x_log"] =  True
        config["legend_loc"] = 'upper right'
        config["x_label"] = "$x$"
        config["y_label"] = '$xf(x,Q^2\!)$'
        config["ax_texts"] = [
                              's=$Q^2\!={0}\mathrm{{GeV}}^2$?_topright_'.format(get_q2label(q2)),
                              's=$0.2\cdot x\Sigma$?x=0.2|y=0.5|va=bottom|ha=right',
                              's=$0.2\cdot xg$?x=0.5|y=0.65|va=bottom|ha=right',
                              's=$xu_{\mathrm{v}}$?x=0.8|y=0.70|va=bottom|ha=right',
                              's=$xu_{\mathrm{d}}$?x=0.85|y=0.45|va=bottom|ha=right',
                              ] 
        config["output_path"] = 'pdfcomp_direct_overview_{0}.png'.format(q2)
        configs.append(config)

    return configs

# @callbacks.register('before_plot')
# def final_plot(**kwargs):
#     kwargs['mpl'].rcParams['legend.fontsize'] = 20
#     # kwargs['mpl'].rcParams['font.size'] = 20
