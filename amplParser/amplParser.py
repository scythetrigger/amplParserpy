# Standard Libraries

# Third-Party Libraries

# Information
__author__ = 'Nicholas Parham'
__copyright__ = ''
__credits__ = ['Nicholas Parham']
__license__ = 'Apache Software License'
__version__ = '0.0.0'
__maintainer__ = 'Nicholas Parham'
__email__ = 'nick-99@att.net'
__status__ = 'Dev'

# AMPL REST API Raw Console Output Parser

def addReport(runFile):
    # takes in AMPL runFile and appends code to create a report
    # return a runFile
    reportCode = open('master.run', 'r').read()
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