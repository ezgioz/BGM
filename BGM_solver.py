def num_there(s):
    return any(i.isdigit() for i in s)


# +
def compute_case(expm):
    '''Evaluates welfare for the planner and the competitive equilibrium for various values of a specified parameter.
    
    Parameters
    ----------
    expm: dict
        Description of the experiment to perform. Contains several fields:
        - name: name of the experiment, the corresponding model file is expected to be model_*name*.yaml
        - param: name of the parameter to change
        - range: set of parameter values (min value, max value, N values)
    Returns
    -------
    df: pandas.DataFrame
        Each line contains:
        - parameter value
        - welfare for the planner optimum
        - welfare for the competitive equilibrium
    '''
        
    
    import pandas
    from dolo import yaml_import
    from numpy import exp, array, linspace, column_stack
    from dolo.algos.perturbations_higher_order import perturb
    from dolo.algos.simulations import tabulate
    from dolo.algos.steady_state import residuals
    from dolo.algos.steady_state import find_steady_state
    
    import sympy
    from sympy import  Symbol, solve
    
    freeparam = expm['freeparam']
    range = expm['range']
    modfile = expm['modfile']
    if 'fixedparam' in expm:
        fixedparam = expm['fixedparam']
        fixedparamval = expm['value']
        case = f"{expm['modfile']}_{expm['fixedparam']}{expm['value']}_{expm['freeparam']}".replace('.', '')
    else:
        case = f"{expm['modfile']}_{expm['freeparam']}".replace('.', '')

    # Import model    
    model = yaml_import('model_files/model_{}.yaml'.format(modfile))
    
    # Set fixed parameter declared above (Here we solve translog model twice with two different varphi values)
    if 'fixedparam' in expm:
        p2 = {expm['fixedparam']:expm['value']}
        model.set_calibration(**p2)

    # Set beta    
    beta = model.calibration['beta'];
    
    # Create necesarry objects to store results
    values_ce = []
    values_po = []

    nvals_ce = []
    nvals_po = []
    
    # create parameter range
    parm_vec = linspace(*range)
    
    # solve all calibrations (For the range of calibrations)
    
    for i in parm_vec:
        # Set calibrated parater value
        pp = {freeparam:i}
        model.set_calibration(**pp)
        
        
        # Solve for the competitive equilibrium
        model.set_calibration(po=0);
        calib_ce = find_steady_state(model);
        res = residuals(model,calib=calib_ce)
        
        
        if abs(sum(res['arbitrage'])) + abs(sum(res['transition'])) > 0.00001:
            #print('model', case, 'ME', freeparam, '=', i, '--> steady state cant be found: non-zero residuals')  
            dr_me_true = 0
            
            #calib_ce = calib_pre_ce
            #res = residuals(model,calib=calib_ce)
            #if abs(sum(res['arbitrage'])) + abs(sum(res['transition'])) > 0.00001:
            #    dr_me_true = 0   
            #else: 
            #    dr_po_true = 1
            #    dr_ce = perturb(model, order=2, steady_state=calib_ce);
            #    N_ce = model.calibration['N']

        else:    
            #print('model', case, 'ME', freeparam, '=', i, '--> steady state found')  
            dr_me_true = 1         
            dr_ce = perturb(model, order=2, steady_state=calib_ce);
            N_ce = model.calibration['N']

        # Solve for the social planner equilibrium
        model.set_calibration(po=1);
        calib_po = find_steady_state(model);
        res = residuals(model,calib=calib_po)
        
        if abs(sum(res['arbitrage'])) + abs(sum(res['transition'])) > 0.00001:
            dr_po_true = 0
            
            #print('model', case, 'ME', freeparam, '=', i, '--> steady state cant be found: non-zero residuals')  
            #calib_po = calib_pre_po
            #res = residuals(model,calib=calib_po)
            #if abs(sum(res['arbitrage'])) + abs(sum(res['transition'])) > 0.00001:
            #    dr_po_true = 0   
            #else:  
            #    dr_po_true = 1
            #    dr_po = perturb(model, order=2, steady_state=calib_po);
            #    N_po = model.calibration['N']

        else:
            #print('model', case, 'PO', freeparam, '=', i, '--> steady state found')  
            dr_po_true = 1
            dr_po = perturb(model, order=2, steady_state=calib_po);   
            N_po = model.calibration['N']
                    
        if dr_me_true == 1 and dr_po_true == 1:
            print('model', freeparam, '=', i, '--> steady state found for both models')
            # Initial point at which to evaluate the welfare
            eval_point = calib_po['states'].copy();
            # Change initial value of N
            eval_point[1]*=0.5 # to 50 % of its of its steady-state value
            #eval_point[1]= 1    # to 1
            
            # Evalueate welfare
            w_ce = dr_ce(eval_point)[1]
            w_po = dr_po(eval_point)[1]
                
            # Convert to consumption equivalent
            v_ce = exp((1-beta)*w_ce)
            v_po = exp((1-beta)*w_po)
            
            
        else:
            v_ce = float('NaN')
            v_po = float('NaN')
            
            N_ce = float('NaN')
            N_po = float('NaN')
            
        # Add to list of values
        values_ce.append(v_ce)
        values_po.append(v_po)
        
        nvals_ce.append(N_ce)
        nvals_po.append(N_po)
    
    #Construct dataframe
    columns = [h.format(case) for h in ['{}', '{}_po', '{}_ce', '{}_N_po', '{}_N_ce']]
    df = pandas.DataFrame( column_stack([parm_vec, values_po, values_ce, nvals_po, nvals_ce]), columns=columns)
    
    #compute gains
    df['{}_gain'.format(case)] = (df['{}_po'.format(case)]/df['{}_ce'.format(case)]-1)*100    
    return df



