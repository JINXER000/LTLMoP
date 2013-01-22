
import math, re, sys, random, os, subprocess, time
from logic import to_cnf
from multiprocessing import Pool




def conjunctsToCNF(conjuncts, isTrans, propList, outFilename, depth):
    
    propListNext = map(lambda s: 'next_'+s, propList)
    
    props = {propList[x]:x+1 for x in range(0,len(propList))}
    propsNext = {propListNext[x]:len(propList)+x+1 for x in range(0,len(propListNext))}
    mapping = {conjuncts[x]:[] for x in range(0,len(conjuncts))}
    
    cnfClauses = []
    transClauses = []
    goalClauses = []
    n = 0
    p = len(props)+len(propsNext)       
    
    
    pool = Pool(processes=len(conjuncts))
    print "STARTING CNF MAP"
    allCnfs = map(lineToCnf, conjuncts)   
    print "STARTING CNF MAP"
        
    for cnf, lineOld in zip(allCnfs,conjuncts):
      if cnf is not None: 
        allClauses = cnf.split("&");
        #associate original conjuncts with CNF clauses
        for clause in allClauses:    
            clause = re.sub('[()]', '', clause)   
            clause = re.sub('[|]', '', clause)           
            clause = re.sub('~', '-', clause)    
            #replace prop names with var numbers
            for k in propsNext.keys():
                clause = re.sub(k,str(propsNext[k]), clause)
            for k in props.keys():
                    clause = re.sub(k,str(props[k]), clause)   
                #add trailing 0   
            if "<>" in lineOld:
                goalClauses.append(clause.strip()+" 0\n")
            elif isTrans[lineOld]:
                transClauses.append(clause.strip()+" 0\n")
                cnfClauses.append(clause.strip()+" 0\n")
            else:
                cnfClauses.append(clause.strip()+" 0\n")         
            
        if not "<>" in lineOld:
            mapping[lineOld].extend(range(n+1,n+1+len(allClauses)))    
            n = n + len(allClauses)
                
    #Duplicating transition clauses for depth greater than 1         
    numOrigClauses = len(cnfClauses)   
    for i in range(1,depth+1):
        transClausesNew = []
        for clause in transClauses:
            newClause = ""
            for c in clause.split():
                intC = int(c)
                newClause= newClause + str(cmp(intC,0)*(abs(intC)+len(props)*i)) +" "
            newClause=newClause+"\n"
            transClausesNew.append(newClause)
        j = 0    
        for line in conjuncts:
            if isTrans[line]:                       
                numVarsInTrans = (len(mapping[line]))/i
                mapping[line].extend(map(lambda x: x+numOrigClauses, mapping[line][-numVarsInTrans:]))
                j = j + 1
        n = n + len(transClausesNew)
        p = p + len(props)
        cnfClauses.extend(transClausesNew)
        numOrigClauses = len(transClausesNew)   
    
        
    # Create disjunction of goal over all the time steps         
    """finalDisj = ""     
    
    firstDisj = True        
    for i in range(1,depth+2):   
        newClause = ""                                           
        firstConj = True
        for clause in goalClauses:
             if not firstConj:
                 newClause= newClause + " & "
             f = True
             for c in clause.split():
                 intC = int(c)
                 if intC is not 0:                    
                  if not f:
                     newClause= newClause + " | " + str(cmp(intC,0)*(abs(intC)+len(props)*(i-1)))
                  else:
                     newClause= newClause + str(cmp(intC,0)*(abs(intC)+len(props)*(i-1)))
                 f = False
             firstConj = False
        if finalDisj is not "":
            finalDisj = finalDisj + "|" 
        finalDisj = finalDisj + newClause
        firstDisj = False

        

    
    finalConj = []
    if finalDisj is not "":
        for c in str(to_cnf(finalDisj)).split('&'):
            finalConj.append(re.sub('[\(\)|&]*','',c) + " 0\n")
    
            
            # add disjuncts to the goal clause (goal is satisfied in at least one of the time steps)
            # assumes goals all contain <> on line (so no line breaks within goals)
            if "<>" in line:
                for v in mapping[line]:
                    newDisjuncts = ""
                    currGoals = cnfClauses[v-1].split()
                    numVarsInGoal = (len(currGoals) - 1)/i
                    
                    for c in currGoals[-(numVarsInGoal+1):-1]:
                        intC = int(c)
                        if intC is not 0:                    
                            newDisjuncts= newDisjuncts + str(cmp(intC,0)*(abs(intC)+len(props)*(i))) +" "
                            
                    # adding disjuncts here
                    cnfClauses[v-1] = newDisjuncts + cnfClauses[v-1]                               
"""                

    
    
    #for line in conjuncts:        
        #if "<>" in line:
            #mapping[line] = range(n+1,n+len(finalConj)+1)                       
    
    #n = n + len(finalConj)
    #cnfClauses.extend(finalConj)

 
            

        
        
    """#write CNFs to file        
    open(outFilename, 'w').close()
    output = open(outFilename, 'a')
    output.write("p cnf "+str(p)+" "+str(n)+"\n")
    output.writelines(cnfClauses)
    output.close()
    """
    #dimacs = "p cnf "+str(p)+" "+str(n)+"\n" + "".join(cnfClauses)
    
    for line in conjuncts:        
        if "<>" in line:
            mapping[line] = range(n+1,n+len(goalClauses)+1)   
                        
    return mapping, cnfClauses, goalClauses
    
    #for i in range(0,depth):
    #        for k in propsNext.keys():
    #                print str(propsNext[k]+len(propsNext)*(i)) + " " + k
    #        for k in props.keys():
    #                print str(props[k]+len(props)*(i)) + " " + k


