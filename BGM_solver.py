def num_there(s):
    return any(i.isdigit() for i in s)


# +
def compute_case(expm):
    '''Evaluates welfare for the planner and the competitive equilibrium for various values of a specified parameter.
    
    Parameters
    ----------
    expm: dict
        Description of the experiment to perform. Contains several fields:
        - modfile: name of the experiment, the corresponding model file is expected to be model_*name*.yaml
        - freeparam: name of the parameter to change
        - range: set of parameter values (min value, max value, N values)
        - fixedparam: name of the fixed parameter (value different from model calibration)
        - value: value of fixed parameter
    Returns
    -------
    df: pandas.DataFrame
        Each line contains:
        - parameter value
        - welfare for the planner optimum
        - welfare for the competitive equilibrium
        - welfare gains
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
    
    ################################
    # Set information for each model
    ################################
    
    ### Code below will set information for each case and name output variables/files accordingly
    # If model is CES to be solved for free parameter xi, declarre in Produce graphs notebook:
    # dict(modfile='ces', freeparam='xi', range=(0.2,1.0,N))
    # output files will be names as 'BGM_' 
    #
    
    ### Model file name, Freeparam and range --> we will solve model for each value of the declared interval
    freeparam = expm['freeparam']
    range = expm['range']
    modfile = expm['modfile']
    
    ### Fixed param--> if any, default is from model calibration in the yaml file
    # (Here we solve translog model twice with two different varphi values so fixed parameter exist)
    if 'fixedparam' in expm:
        fixedparam = expm['fixedparam']
        fixedparamval = expm['value']
        case = f"{expm['modfile']}_{expm['fixedparam']}{expm['value']}_{expm['freeparam']}".replace('.', '')
    else:
        case = f"{expm['modfile']}_{expm['freeparam']}".replace('.', '')
    
    
    #######################
    # Solving for each model
    #########################
    
    # Import model    
    model = yaml_import('model_files/model_{}.yaml'.format(modfile))
    
    # Set fixed parameter declared above 
    if 'fixedparam' in expm:
        p2 = {expm['fixedparam']:expm['value']}
        model.set_calibration(**p2)

    # Set beta    
    beta = model.calibration['beta'];
    
    # Create necesarry objects to store results -> This will store consumption equivalent
    # of welfare for competetitive eq. and planner eq.
    values_ce = []
    values_po = []
    
    # create parameter range
    parm_vec = linspace(*range)
    
    # solve all calibrations (For the range of calibrations)
    
    for i in parm_vec:
        # Set calibrated parater value
        pp = {freeparam:i}
        model.set_calibration(**pp)
        
        #######################################
        # Solve for the competitive equilibrium
        ######################################### 
        model.set_calibration(po=0);
        calib_ce = find_steady_state(model);
        res = residuals(model,calib=calib_ce)
        
        
        if abs(sum(res['arbitrage'])) + abs(sum(res['transition'])) > 0.00001:
            print('model', case, 'ME', freeparam, '=', i, '--> steady state cant be found: non-zero residuals')  
            dr_me_true = 0

        else:    
            dr_me_true = 1         
            dr_ce = perturb(model, order=2, steady_state=calib_ce);

        ##########################################    
        # Solve for the social planner equilibrium
        ########################################## 
        model.set_calibration(po=1);
        calib_po = find_steady_state(model);
        res = residuals(model,calib=calib_po)
        
        if abs(sum(res['arbitrage'])) + abs(sum(res['transition'])) > 0.00001:
            dr_po_true = 0
            #print('model', case, 'ME', freeparam, '=', i, '--> steady state cant be found: non-zero residuals')  
            

        else:
            dr_po_true = 1
            dr_po = perturb(model, order=2, steady_state=calib_po);   
        
        # If model is solved correctly for both cases
        # compute welfare and gains for that parameter value
        
        if dr_me_true == 1 and dr_po_true == 1:
            print('model', freeparam, '=', i, '--> Bengi is a looser')
            
            # Initial point at which to evaluate the welfare (common for both models!)
            eval_point = calib_po['states'].copy();
            
            # Change initial value of N
            eval_point[1]*=0.5 # to 50 % of its of its steady-state value
            #eval_point[1]= 1    # to 1
            
            # Evalueate welfare at this point (same point) for both ce and po
            w_ce = dr_ce(eval_point)[1]
            w_po = dr_po(eval_point)[1]
                
            # Convert to consumption equivalent
            v_ce = exp((1-beta)*w_ce)
            v_po = exp((1-beta)*w_po)
            
            
        else: #If model is not solved for both cases, set it to NaN
            v_ce = float('NaN')
            v_po = float('NaN')
            
            
        # Add to list of values
        values_ce.append(v_ce)
        values_po.append(v_po)
        
    #Construct dataframe -> Create the table with param value, cons. eq. of welfare for each 
    columns = [h.format(case) for h in ['{}', '{}_po', '{}_ce']]
    df = pandas.DataFrame( column_stack([parm_vec, values_po, values_ce]), columns=columns)
    
    #compute gains -> compute gains and append matrix
    df['{}_gain'.format(case)] = (df['{}_po'.format(case)]/df['{}_ce'.format(case)]-1)*100    
    return df



