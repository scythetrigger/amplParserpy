# Standard Libraries

# Third-Party Libraries

# Information
__author__ = 'Nicholas Parham'
__copyright__ = ''
__credits__ = ['Nicholas Parham']
__license__ = 'Apache Software License'
__version__ = '0.0.3'
__maintainer__ = 'Nicholas Parham'
__email__ = 'nick-99@att.net'
__status__ = 'Dev'

# AMPL REST API Raw Console Output Parser

masterFile = '''
print '---Start Report---';

print '---Start Solve---';
#solve;
print '---End Solve---';

print '---Start Variables---';
print 'name[index]|value';
for {i in 1.._nvars}
    print _varname[i] & '|' & _var[i];
print '---End Variables---';

print '---Start Objectives---';
print 'name|value';
for {i in 1.._nobjs}
    print _objname[i] & '|' & _obj[i];
print '---End Objectives---';

print '---Start amplTimes---';
print 'name|value|description';
print 'elapsed|' & _ampl_elapsed_time & '|elapsed seconds since the start of the AMPL process';
print 'system|' & _ampl_system_time & '|system CPU seconds used by the AMPL process itself';
print 'user|' & _ampl_user_time & '|user CPU seconds used by the AMPL process itself';
print 'total|' & _ampl_time & '|_ ampl _ system _ time + _ ampl _ user _ time';
print '---End amplTimes---';

print '---Start shellTimes---';
print 'name|value|description';
print 'elapsed|' & _shell_elapsed_time & '|elapsed seconds for most recent shell command';
print 'system|' & _shell_system_time & '|system CPU seconds used by most recent shell command';
print 'user|' & _shell_user_time & '|user CPU seconds used by most recent shell command';
print 'total|' & _shell_time  & '|_ shell _ system _ time + _ shell _ user _ time';
print '---End shellTimes---';

print '---Start solveTimes---';
print 'name|value|description';
print 'elapsed|' & _solve_elapsed_time & '|elapsed seconds for most recent solve command';
print 'system|' & _solve_system_time & '|system CPU seconds used by most recent solve command';
print 'user|' & _solve_user_time & '|user CPU seconds used by most recent solve command';
print 'total|' & _solve_time & '|_ solve _ system _ time + _ solve _ user _ time';
print '---End solveTimes---';

print '---Start totalShellTimes---';
print 'name|value|description';
print 'elapsed|' & _total_shell_elapsed_time & '|elapsed seconds used by all shell commands';
print 'system|' & _total_shell_system_time & '|system CPU seconds used by all shell commands';
print 'user|' & _total_shell_user_time & '|user CPU seconds used by all shell commands';
print 'total|' & _total_shell_time & '|_ total _ shell _ system _ time + _ total _ shell _ user _ time';
print '---End totalShellTimes---';

print '---Start totalSolveTimes---';
print 'name|value|description';
print 'elapsed|' & _total_solve_elapsed_time & '|elapsed seconds used by all solve commands';
print 'system|' & _total_solve_system_time & '|system CPU seconds used by all solve commands';
print 'user|' & _total_solve_user_time & '|user CPU seconds used by all solve commands';
print 'total|' & _total_solve_time & '|';
print '---End totalSolveTimes---';

print '---End Report---';
'''

def addReport(runFile):
    # takes in AMPL runFile and appends code to create a report
    # return a runFile
    reportCode = masterFile
    if 'solve;' not in runFile: # FIXME: make more advanced regex
        runFile += reportCode.replace('#solve;', 'solve;')
    else:
        runFile += reportCode
    
    return runFile



def removeReport(content): # not tested
    # takes in raw AMPL console output and returns it without report
    # return raw AMPL console output
    lines = content.split('\n')
    
    content = lines[:lines.index('---Start Report---') + 1] + lines[lines.index('---End Report---'):]
    content = '\n'.join(lines)
    
    return content



def parseReport(content):
    # takes in raw AMPL console output and returns a JSON solution
    output = {}
    lines = content.split('\n')
    
    # parse variables
    variables = {}
    data = lines[lines.index('---Start Variables---') + 2:lines.index('---End Variables---')]
    for datum in data:
        datum = datum.strip()
        name, value = datum.split('|')
        crumbs = name.split('[')
        name = crumbs[0]
        index = crumbs[1].replace('[', '').replace(']', '')
        if name not in variables.keys():
            variables[name] = {}
        variables[name][index] = float(value)
         
    # parse objectives
    objectives = {}
    data = lines[lines.index('---Start Objectives---') + 2:lines.index('---End Objectives---')]
    for datum in data:
        datum = datum.strip()
        name, value = datum.split('|')
        objectives[name] = float(value)
    
    # parse time metrics
    amplTimes = {}
    amplTimeDescriptions = {}
    data = lines[lines.index('---Start amplTimes---') + 2:lines.index('---End amplTimes---')]
    for datum in data:
        datum = datum.strip()
        name, value, description = datum.split('|')
        amplTimes[name] = float(value)
        amplTimeDescriptions[name] = description
        
    solveTimes = {}
    solveTimeDescriptions = {}
    data = lines[lines.index('---Start solveTimes---') + 2:lines.index('---End solveTimes---')]
    for datum in data:
        datum = datum.strip()
        name, value, description = datum.split('|')
        solveTimes[name] = float(value)
        solveTimeDescriptions[name] = description
        
    totalShellTimes = {}
    totalShellTimeDescriptions = {}
    data = lines[lines.index('---Start totalShellTimes---') + 2:lines.index('---End totalShellTimes---')]
    for datum in data:
        datum = datum.strip()
        name, value, description = datum.split('|')
        totalShellTimes[name] = float(value)
        totalShellTimeDescriptions[name] = description
        
    totalSolveTimes = {}
    totalSolveTimeDescriptions = {}
    data = lines[lines.index('---Start totalSolveTimes---') + 2:lines.index('---End totalSolveTimes---')]
    for datum in data:
        datum = datum.strip()
        name, value, description = datum.split('|')
        totalSolveTimes[name] = float(value)
        totalSolveTimeDescriptions[name] = description
    
    # construct output
    output['variables'] = variables
    output['objectives'] = objectives
    output['timeMetrics'] = {}
    output['timeMetrics']['amplTimes'] = amplTimes
    output['timeMetrics']['solveTimes'] = solveTimes
    output['timeMetrics']['totalShellTimes'] = totalShellTimes
    output['timeMetrics']['totalSolveTimes'] = totalSolveTimes
    output['timeMetricDescriptions'] = {}
    output['timeMetricDescriptions']['amplTimes'] = amplTimeDescriptions
    output['timeMetricDescriptions']['solveTimes'] = solveTimeDescriptions
    output['timeMetricDescriptions']['totalShellTimes'] = totalShellTimeDescriptions
    output['timeMetricDescriptions']['totalSolveTimes'] = totalSolveTimeDescriptions
    
    return output



if __name__ == '__main__':
    pass