def cnfToConjuncts(cnfIndices, mapping):
    conjuncts = []
    i = 0
    for k in mapping.keys():
        i = i + 1
        if not set(mapping[k]).isdisjoint(cnfIndices):
            conjuncts.append(k)     
            #print k + str(set(mapping[k]).intersection(cnfIndices))
            #print k
    return conjuncts


def lineToCnf(line):
            
        lineOld = line
        line = re.sub('[\t\n]*','',line)            
        line = re.sub('s\.','',line)
        line = re.sub('e\.','',line)   
        line = re.sub(r'(next\()', r'(next_', line)         
        line = re.sub(r'(next\(\s*!)', r'(!next_', line)         
        line = re.sub('\<\>','',line)  
        line = re.sub('\[\]','',line)  
        line = line.strip()
        #trailing &
        line = re.sub('&\s*$','',line)  
        if line!='':
            
            line = re.sub('!', '~', line)
            #line = re.sub('&\s*\n', '', line)
            line = re.sub('[\s]+', ' ', line)        
            line = re.sub('\<-\>', '<=>', line)
            line = re.sub('->', '>>', line)
            line = line.strip() 
            cnf = str(to_cnf(line))
            return cnf
        else:
            return None
        
def findGuiltyClauseIndsWrapper(x):        
        return findGuiltyClauseInds(*x)
        
def findGuiltyClauseInds(cmd, depth, numProps, cnfs, mapping): 
        p = (depth+3)*numProps
        n = len(cnfs)       
        input = "p cnf "+str(p)+" "+str(n)+"\n" + "".join(cnfs)               
            
        
                
        #find minimal unsatisfiable core by calling picomus
        if cmd is None:
            return (False, False, [], "")        
 
        subp = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, close_fds=False)                                            
        output = subp.communicate(input)[0]                                         
                                                                                      
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__

        """#this is the BMC part: keep adding cnf clauses from the transitions until the spec becomes unsatisfiable
            if "UNSATISFIABLE" in output or depth >= maxDepth:
                    break
            depth = depth +1
            """
        if "UNSATISFIABLE" not in output:
            print "Satisfiable at depth" + str(depth)
        else:
            print "Unsatisfiable core found at depth" + str(depth)
                    
            
            
        """#Write output to file (mainly for debugging purposes)
            satFileName = self.proj.getFilenamePrefix()+".sat"
            outputFile = open(satFileName,'w')
            outputFile.write(output)
            outputFile.close()
            """
            
            #get indices of contributing clauses
        """cnfIndices = []
            for line in output:
                if re.match('^v', line):
                    index = int(line.strip('v').strip())
                    if index!=0:
                        cnfIndices.append(index)
            """
        #pythonified the above
        cnfIndices = filter(lambda y: y!=0, map((lambda x: int(x.strip('v').strip())), filter(lambda z: re.match('^v', z), output.split('\n'))))
        return cnfIndices
        
        
        
