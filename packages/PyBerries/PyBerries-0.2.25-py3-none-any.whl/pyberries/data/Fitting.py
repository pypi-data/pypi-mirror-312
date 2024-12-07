import inspect
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
from scipy.stats import sem

from ..stats import get_aic, get_bic, get_llf_


class Fit():

    def __init__(self, df_in, x: str, y: str, y_err: str = None, model=None, model_type: str = None,
                 groupby: str = 'Group', bootstrap_samples: int = 1, p0=None, param_format: str = 'long',
                 verbose: bool = False):

        assert model or model_type, 'Must provide either a model_type or a model function'
        assert param_format in ['long', 'wide'], \
            f'param_format "{param_format}" not recognised (must be "long" or "wide")'
        if model:
            self.model = model
            self.model_type = 'custom'
        else:
            self.model_type = model_type
            self.model = get_model(model_type)
        self.model_parameters = inspect.getfullargspec(self.model).args[1:]
        if p0:
            model_args = len(self.model_parameters)
            assert len(p0) == model_args, \
                f'Number of initial parameters ({len(p0)}) does not match number of model arguments ({model_args})'
        fit_parameters = pd.DataFrame(columns=['Group', 'Value', 'Error', 'Parameter'])
        llf = dict()
        aic = dict()
        bic = dict()
        df_out = pd.DataFrame()
        i = 0
        for name, data in df_in.groupby(groupby, observed=True, sort=False):
            groupName = '--'.join(map(str, name)) if isinstance(name, tuple) else str(name)
            flag = True
            if y_err:
                sigma = data[y_err]
            else:
                sigma = None
            if bootstrap_samples > 1:
                bootstrap_results = []
                fails = 0
                for boot_iteration in range(bootstrap_samples):
                    fit_data = data.copy().iloc[np.random.randint(len(data), size=len(data))]
                    try:
                        popt, _ = curve_fit(self.model, fit_data[x], fit_data[y], sigma=sigma,
                                            absolute_sigma=True, p0=p0)
                        bootstrap_results.append(popt)
                    except Exception:
                        fails += 1
                if verbose:
                    print(f'Group {name}: {fails} iterations failed')
                if bootstrap_results:
                    popt = np.median(bootstrap_results, axis=0)
                    popt_err = sem(bootstrap_results, axis=0)
                else:
                    flag = False
            else:
                try:
                    popt, _ = curve_fit(self.model, data[x], data[y], sigma=sigma, absolute_sigma=True, p0=p0)
                    popt_err = np.empty((len(popt))) * np.nan
                except Exception as e:
                    flag = False
                    if verbose:
                        print(f'Fit for dataset {name} failed: {e}')
            if flag:
                for k, param in enumerate(popt):
                    fit_parameters.loc[i] = {'Group': groupName,
                                             'Value': param,
                                             'Error': popt_err[k],
                                             'Parameter': self.model_parameters[k]
                                             }
                    i += 1
                data = data.assign(Fit=self.model(data[x], *popt),
                                   Residuals=lambda df: data[y] - df.Fit
                                   )
                llf[groupName] = get_llf_(data[y], data['Fit'])
                aic[groupName] = get_aic(data[y], data['Fit'], len(popt))
                bic[groupName] = get_bic(data[y], data['Fit'], len(popt))
                df_out = pd.concat([df_out, data], axis=0, ignore_index=True)
        fit_parameters[groupby] = (fit_parameters['Group'].str.split('--', expand=True))
        if param_format == 'wide':
            fit_parameters = (pd.pivot_table(fit_parameters, values=['Value', 'Error'],
                                             index=groupby, columns='Parameter')
                              .reset_index()
                              )
        self.data = df_out
        self.llf = llf
        self.aic = aic
        self.bic = bic
        self.parameters = fit_parameters
        self.groupby = groupby

    def __str__(self):
        return f'Fit with parameters: (model={self.model_type}, Groupby={self.groupby})'


def get_model(model_type=''):
    if model_type == 'monoexp_decay':
        def model(x, Amplitude, Rate):
            return Amplitude*np.exp(-Rate*x, dtype='float64')
    elif model_type == 'biexp_decay':
        def model(x, Amplitude_1, Rate_1, Amplitude_2, Rate_2):
            return Amplitude_1*np.exp(-Rate_1*x, dtype='float64') + Amplitude_2*np.exp(-Rate_2*x, dtype='float64')
    elif model_type == 'monoexp_decay_offset':
        def model(x, Amplitude, Rate, Offset):
            return Amplitude*np.exp(-Rate*x) + Offset
    elif model_type == 'linear':
        def model(x, Slope, Offset):
            return Slope*x + Offset
    return model
